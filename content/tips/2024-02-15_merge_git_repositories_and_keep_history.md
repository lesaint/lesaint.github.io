title: Merge multiple Git repositories while keeping history
tags: Git


# WHY

I have 5 repositories (they are all private) holding scripts for my home backup strategy.
I clone them on my NAS and maintain them on my laptop.

* `onsite_backup`
* `offsite_backup`
* `local_backup`
* `phanas_scripts`
* `onsite_backup_copy`

Cloning multiple repositories on multiple machine is cumbersome.

It is also error-prone as consistency between the scripts is sometimes required.

In addition, some code is duplicated and has diverged on a couple occasions already. 

# WHAT

I want to merge all repositories into `phanas_scripts`, keeping the history.

I'll follow this procedure:

1. in each repository, move content to a subdirectory with the name of the repo
2. merge content of the 3 other repos into `phanas_scripts`
3. to keep the history, use `git merge --allow-unrelated-histories`

!!! note " Sources"

    * [https://stackoverflow.com/a/76831513](https://stackoverflow.com/a/76831513)

# HOW

```shell
cd ~/tmp
mkdir work_dir
cd work_dir

# clone repositories, the target one and those to merge
g clone git@github.com:lesaint/phanas_scripts.git
g clone git@github.com:lesaint/local_backup.git
g clone git@github.com:lesaint/onsite_backup.git
g clone git@github.com:lesaint/offsite_backup.git
g clone git@github.com:lesaint/onsite_backup_copy.git

# move local_backup repository content to a subdirectory
cd local_backup
mkdir local_backup
git mv local_backup.sh README.md rtb.sh sync_on_nas.sh local_backup/
# fix rtb.sh symlink, broken by the move
unlink rtb.sh
cd local_backup
ln -s ../../rtb/rsync_tmbackup.sh rtb.sh
git add rtb.sh
git commit -m "move local_backup repository content to subdirectory local_backup"

# do the same with offsite_backup repository
cd ../offsite_backup
mkdir offsite_backup
git mv exclude_rtb_managed_dirs offsite_backup.sh README.md sync_on_phanas.sh offsite_backup/
git commit -m "move offsite_backup repository content to offsite_backup subdirectory"

# do the same with onsite_backup repository
cd ../onsite_backup
mkdir onsite_backup
git mv backup.sh exclude_rtb_managed_dirs README.md onsite_backup/
git commit -m "move onsite_backup repository content to onsite_backup subdirectory"
# take the opportunity to fix the name of the script
cd onsite_backup
git mv backup.sh onsite_backup.sh
git commit -m "rename backup.sh to onsite_backup.sh for consistency"

# do the same with onsite_backup_copy repository
cd ../onsite_backup_copy
mkdir onsite_backup_copy
git mv copy.sh exclude.rsync README.md onsite_backup_copy/
git commit -m "move onsite_backup_copy repo content to onsite_backup_copy subdirectory"

# go to target repository and add all source directories local clones as remote
cd ../phanas_scripts
git remote add onsite_backup ../onsite_backup
git remote add offsite_backup ../offsite_backup
git remote add local_backup ../local_backup
git remote add onsite_backup_copy ../onsite_backup_copy

# fetch all repository contents
git fetch --all

# merge, one after the other, all source repositories
git merge --allow-unrelated-histories onsite_backup/master -m "merge 'onsite_backup' repository into 'phanas_scripts' repository"
git merge --allow-unrelated-histories offsite_backup/master -m "merge 'offsite_backup' repository into 'phanas_scripts' repository"
git merge --allow-unrelated-histories local_backup/master -m "merge 'local_backup' repository into 'phanas_scripts' repository"
git merge --allow-unrelated-histories onsite_backup_copy/master -m "merge 'onsite_backup_copy' repository into 'phanas_scripts' repository"

# clean up remotes
git remote remove local_backup
git remote remove offsite_backup
git remote remove onsite_backup 
git remote remove onsite_backup_copy

git push
```
