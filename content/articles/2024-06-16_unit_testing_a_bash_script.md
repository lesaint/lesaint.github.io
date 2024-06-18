title: Unit testing a Bash script
tags: Bash, Testing

[TOC]

# Fixing rsync-time-backup

[rsync-time-backup](https://github.com/lesaint/rsync-time-backup) is a Bash script I maintain that wraps around
[rsync](https://linux.die.net/man/1/rsync) to produce Apple Time Machine style backups.

`rsync` is able to create incremental backups thanks to its `--link-dest=DIR` option, that creates hardlinks to files in
`DIR` when unchanged. 

To leverage this option, `rsync-time-backup` has a key piece of logic that resolves the directory (let's call it `LINK_DEST`)
to use as the argument to the `link-dest` option.

Resolving `LINK_DEST` must support several use cases. When the script runs:

1. for the 1st time
2. any later time
3. after a previous backup attempt failed/was interrupted
4. after several previous backup attempts failed/were interrupted.

Last week, I changed the logic for the 4th use case because it was broken: the script would use an incomplete
backup attempt as `LINK_DEST` and this broke the incremental backup, recreating many unchanged files as new.

!!! note ""
    The changes to `rsync-time-backup` described in this article are visible in commits
    [e2bc6ad](https://github.com/lesaint/rsync-time-backup/commit/e2bc6ad08cdca55db548351666e1c04ba3ce6023) and 
    [6577c3](https://github.com/lesaint/rsync-time-backup/commit/6577c3eb714778bd8173d90145f749b955994b69).

**Keep and automate the tests**

When coding the new logic, I found myself creating several directories reproducing the above use cases
(and several others) to test my changes. 

Unit testing is seldom practice in `Bash`, probably due to the nature and usage of `Bash`, as well as due to the lack of
tooling.

Nevertheless, it's such a pity not to have these tests to prevent regressions during future changes. So I
decided to take on the challenge, try and write Unit Test for Directory Resolution, time-boxed to a weekend.

# Code Unit tests for Bash

The basic requirements for useful Unit Tests in Bash are:

1. run the tests
2. run the script from the tests
3. inspect and run only the code under test
4. ensure reproducibility
5. ensure stateless execution to achieve reentrancy of the tests
6. declare the expected behaviors with assertions, which would fail the test if not met

## Run the tests

Following common practices in other programming languages, I'll code tests in a dedicated directory: `tests`.   
I'll have one script per feature under test, i.e. a test suite: `directory_resolution.sh`.

```shell
➜  rsync-time-backup git:(master) tree
.
├── README.md
├── rsync_tmbackup.sh
└── tests
    ├── directory_resolution.sh
```

## Run the script from the tests

[KISS][kiss], I'll hardcore the path to `rsync_tmbackup.sh`, expecting test suites always to be called from their directory.

```shell
fn_run_test() {
    local test_dir="$1"
    local under_test="../../../rsync_tmbackup.sh"
[...]
```

## Inspect and run only the code under test

Directory resolution is only one of many `rsync-time-backup` features. I don't want to run these other features when
testing directory resolution.

In other programming languages, the usual practice is to have the feature under test in a separate piece of code
(a class, a package, a library, ...).
In `Bash`, the candidates I see are files or functions.

Such isolation does not exist (yet) and I decided against refactoring because:

1. I lack tests to prevent regression during this refactoring (sic!)
2. My focus is on proving I can write Unit Tests for Bash, not on writing testable Bash code (yet)

So, I went for a simpler solution (which is also a bad practice) and altered my production code with two control points
for my tests:

* The first one prints directory-resolution-related variables.
* The second one prints the same variables and stops `rsync-time-backup`.
* Both are inactive unless the variable `TEST1` is set.

Printing allows me to inspect the code. Exiting allows me to only execute the directory resolution code (almost, see [Conclusions](#conclusions)).

```shell
--- i/rsync_tmbackup.sh
+++ w/rsync_tmbackup.sh
@@ -165,6 +165,32 @@ fn_dest_chown_link() {
     fi
 }
 
+# -----------------------------------------------------------------------------
+# Test code
+# -----------------------------------------------------------------------------
+fn_is_test1_active() {
+    [ -n "${TEST1}" ]
+}
+
+fn_test_1_echo_vars() {
+    echo "TEST1: SYM_LINK=$SYM_LINK DEST=$DEST LINK_DEST=$LINK_DEST LAST_BACKUP_DIR=$LAST_BACKUP_DIR"
+}
+
+fn_test_1_step_1() {
+    if fn_is_test1_active; then
+        fn_test_1_echo_vars
+    fi
+}
+
+fn_test_1_step_2() {
+    if fn_is_test1_active; then
+        fn_test_1_echo_vars
+        # end test
+        echo "TEST1: end execution"
+        exit 0
+    fi
+}
+
 # -----------------------------------------------------------------------------
 # Source and destination information
 # -----------------------------------------------------------------------------
@@ -300,6 +326,8 @@ else
     LINK_DEST="$(fn_dest_find_last_backup)"
 fi
 
+fn_test_1_step_1
+
 # -----------------------------------------------------------------------------
 # Handle case where a previous backup failed or was interrupted.
 # -----------------------------------------------------------------------------
@@ -330,6 +358,8 @@ if [ -n "$(fn_dest_find "$INPROGRESS_FILE")" ]; then
     fi
 fi
 
+fn_test_1_step_2
+
 # Run in a loop to handle the "No space left on device" logic.
 while : ; do
```

## Ensure reproducibility

There is one non-deterministic piece of code in Directory Resolution: the name of the new backup directory is generated 
from the current date.

Such code is a challenge to test, notably because it is a dependency to code outside our own.

The common practice in other programming languages in such case is to mock, or patch in `Python`, the dependency.

There are no libraries to mock or patch with `Bash`<sup>*</sup>.

Focusing on my goal to write tests, I went for the same (and bad) solution as above: I altered the production code.

This time, I replaced the code that computes the name of a directory from the current date with a function and allowed
variable `INJECT_NOW` to be set to provide the value to return instead of calling the system's `date` function.

```shell
--- i/rsync_tmbackup.sh 
+++ w/rsync_tmbackup.sh
@@ -273,7 +273,15 @@ fi
 # -----------------------------------------------------------------------------
 
 # Date logic
-NOW=$(date +"%Y-%m-%d-%H%M%S")
+fn_now() {
+    if [ -n "${INJECT_NOW}" ]; then
+        echo "$INJECT_NOW"
+    else
+        date +"%Y-%m-%d-%H%M%S"
+    fi
+}
+
+NOW=$(fn_now)
 EPOCH=$(date "+%s")
 KEEP_ALL_DATE=$((EPOCH - 86400))       # 1 day ago
 KEEP_DAILIES_DATE=$((EPOCH - 15768000)) # 6 months
```

!!! note ""
    *<sup>\*</sup> I didn't do an extensive search. At least, there is none in the standard `Bash` ecosystem.*

## Setup and teardown for reentrancy

Directory resolution needs... directories. A source directory (the one to back up) and a target directory (the one 
where to create backups).

I'll create source and target directories for the tests in a dedicated directory for a run of the test suite, which I 
create in setup code and execute before all tests.

```shell
# creates a directory dedicated to this run of tests
fn_prepare_test() {
    mkdir -p "out"
    TEST_DIR="$(mktemp --tmpdir="out" -d test1-XXXXXXXX)"
}

[...]

##########################
#--- the actual tests ---#
##########################
# Suite level preparation
fn_prepare_test
```

The source directory is only read and can be the same for tests. This one is set up once for all tests.

```shell
# creates an empty directory
fn_prepare_source_dir() {
    mkdir -p "$TEST_DIR/src"
}

[...]

##########################
#--- the actual tests ---#
##########################
# Test level preparation
fn_prepare_test
# same source dir is used for all tests
fn_prepare_source_dir
```

Target directory changes from one test to the other AND directory resolution may its content (when resuming from an interrupted backup).

I have setup code before each test, creating the directories for that one test:

```shell
# creates an empty directory
fn_prepare_source_dir() {
    mkdir -p "$TEST_DIR/src"
}

# create a target directory with name 1st argument and executes method 2nd argument in it
fn_prepare_target_dir() {
    local test_dir="$1"
    local prepare_function="$2"
    local target_dir="$TEST_DIR/target/$test_dir"

    echo ""
    echo "**************** $test_dir ****************"

    mkdir -p "$target_dir"
    cd "$target_dir"
    echo "Preparing $test_dir..."
    $prepare_function

    cd "../../../../"
}

#--- common functions used during prepare of a test ---#
fn_marker_file() {
    touch "backup.marker"
}

fn_inprogress_file() {
    touch "backup.inprogress"
}

fn_latest_symlink() {
    local target_dir="$1"
    ln -s "$target_dir" "latest"
}

[...]

fn_prepare_target_2nd_backup_interrupted() {
    fn_marker_file
    mkdir "2022-04-19-202210"
    mkdir "2022-10-25-213541"
    fn_latest_symlink "2022-04-19-202210"
    fn_inprogress_file
}
fn_prepare_target_dir "2nd_backup_interrupted" "fn_prepare_target_2nd_backup_interrupted"
```

After successfully completing the tests, I delete the directory for the suite in a piece of teardown code for the test suite.    

```shell
fn_teardown_test() {
    echo ""
    echo "Clean up: deleting ${TEST_DIR}..."
    rm -Rf -- "$TEST_DIR"
}

[...]

fn_teardown_test

[EOF]
```

## Implement assertions

Because this is the way I verified the code behavior when modifying directory resolution, I want to code assertions 
against some logs produced by the script.

The assertions will be line-based and will be exact matches ([KISS][kiss] again).   
They come in 2 flavors: 1/ find a line in the logs 2/ verify the logs ends with the N following lines

To code assertions on the script output, I need:

1. to capture the script output (both `stdout` and `stderr`, indistinctly for now)
2. have a readable and convenient way to declare expected line or lines

The former is achieved by storing the output into variable `TEST_OUTPUT`.

```shell
# Runs the executable under_test with the specified $1 directory as target.
# Output of execution of under_test is set into variable TEST_OUTPUT
fn_run_test() {
    local test_dir="$1"
    local under_test="../../../rsync_tmbackup.sh"
    local out=""

    # ensure no leakage from previous test
    TEST_OUTPUT=""

    # print content of target directory
    tree "$TEST_DIR/target/$test_dir"

    # temporarily do not exit if command returns a non-zero exit code
    # doc: https://www.gnu.org/savannah-checkouts/gnu/bash/manual/bash.html#The-Set-Builtin
    echo "Running $test_dir..."
    cd "$TEST_DIR"
    # make sure executable exists and is accessible
    if ! [ -x "$under_test" ]; then
        echo "$(pwd)/$under_test is not accessible or executable"
        exit 1
    fi
    set +e
    TEST_OUTPUT="$( ${under_test} "src" "target/$test_dir" 2>&1 )"
    set -e
    cd "../.."
    echo "$TEST_OUTPUT"
}
```

!!! tip
    I use `set +e` and `set -e` around the call to the script because the whole test suite is coded with 
    [Bash unofficial strict mode](http://redsymbol.net/articles/unofficial-bash-strict-mode/). Otherwise, the script
    exiting with a non-zero code would exit the whole test suite.

The latter is achieved by having lines as function arguments and use ``\`` to put each expected line on a different line.

### Assertions output contains line(s)

```shell
# checks whether a single line is present in TEST_OUTPUT
fn_test_output_contains_line() {
    local expected="$1"
    # declare line local to prevent leak of lines read in this function out of it
    local line=""

    # read TEST_OUTPUT line by line and compare each of them to searched line
    # source: https://superuser.com/a/284226
    while IFS= read -r line; do
        if [ "$line" == "$expected" ]; then
            return 0
        fi
    done <<< "$TEST_OUTPUT"
    return 1
}

# checks whether test output contains all the specified lines (one line per argument), IN NO SPECIFIC ORDER
fn_test_output_contains_lines() {
    local line=""
    for line in "$@"; do
        if ! fn_test_output_contains_line "${line}"; then
            echo "[TEST FAILURE] Expecting output to contain \"$line\""
            exit 1
        fi
    done
}

[...]

fn_run_test "no_marker_file"
fn_test_output_contains_lines \
    "rsync_tmbackup: Safety check failed - the destination does not appear to be a backup folder or drive (marker file not found)." \
    "rsync_tmbackup: mkdir -p -- \"target/no_marker_file\" ; touch \"target/no_marker_file/backup.marker\""
```

### Assertion output ends with line(s)

```shell
# checks that the last lines of TEST_OUTPUT are the same as the lines provided as arguments (IN ORDER)
fn_test_output_ends_with() {
    # concatenating arguments with new lines in between
    # source: https://www.baeldung.com/linux/add-newline-variable-bash#4-shell-parameter-expansion
    local expected=""
    for arg in "$@"; do
        expected="${expected}${arg}"$'\n'
    done
    # remove trailing \n
    expected="${expected::-1}"

    # capture the last n lines of TEST_OUTPUT
    # $# is the number of arguments
    local tested=$(echo "$TEST_OUTPUT" | tail "-$#")

    # diff between two variables
    # source: https://stackoverflow.com/a/13437445
    if ! diff <(echo "$tested") <(echo "$expected"); then
        echo "[TEST FAILURE] Expecting output to end with (see diff output above):"
        for arg in "$@"; do
            echo "  $arg"
        done
        exit 1
    fi
}

[...]

fn_run_test "1st_backup"
fn_test_output_ends_with \
    "rsync_tmbackup: target/1st_backup/latest exists and targets existing directory target/1st_backup/2022-04-19-202210." \
    "TEST1: SYM_LINK=target/1st_backup/latest DEST=target/1st_backup/${INJECT_NOW} LINK_DEST=target/1st_backup/2022-04-19-202210 LAST_BACKUP_DIR=target/1st_backup/2022-04-19-202210" \
    "TEST1: SYM_LINK=target/1st_backup/latest DEST=target/1st_backup/${INJECT_NOW} LINK_DEST=target/1st_backup/2022-04-19-202210 LAST_BACKUP_DIR=target/1st_backup/2022-04-19-202210" \
    "TEST1: end execution"
```

# Conclusions

Positive conclusions:

* it works! And it does the job, failing when log changes
* the test code is very succinct, readable and to the point, writing new tests is easy and fast
* the exercise confirms that Unit Testing is not language-specific, only the tooling is. 

Improvements:

* the script could be easier to test, isolating features in function or files
    * this would also remove the tests having side effects unrelated to the feature under test:  e.g. creation of the `pid` file  
* the test could have assertions on the content of the source and target directories instead of assertions on logs
    * this would be less brittle: test can fail because logs changed while directories are still in the expected state
    * behavior on directories IS what is expected from the script, not logs
    * this would imply less to no production code changes
* writing tests for other pieces of the script may not be as easy/possible
    * code was located at the beginning of the script
    * code worked solely on directories and symlink, with little state to set up and to verify
    * dependencies on external code were small (just `date`)

Further writing of Unit Test for `Bash` will certainly be an opportunity for more fun and learning. 


[kiss]: https://en.wikipedia.org/wiki/KISS_principle

