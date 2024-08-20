title: Tilde expansion in SSH client broken on QNAP
tags: QNAP

[TOC]

I have a nightly job running on my QNAP NAS (QTS 5.1.8.2823 2024/07/12), connecting to a remote device over SSH.
The job had been running fine for months, but a couple of days ago, it started failing with `The authenticity of host '[<redacted>]:<redacted> ([<redacted>]:<redacted>)' can't be established.`.

I started investigating because the host had not changed (neither IP nor SSH server configuration), the host identity
was and is still in `~/.ssh/known_hosts` and accepting the new host information simply isn't the right secure move.

# TLDR

The error was only one of several symptoms caused by the expansion of `~` (tilde) in the path to the user's identity
file (eg. `~/.ssh/id_rsa`) or known_hosts file (`~/.ssh/known_hosts`) not working on my QNAP device for non-root users.

I initially had the error with the admin user created upon initial setup of my QNAP system and reproduced with another
non-root user.

A workaround is to create a user SSH client configuration file `~/.ssh/config` and add two options with absolute paths
to the files know_hosts and identity files:

```
UserKnownHostsFile /home/the_user/.ssh/known_hosts
IdentityFile /home/the_user/.ssh/id_rsa
```

Oddly enough, this workaround demonstrates that tilde expansion appears to work for the SSH client configuration file.

As to what causes the failed tilde expansion, I don't know at this point but pinned down to a handful possible causes
(see [Tilde expansion works for some files but not others](#tilde-expansion-works-for-some-files-but-not-others)).
I opened a support ticket at QNAP.

!!! note ""
    To ease reading, instead of redacting information, I'll use dummy values for SSH port number (`9999`), user (`the_user`), hostname (`donut.acme.com`) and IP (`126.126.126.126`).

# Host identity hash protocol is different

I reproduced the SSH call and the error directly from the command line and activated the full debug logs to try and
understand what caused the host authentication error:


```shell
$ ssh -vvvv -p 9999 the_user@donut.acme.com 'ls -1'
```

And here is an extract of the output around the host authentication failure:

```shell
debug1: expecting SSH2_MSG_KEX_ECDH_REPLY
debug3: receive packet: type 31
debug1: SSH2_MSG_KEX_ECDH_REPLY received
debug1: Server host key: ssh-ed25519 SHA256:<redacted>
debug3: put_host_port: [126.126.126.126]:9999
debug3: put_host_port: [donut.acme.com]:9999
debug1: load_hostkeys: fopen /.ssh/known_hosts: No such file or directory
debug1: load_hostkeys: fopen /.ssh/known_hosts2: No such file or directory
debug1: load_hostkeys: fopen /usr/etc/ssh_known_hosts: No such file or directory
debug1: load_hostkeys: fopen /usr/etc/ssh_known_hosts2: No such file or directory
debug1: checking without port identifier
debug1: load_hostkeys: fopen /.ssh/known_hosts: No such file or directory
debug1: load_hostkeys: fopen /.ssh/known_hosts2: No such file or directory
debug1: load_hostkeys: fopen /usr/etc/ssh_known_hosts: No such file or directory
debug1: load_hostkeys: fopen /usr/etc/ssh_known_hosts2: No such file or directory
debug3: hostkeys_find_by_key_hostfile: trying user hostfile "/.ssh/known_hosts"
debug1: hostkeys_find_by_key_hostfile: hostkeys file /.ssh/known_hosts does not exist
debug3: hostkeys_find_by_key_hostfile: trying user hostfile "/.ssh/known_hosts2"
debug1: hostkeys_find_by_key_hostfile: hostkeys file /.ssh/known_hosts2 does not exist
debug3: hostkeys_find_by_key_hostfile: trying system hostfile "/usr/etc/ssh_known_hosts"
debug1: hostkeys_find_by_key_hostfile: hostkeys file /usr/etc/ssh_known_hosts does not exist
debug3: hostkeys_find_by_key_hostfile: trying system hostfile "/usr/etc/ssh_known_hosts2"
debug1: hostkeys_find_by_key_hostfile: hostkeys file /usr/etc/ssh_known_hosts2 does not exist
The authenticity of host '[donut.acme.com]:9999 ([126.126.126.126]:9999)' can't be established.
```

At this point, I'm not sure what to think of these logs.

However, I notice that the job does connect to the server just before the failure, with a `rsync` command over
`ssh`. The only difference is that the `rsync` command runs with `sudo` and explicitly provides the path to the identity
file on the command line. So `sudo` is really the only difference (keep that in mind for later). 

So I try with `sudo` and intend to compare the debug output.

```shell
$ sudo ssh -vvvv -i /home/the_user/.ssh/id_rsa -p 9999 the_user@donut.acme.com 'ls -1'
```

And here is an extract of the output around the host authentication failure:

```shell
debug1: expecting SSH2_MSG_KEX_ECDH_REPLY
debug3: receive packet: type 31
debug1: SSH2_MSG_KEX_ECDH_REPLY received
debug1: Server host key: ecdsa-sha2-nistp256 SHA256:<redacted>
debug3: put_host_port: [126.126.126.126]:9999
debug3: put_host_port: [donut.acme.com]:9999
debug3: record_hostkey: found key type ECDSA in file /root/.ssh/known_hosts:2
debug3: load_hostkeys_file: loaded 1 keys from [donut.acme.com]:9999
debug1: load_hostkeys: fopen /root/.ssh/known_hosts2: No such file or directory
debug1: load_hostkeys: fopen /usr/etc/ssh_known_hosts: No such file or directory
debug1: load_hostkeys: fopen /usr/etc/ssh_known_hosts2: No such file or directory
debug1: Host '[donut.acme.com]:9999' is known and matches the ECDSA host key.
debug1: Found key in /root/.ssh/known_hosts:2
```

I noticed that the host key protocol is `ecdsa-sha2-nistp256` with `sudo`, while it is `ssh-ed25519` without it.

From previous knowledge of the SSH protocol, my assumption was that the client, somehow, would request different
protocols from the server for authentication. So, I want to loop up earlier occurrences of the protocol names in both
logs but decide to simply text-compare the whole logs, to get a better view and see all the differences.

![screenshot meld diff logs with and without sudo]({static}/images/2024-08-18_ssh_tilde_expansion_in_SSH_broken_on_qnap/meld_diff_ssh_debug_logs.png)

This highlights the reason a different protocol is used:

* when `sudo` is used: a key for the host is found and the SSH client requests protocols that match the existing key
    ```
    debug3: record_hostkey: found key type ECDSA in file /root/.ssh/known_hosts:2
    [...]
    debug3: order_hostkeyalgs: prefer hostkeyalgs: ecdsa-sha2-nistp256-cert-v01@openssh.com,ecdsa-sha2-nistp256
    ```
* when `sudo` is not used: no key is found and the SSH client let the server send hash key in its favorite protocol
    ```
    debug1: load_hostkeys: fopen /.ssh/known_hosts: No such file or directory
    [...]
    debug3: order_hostkeyalgs: no algorithms matched; accept original
    ```

# known_host file is not read

As stated before, the host key IS present in the user's know_host file `/home/the_user/.ssh/known_host`. In addition,
it is the same as the one in root user's known_host file `/root/.ssh/known_hosts`.

So, the question becomes why is the user's know_host file not read?

`/home/the_user/.ssh/known_host` does not appear in logs. `/.ssh/known_host` is shown instead and, of course, does not
exist since the path `/.ssh/` is not valid.

The following log caught my attention and demonstrates that, when not running as root, `~` is not replaced by 
`/home/the_user` as it should be. 

```shell
debug3: expanded UserKnownHostsFile '~/.ssh/known_hosts' -> '/.ssh/known_hosts'
```

This debug log is produced by at [line 1522](https://github.com/openssh/openssh-portable/blob/V_9_8_P1/ssh.c#L1522-L1523)
in SSH client's `main` function.

```c
for (j = 0; j < options.num_user_hostfiles; j++) {
    if (options.user_hostfiles[j] == NULL)
        continue;
    cp = tilde_expand_filename(options.user_hostfiles[j], getuid());
    p = default_client_percent_dollar_expand(cp, cinfo);
    if (strcmp(options.user_hostfiles[j], p) != 0)
        debug3("expanded UserKnownHostsFile '%s' -> "
            "'%s'", options.user_hostfiles[j], p);
    free(options.user_hostfiles[j]);
    free(cp);
    options.user_hostfiles[j] = p;
}
```

The expansion is performed by function [`tilde_expand_filename`](https://github.com/openssh/openssh-portable/blob/V_9_8_P1/misc.c#L1245-L1253), 
calling the implementation function [`tilde_expand`](https://github.com/openssh/openssh-portable/blob/V_9_8_P1/misc.c#L1173-L1243).

``` { .c linenos=true }
char *
tilde_expand_filename(const char *filename, uid_t uid)
{
	char *ret;

	if (tilde_expand(filename, uid, &ret) != 0)
		cleanup_exit(255);
	return ret;
}

/*
 * Expands tildes in the file name.  Returns data allocated by xmalloc.
 * Warning: this calls getpw*.
 */
int
tilde_expand(const char *filename, uid_t uid, char **retp)
{
	char *ocopy = NULL, *copy, *s = NULL;
	const char *path = NULL, *user = NULL;
	struct passwd *pw;
	size_t len;
	int ret = -1, r, slash;

	*retp = NULL;
	if (*filename != '~') {
		*retp = xstrdup(filename);
		return 0;
	}
	ocopy = copy = xstrdup(filename + 1);

	if (*copy == '\0')				/* ~ */
		path = NULL;
	else if (*copy == '/') {
		copy += strspn(copy, "/");
		if (*copy == '\0')
			path = NULL;			/* ~/ */
		else
			path = copy;			/* ~/path */
	} else {
		user = copy;
		if ((path = strchr(copy, '/')) != NULL) {
			copy[path - copy] = '\0';
			path++;
			path += strspn(path, "/");
			if (*path == '\0')		/* ~user/ */
				path = NULL;
			/* else				 ~user/path */
		}
		/* else					~user */
	}
	if (user != NULL) {
		if ((pw = getpwnam(user)) == NULL) {
			error_f("No such user %s", user);
			goto out;
		}
	} else if ((pw = getpwuid(uid)) == NULL) {
		error_f("No such uid %ld", (long)uid);
		goto out;
	}

	/* Make sure directory has a trailing '/' */
	slash = (len = strlen(pw->pw_dir)) == 0 || pw->pw_dir[len - 1] != '/';

	if ((r = xasprintf(&s, "%s%s%s", pw->pw_dir,
	    slash ? "/" : "", path != NULL ? path : "")) <= 0) {
		error_f("xasprintf failed");
		goto out;
	}
	if (r >= PATH_MAX) {
		error_f("Path too long");
		goto out;
	}
	/* success */
	ret = 0;
	*retp = s;
	s = NULL;
 out:
	free(s);
	free(ocopy);
	return ret;
}
```

If my understanding of the code is correct, the home directory path is retrieved by calling function `getpwuid(uid)` and
reading the returned field `pw_dir` ([here](https://github.com/openssh/openssh-portable/blob/V_9_8_P1/misc.c#L1226)),
which `uuid` argument is retrieved by a call to function `getuuid()` ([here](https://github.com/openssh/openssh-portable/blob/V_9_8_P1/ssh.c#L1519)).

According to [getpwuid man page](https://linux.die.net/man/3/getpwuid), reads the `/etc/passwd` file and I confirmed
that the user's directory is set in this file.

```c
slash = (len = strlen(pw->pw_dir)) == 0 || pw->pw_dir[len - 1] != '/';

if ((r = xasprintf(&s, "%s%s%s", pw->pw_dir,
    slash ? "/" : "", path != NULL ? path : "")) <= 0) {
```

According to the code above, the string `~/.ssh/known_hosts` being transformed to `/.ssh/known_hosts` could have two
possible causes:

* `pw->pw_dir` is an empty string, in which case the heading slash in `/.ssh/known_hosts` comes from `slash` variable
being `true` (because `len` is `0`)
* `pw->pw_dir` is `/`


# Workaround

Without much hope, because accessing it also requires expanding the tilde, I tried providing the path to the known_hosts
file in the user's SSH client config file `~/.ssh/config` (remember to change the file permissions `chmod 600 ~/.ssh/config`):

```
UserKnownHostsFile /home/the_user/.ssh/known_hosts
```

Authenticating the remote host worked but the SSH command failed with a new error:

```
debug1: Authentications that can continue: publickey
debug3: start over, passed a different list publickey
debug3: preferred publickey,keyboard-interactive,password
debug3: authmethod_lookup publickey
debug3: remaining preferred: keyboard-interactive,password
debug3: authmethod_is_enabled publickey
debug1: Next authentication method: publickey
debug1: Will attempt key: /.ssh/id_rsa 
debug1: Will attempt key: /.ssh/id_ecdsa 
debug1: Will attempt key: /.ssh/id_ecdsa_sk 
debug1: Will attempt key: /.ssh/id_ed25519 
debug1: Will attempt key: /.ssh/id_ed25519_sk 
debug1: Will attempt key: /.ssh/id_xmss 
debug2: pubkey_prepare: done
debug1: Trying private key: /.ssh/id_rsa
debug3: no such identity: /.ssh/id_rsa: No such file or directory
debug1: Trying private key: /.ssh/id_ecdsa
debug3: no such identity: /.ssh/id_ecdsa: No such file or directory
debug1: Trying private key: /.ssh/id_ecdsa_sk
debug3: no such identity: /.ssh/id_ecdsa_sk: No such file or directory
debug1: Trying private key: /.ssh/id_ed25519
debug3: no such identity: /.ssh/id_ed25519: No such file or directory
debug1: Trying private key: /.ssh/id_ed25519_sk
debug3: no such identity: /.ssh/id_ed25519_sk: No such file or directory
debug1: Trying private key: /.ssh/id_xmss
debug3: no such identity: /.ssh/id_xmss: No such file or directory
debug2: we did not send a packet, disable method
debug1: No more authentication methods to try.
the_user@donut.acme.com: Permission denied (publickey).
```

This demonstrates that tilde expansion is also failing for the identity file, which must also be provided with an 
absolute path in `~/.ssh/config`:

```
UserKnownHostsFile /home/the_user/.ssh/known_hosts
IdentityFile /home/the_user/.ssh/id_rsa
```

# Tilde expansion works for some files but not others

Investigation so far allowed us to corner down that tilde expansion works for the user's SSH config file but does not 
for the user's known_host file and identity file.

Let's see how expansion happens for the user's SSH config file.

Path config file appears to not be expanded with function `tilde_expand` but computed with a specific piece of code:

* user's SSH config file is resolved and read in function `process_config_files` ([source](https://github.com/openssh/openssh-portable/blob/V_9_8_P1/ssh.c#L556-L587))
* the user's directory is concatenated with a constant unless a config file was explicitly provided ([source](https://github.com/openssh/openssh-portable/blob/V_9_8_P1/ssh.c#L575-L576)) 
```c
r = snprintf(buf, sizeof buf, "%s/%s", pw->pw_dir, _PATH_SSH_USER_CONFFILE);
```
* value of `_PATH_SSH_USER_CONFFILE` is `.ssh/config` ([source](https://github.com/openssh/openssh-portable/blob/V_9_8_P1/pathnames.h#L61-L94)) 
```c
#define _PATH_SSH_USER_DIR		".ssh"
[...]
#define _PATH_SSH_USER_CONFFILE		_PATH_SSH_USER_DIR "/config"
```
* and `pw` in `pw->pw_dir` also comes from calls to `getuid` and `getpwuid` ([source](https://github.com/openssh/openssh-portable/blob/V_9_8_P1/ssh.c#L709-L716))
```c
/* Get user data. */
pw = getpwuid(getuid());
if (!pw) {
    logit("No user exists for uid %lu", (u_long)getuid());
    exit(255);
}
/* Take a copy of the returned structure. */
pw = pwcopy(pw);
```
* `pwcopy` does a plain copy of the field `pw_dir` ([source](https://github.com/openssh/openssh-portable/blob/V_9_8_P1/misc.c#L483-L507)):
```c
struct passwd *
pwcopy(struct passwd *pw)
{
	struct passwd *copy = xcalloc(1, sizeof(*copy));

	copy->pw_name = xstrdup(pw->pw_name);
	copy->pw_passwd = xstrdup(pw->pw_passwd == NULL ? "*" : pw->pw_passwd);
#ifdef HAVE_STRUCT_PASSWD_PW_GECOS
	copy->pw_gecos = xstrdup(pw->pw_gecos);
#endif
	copy->pw_uid = pw->pw_uid;
	copy->pw_gid = pw->pw_gid;
#ifdef HAVE_STRUCT_PASSWD_PW_EXPIRE
	copy->pw_expire = pw->pw_expire;
#endif
#ifdef HAVE_STRUCT_PASSWD_PW_CHANGE
	copy->pw_change = pw->pw_change;
#endif
#ifdef HAVE_STRUCT_PASSWD_PW_CLASS
	copy->pw_class = xstrdup(pw->pw_class);
#endif
	copy->pw_dir = xstrdup(pw->pw_dir);
	copy->pw_shell = xstrdup(pw->pw_shell);
	return copy;
}
```

To sum up, the difference between tilde expansion for the user SSH client config file and the known_host and identity files could be:

* a bug in string replacement code I could have missed?
* the usage of `pwcopy` making a difference?
* a different `uuid` being returned by `getuid()`?
* `getpwuid()` somehow not returning the same structure on the second/later call?
