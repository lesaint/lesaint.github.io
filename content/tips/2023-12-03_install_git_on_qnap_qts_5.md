title: Install Git on QNAP's QTS 5.X
tags: QNAP, Git

`Git` is not installed by default on QNAP's QTS 5.X systems (nor was it on QTS 4.X).

In absence of standard package managers (eg. `apt`), `Git` must be installed via a third-party App Repository in QNAP's App Center.

After searching the web and finding many references to non-existent or now-gone App Centers, I settled on using [MyQnap](https://www.myqnap.org):

1. it "replaces" QnapCloud.eu after this website disappeared
	* some maintainers from QnapClub moved to MyQnap but they don't relate ([source](https://www.reddit.com/r/qnap/comments/108u0qn/qnapclub_is_back_and_no_longer_called_qnapclub/))
2. it's a third-party QNAP App store with many open source utilities packaged as Apps
3. Installed the app named `QGit` (or `Git` once installed)

!!! warning

	There are very little security waranties with installing any software from MyQnap.

	However, the convience appears to be worth trusting the people behind the package, is it?

# Install Git

Add MyQnap App Repository:

![screenshot add app repository in QTS]({static}/images/2023-12-03_install_git_on_qnap_qts_5/screenshot_add_qnap_repository.jpg)

Install the `Git` app:

![screenshot install git app from myqnap]({static}/images/2023-12-03_install_git_on_qnap_qts_5/screenshot_install_git_app.jpg)

!!! note " Sources"

    * [MyQnap documentation: How to install the repository](https://www.myqnap.org/install-the-repo/)