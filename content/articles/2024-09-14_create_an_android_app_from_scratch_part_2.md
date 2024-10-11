title: Create an Android app from scratch, with CI, and no knowledge - Part 2
tags: Android

[TOC]

!!! warning " This is a multi-part article"
    You're reading part 2.
    
    * [Part 1]({filename}/articles/2024-09-13_create_an_android_app_from_scratch_part_1.md) focuses on bootstrapping an Android app dev project and run it on an emulated device
    * [Part 2]({filename}/articles/2024-09-14_create_an_android_app_from_scratch_part_2.md) focuses on deploying the app to my phone and create a CI pipeline producing APKs
    * [Part 3]({filename}/articles/2024-10-11_create_an_android_app_from_scratch_part_3.md) focuses on basic Jetpack Compose and Kotlin programming to create a demo UI for LMS

Deploy to my phone
==================

Build the project
-----------------

Two options

1. use Android Studio
    * deploying the app the emulator automatically builds the app (see [Run the app]({filename}/articles/2024-09-13_create_an_android_app_from_scratch_part_1.md#run-the-app))
    * otherwise `Build > Make project` or the keyboard shortcut (CTRL+F9 on Ubuntu Gnome)
2. use the command line
    * `./gradlew build`

Create signed APKs
------------------

### With Android Studio

* I selected `Build > Generate Signed App Bundle / APK...`

* I selected `APK` as I target only my phone (and not Google Play)

![screenshot Select APK and click next]({static}/images/2024-09-14_create_an_android_app_from_scratch_part_2/generate_signed_apk_select_apk.png)

* I selected `Create new` to create a keystore with the wizard, as I don't have one yet

![screenshot Click Create new]({static}/images/2024-09-14_create_an_android_app_from_scratch_part_2/generate_signed_apk_keystore.png)

* I input the following keystore details
    * location: `[path to project]/app/signing_keystore.jks`, this location makes it straightforward to reference it from Gradle (see [From the command line](#from-the-command-line))
    * I used strong passwords for both the keystore and the key
    * I named the key `release` (because this matches the build signing configuration in Gradle (see [From the command line](#from-the-command-line))
    * I only filed the `Organization` with `javatronic.fr` as I don't see the point of providing any personal data

![screenshot Input keystore and key details]({static}/images/2024-09-14_create_an_android_app_from_scratch_part_2/generate_signed_apk_new_keystore.png)

* Click on `Create` creates the keystore and shows the previous screen with all fields completed
* Click on `Next` and make sure to select at least build variant `release`
    * the build variant `debug` actually uses a Google's signing key, see [Verify the APK is signed](#verify-the-apk-is-signed) (this can be overridden, but it doesn't matter at this point)

![screenshot Select build variants]({static}/images/2024-09-14_create_an_android_app_from_scratch_part_2/generate_signed_apk_build_variants.png)

* Android Studio starts a Gradle build with targets `[:app:assembleDebug, :app:assembleRelease]` (if both variants were selected)
    * the logs are visible in the build tab as any other build
      * the APKs are written to directories `app/release` and `app/debug`

!!! hint " Sources"
    * [Generate an upload key and keystore with Android Studio - Android Developer](https://developer.android.com/studio/publish/app-signing#generate-key)

### From the command line

Building from the command line requires a keystore, its password, a key alias and the key password.

I used the one created with Android Studio but Java JDK's `keytool` utility can be used as well (not tested).

Modify `app/build.gradle.kts`

1. before the `buildTypes` bloc, add a signing configuration named `release`. It describes where and how to read the signing key.
    * ➊: create and specify the name of configuration
    * ➋: path can be absolute (not great) or relative to the current Gradle file
    * ➌: the name of the key to use (there can be more than one in a keystore)

```kotlin
    signingConfigs {
        create("release") { # ➊
            storeFile = file("signing_keystore.jks") # ➋
            storePassword = "the_store_password"
            keyAlias = "release" # ➌
            keyPassword = "the_key_password"
        }
    }
```

!!! warning " Don't use passwords in clear-text"
    Use of password written in clear-text in `build.gradle.kts` is bad. A better way, using environment variables, is
    described below.

    It's ok to use locally for testing. Do not push it to GitHub (or any other non-local place) unless you intend to
    delete and drop the keystore, and not use these passwords ever again. 

2. modify the `release` bloc in `buildTypes` to reference and use this new signing configuration
    * ➊: reference the signing configuration with name `release` created above
    * ➋ and ➌: as is from Android Developer reference

```kotlin
    buildTypes {
        release {
            signingConfig = signingConfigs.getByName("release") # ➊
            isMinifyEnabled = false # ➋
            proguardFiles( # ➌
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }
```

3. Generate the signed APKs (both `debug` and `release`, the former appears to be implicit) with

```shell
./gradlew build
```

4. The signed APKs are generated in `app/build/outputs/apk/debug/` and `app/build/outputs/apk/release/`

!!! hint " Sources"
    * [Configure Gradle to sign your app - Android developer](https://developer.android.com/build/building-cmdline#gradle_signing)
    * [Create a keystore for Android signing with keytool - Android developer](https://developer.android.com/build/building-cmdline#sign_cmdline)

Install the app
---------------

I downloaded the release APK onto my phone via SSH from my NAS (because I had this method readily available, but email,
Google Drive or many other ways will do).

On the phone, enable Installation from Unknown Sources:

1. Open `Paramètres` (`Settings`)
2. Open `Sécurité et confidentialité`
3. Open `Autres paramètres de sécurité`
4. Open `Installation applis inconnues`
5. Enable `Amaze` (or any other tool intended to open the APK with)
6. Go to `Amaze`, find the APK, click on it and install it
7. Start `AndroLMS` like any other app

!!! hint " Sources"
    * [Release your app’s APK file and deploy it on your device by Msowski](https://medium.com/@msowski/release-your-apps-apk-file-and-deploy-it-on-your-device-66a5a2177ac8)
    * [Amaze file manager - Google Play](https://play.google.com/store/apps/details?id=com.amaze.filemanager)


Create an Android CI pipeline
=============================

The goal is to have a GitHub Action workflow build and publish APKs with GitHub actions.

This can be achieved with the following steps:

1. Install Java
2. Build the project with Gradle, securely providing the key to sign the APK
3. Upload the APKs as GitHub artifacts
4. Add a comment to the PR (when building on a PR) with a link to download the APKs

Adapt GitHub workflow to a monorepo setup
-----------------------------------------

The `PyLMS` repository contains a Python project. I want to add the Android `AndroLMS` project to the same repo and soon rename the repository to `LMS`.

I've decided to move all Python code to subdirectory `python` and put the Android project into the `android` subdirectory.

The existing workflow building the Python project must be adapted:

* ➊: Rename some steps for consistency
* ➋: run the steps in the `python` subdirectory and not from root anymore
    * depending on the step's implementation, how this is achieved varies
    * `working-directory` works for raw steps
    * commonly, steps using an action accepts `with.working-directory`
    * SonarCloud takes `with.projectBaseDir`
* ➌: Trigger the job only when change happens in the `pyton` subdirectory
    * except changes to `README.md`, as obviously it does not impact the Python artefacts
    * note the `!` at the beginning of the path to exclude it

```yaml
name: PyLMS CI
on:
  push:
    branches:
      - main
    paths: # ➌
      - "python/**"
      - "!python/README.md"
  pull_request:
    types: [opened, synchronize, reopened]
    paths: # ➌
      - "python/**"
      - "!python/README.md"
jobs:
  python-ci: # ➊
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
      with:
        fetch-depth: 0  # Shallow clones should be disabled for a better relevancy of analysis
    - name: Set up Python 3.10
      uses: actions/setup-python@v4
      with:
        python-version: "3.10"
    - name: check-format
      run:  make check-format
      working-directory: python # ➋
    - name: tests
      uses: coactions/setup-xvfb@v1.0.1
      with:
        run: make test-ci
        working-directory: python # ➋
    - name: SonarCloud Scan
      uses: SonarSource/sonarcloud-github-action@master
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}  # Needed to get PR information, if any
      with: # ➋
        projectBaseDir: python/
  python-build: # ➊
    permissions: 
      pull-requests: write 
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Set up Python 3.10
      uses: actions/setup-python@v4
      with:
        python-version: "3.10"
    - name: build
      uses: coactions/setup-xvfb@v1.0.1
      with:
        run: make build
        working-directory: python # ➋
```


!!! hint " Sources"
    * [Monorepo - Wikipedia](https://en.wikipedia.org/wiki/Monorepo)
    * [Using filters to target specific paths for pull request or push events - GitHub doc](https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/triggering-a-workflow#using-filters-to-target-specific-paths-for-pull-request-or-push-events)
    * [jobs.<job_id\>.steps[*].working-directory - GitHub doc](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#jobsjob_idstepsworking-directory)
    * [Sample Github Action workflow for monorepo setup - SonarCloud doc](https://docs.sonarsource.com/sonarcloud/advanced-setup/ci-based-analysis/github-actions-for-sonarcloud/#github-actions-yml-file)


Build Android APKs with GitHub Action
-------------------------------------

Building the APKs with a Github Action workflow is the same as building from the command line (see [From the command line](#from-the-command-line)),
except that it's not acceptable to have the keystore in Git.

We need an alternative way to read it from the disk of the GitHub Action runner.

The one way to access sensitive data in GitHub action is using secrets.

### Change Gradle build to securely read the signing key

Let's change the Gradle build to:

* Read the keystore from a file in the runner's filesystem's temporary folder when executed on a GitHub Action runner 
    * ➊: The situation is detected by checking whether the environment variable `RUNNER_TEMP` is set
    * the `RUNNER_TEMP` directory is emptied at the beginning and end of each job, preventing leak
    * ➋: if not on a runner, read the keystore from the current directory
* ➌: Fail if the subdirectory `androlms` or the `keystore` is not found
    * explicit fail intends to ease debugging
    * using a subdirectory to reduce the risk of collisions in a shared directory
* ➍: Read password from environment variables
    * environment variables can securely be set from GitHub secrets

```kotlin
signingConfigs {
    register("release") {
        keyAlias = "release"
        storePassword = System.getenv("SIGNING_STORE_PASSWORD") # ➍
        keyPassword = System.getenv("SIGNING_KEY_PASSWORD") # ➍
        
        val runnerTemp = System.getenv("RUNNER_TEMP") # ➊
        if (runnerTemp == null) {
            storeFile = file("signing_keystore.jks") # ➋
        } else {
            val keystoreDir = File(runnerTemp, "androlms")
            val keystoreFile = File(keystoreDir, "signing_keystore.jks")
    
            if (!keystoreDir.exists()) { # ➌
                throw FileNotFoundException("${keystoreDir.absolutePath} not found")
            }
            if (!keystoreFile.exists()) { # ➌
                throw FileNotFoundException("${keystoreFile.absolutePath} not found")
            }
            storeFile = keystoreFile
        }
    }
}
```

!!! hint " Sources"
    * [Using secrets in GitHub Actions - GitHub doc](https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions)
    * [RUNNER_TEMP env var in Github Action - GitHub doc](https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/store-information-in-variables#default-environment-variables)
    * [How To Securely Build and Sign Your Android App With GitHub Actions by Yanneck Reiß](https://proandroiddev.com/how-to-securely-build-and-sign-your-android-app-with-github-actions-ad5323452ce)


### Create GitHub repository secrets

GitHub secrets only accepts text, so we must encode the keystore (binary data) with Base64. `openssl` is the best tool
in this context.

The following prints the Base64 encoding of the keystore to the console.

```shell
openssl base64 < app/signing_keystore.jks
```

In GitHub's UI of your repository, go to `Settings > Secrets and variables > Actions` and click on `New Repository Secret`:

* store the encoded keystore under secret `SIGNING_KEYSTORE`
* store passwords under `SIGNING_STORE_PASSWORD` and `SIGNING_KEY_PASSWORD`

![screenshot Create New Repository secret on GitHub]({static}/images/2024-09-14_create_an_android_app_from_scratch_part_2/create_new_repository_secret.png)

!!! note
    The name of the secrets is not important but must be consistent with GitHub workflow steps (see [Create the GitHub Action job](#create-the-github-action-job)).

### Create the GitHub Action job

Gradle has only one requirement: a Java JDK. Android requires Java 17+.

Similarly to the Python project, the job:

* ➊ runs on pushes to the `main` branch (and only that branch)
* ➋ runs when Pull Request are opened, reopened and pushed to
* ➌ runs only when changes are made to the `android` subdirectory, except to the `README.md` file

```yaml
name: AndroLMS CI
on:
  push: # ➊
    branches:
      - main
    paths: # ➌
      - "android/**"
      - "!android/README.md"
  pull_request: # ➋
    types: [opened, synchronize, reopened]
    paths: # ➌
      - "android/**"
      - "!android/README.md"
```

The job has the following steps:

1. Write the keystore from the GitHub Repository secret and write it to the runner's disk
    * ➊ stores the value of secret `SIGNING_KEYSTORE` into environment variable `ENCODED_STRING` of the step
    * ➋ create directory `androlms` in `$RUNNER_TEMP` directory and decode the keystore from Base64 into file `${RUNNER_TEMP}/androlms/signing_keystore.jks`
2. Print the MD5 sum of the keystore (Optional - only for troubleshooting purpose)
3. Check out the repository's content
4. Install Java 17 using action `actions/setup-java@v4`
    * ➌ using `Temurin` distribution because it is opensource and from the Eclipse Foundation 
5. Install Gradle using Gradle's official action `gradle/actions/setup-gradle@v3`
6. Build the APKs
    * ➍ passing password as environment variables
    * ➎ running the same command as [From the command line](#from-the-command-line) with the additional option `--no-daemon` 
      as Gradle's daemon is slow to start and useless since we run Gradle only once

```yaml
jobs:
  android-ci:
    permissions: 
      pull-requests: write 
    runs-on: ubuntu-latest
    steps:
    - name: Decode Keystore
      env:
        ENCODED_STRING: ${{ secrets.SIGNING_KEYSTORE }} # ➊
      run: | # ➋
        TMP_KEYSTORE_FILE_PATH="${RUNNER_TEMP}/androlms"
        mkdir "${TMP_KEYSTORE_FILE_PATH}"
        echo "$ENCODED_STRING" | base64 --decode --ignore-garbage > "${TMP_KEYSTORE_FILE_PATH}/signing_keystore.jks"
    - name: Show Keystore checksum
      run: md5sum "${RUNNER_TEMP}/androlms/signing_keystore.jks"
    - uses: actions/checkout@v4
    - name: Setup Java # ➌
      uses: actions/setup-java@v4
      with:
        distribution: 'temurin'
        java-version: 17
    - name: Setup Gradle
      uses: gradle/actions/setup-gradle@v3
    - name: Build with Gradle
      env:
        SIGNING_STORE_PASSWORD: ${{ secrets.SIGNING_STORE_PASSWORD }} # ➍
        SIGNING_KEY_PASSWORD: ${{ secrets.SIGNING_KEY_PASSWORD }} # ➍
      run: ./gradlew build --no-daemon # ➎
      working-directory: android
```

!!! hint " Sources"
    * [action to install Java (setup-java)](https://github.com/actions/setup-java)
    * [action to install and run Gradle (setup-gradle)](https://github.com/gradle/actions/blob/main/docs/setup-gradle.md)


Make the APKs available for download
------------------------------------

The action from GitHub `actions/upload-artifact` allows upload artifacts and make them available for download from the
Actions User Interface on GitHub.com of a specific run.

* ➊ the name of the archive, both in the UI and for the archive file.
* ➋ put both the `debug` and the `release` APK in the archive


```yaml
    - name: APKs upload
      uses: actions/upload-artifact@v4
      with:
        name: AndroLMS_artifacts # ➊
        path: | # ➋
          android/app/build/outputs/apk/debug/AndroLMS-*.apk 
          android/app/build/outputs/apk/release/AndroLMS-*.apk
```

![screenshot Open GitHub Action UI of a specific run]({static}/images/2024-09-14_create_an_android_app_from_scratch_part_2/go_to_action_ui.png)

![screenshot Download the archive of a specific run]({static}/images/2024-09-14_create_an_android_app_from_scratch_part_2/download_archive_from_action_ui.png)


Shorten retention of a GitHub action archive
--------------------------------------------

By default, uploaded archives are stored for 30 days. Especially for PRs, we don't need that long storage. For the main branch, we can always re-run the job.
So, let's be nice to the planet (and to GitHub) and shorten the retention:

* ➊ set retention to 7 days

```yaml
    - name: APKs upload
      id: apk-upload-step
      uses: actions/upload-artifact@v4
      with:
        name: AndroLMS_artifacts
        path: |
          android/app/build/outputs/apk/debug/AndroLMS-*.apk 
          android/app/build/outputs/apk/release/AndroLMS-*.apk
        retention-days: 7 # ➊
```

Create a PR comment with APK download link
------------------------------------------

I find going to the UI of a specific run too complicated.

I want to have the link to download in a comment on the PR, I only care about the latest built archives, and never mind
the email notifications with every comment on a PR that I configured, the quick access is worth the noise in my mailbox.

Also, for the fun (and my convenience, a bit), let's add to the comment the last day the archive will be available.

Let's modify the workflow:

1. Make the number of days a env variable to share the value between steps
    * ➊ define env variable `UPLOAD_RETENTION` for the whole workflow
    * ➋ use the env variable the `actions/upload-artifact@v4` action
2. add a step computing the expiration date as a string with the Bash's `date` command and make the value an output of the step
    * ➌ `echo "key=value" >> $GITHUB_OUTPUT` is the new syntax to create a step output from command line within a runner 
    * ➍ for other steps to access its output, a step must have an `id`
3. add a step creating a pull request comment
    * ➎ using with action `thollander/actions-comment-pull-request@v2`. Found this action and does the job.
    * ➏ using output of steps "APKs upload" (named `artifact-url`) for the download URL and the date from step 
      "Compute expiration date" (named `expiration_date`) to create a comment with dynamic content
    * ➐ to make the action recreate a comment every time the job runs, use both `comment_tag` (for the action to find 
      its previous comment from run to another) and `mode: recreate` (using `mode: upsert` will not move the comment to
      the end of the conversation)
    * ➑ the same job is used on both PRs and the `main` branch, use this condition to not execute this step for PRs, it
      would fail
    * ➒ to create the PR comment, the job must be given write permissions

```yaml
name: AndroLMS CI
env:
  UPLOAD_RETENTION: 7 # ➊
on:
[...]
jobs:
  android-ci:
    permissions: 
      pull-requests: write # ➒
[...]
    - name: APKs upload
      id: apk-upload-step # ➍
      uses: actions/upload-artifact@v4
      with:
        name: AndroLMS_artifacts
        path: |
          android/app/build/outputs/apk/debug/AndroLMS-*.apk 
          android/app/build/outputs/apk/release/AndroLMS-*.apk
        retention-days: ${{ env.UPLOAD_RETENTION }} # ➋
    - name: Compute expiration date
      id: expiration-date # ➍
      run: echo "expiration_date=$(date --date ${UPLOAD_RETENTION}d +%Y-%m-%d)" >> $GITHUB_OUTPUT # ➌
    - uses: thollander/actions-comment-pull-request@v2 # ➎
      if: ${{ github.event_name == 'pull_request' }} # ➑
      with:
        message: Latest AndroLMS artifacts available from ${{ steps.apk-upload-step.outputs.artifact-url }} until ${{ steps.expiration-date.outputs.expiration_date }}. # ➏
        comment_tag: apk-upload # ➐
        mode: recreate # ➐
``` 

And here is a sample of the result

![screenshot PR comment to download AndroLMS archive]({static}/images/2024-09-14_create_an_android_app_from_scratch_part_2/androlms_artifact_download_comment.png)


!!! hint " Sources"
    * [Get the artifact download URL from the `upload-artifact` action - GitHub doc](https://github.com/actions/upload-artifact?tab=readme-ov-file#using-outputs)
    * [Passing information between jobs - GitHub doc](https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/passing-information-between-jobs)
    * [Write permission to create a PR comment - `actions-comment-pull-request` action doc](https://github.com/thollander/actions-comment-pull-request?tab=readme-ov-file#permissions)
    * [Conditionally run a step, including an exemple for running only in Pull Request - GitHub doc](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#jobsjob_idstepsif)
    * [Create step output from Command Line - GitHub blog](https://github.blog/changelog/2022-10-11-github-actions-deprecating-save-state-and-set-output-commands/#examples)
    * [Compute the current date in GitHub action (but uses deprecated syntax) - Stackoverflow](https://stackoverflow.com/a/60942437)

Verify the APK is signed
------------------------

Finally, we need to confirm the produced APKs are signed as expected.

After downloading the AndroLMS archives from GitHub, use the `apksigner` tool from the Android SDK.

The `--print-certs` options shows digest and certificates fields of the key used to sign the APK:

```shell
$ /[some_path]/sdk/build-tools/34.0.0/apksigner apksigner verify --print-certs /tmp/AndroLMS-1.0-release.apk 
Signer #1 certificate DN: O=javatronic.fr
Signer #1 certificate SHA-256 digest: e8b09ece77c0f37a24c9cc5dbe1f83a16ffc563a337c03d938324c71b2c01ea9
Signer #1 certificate SHA-1 digest: c968ba63a8b8270e23d7c16247805f6fcb00333a
Signer #1 certificate MD5 digest: 26aee2775b3f788fc33dea2611ad7e31
```

Using `apksigner` of the debug APK shows Google's key is used:

```shell
$ /[some_path]/sdk/build-tools/34.0.0/apksigner apksigner verify --print-certs /tmp/AndroLMS-1.0-debug.apk              
Signer #1 certificate DN: C=US, O=Android, CN=Android Debug
Signer #1 certificate SHA-256 digest: 0f244cc1996da11be5d27a08c58dcc58519fcb88f6a980ad2706cfafa9dbb373
Signer #1 certificate SHA-1 digest: 15d42424d81e9ca193bbcd0a7f95c3f39dca7711
Signer #1 certificate MD5 digest: 3b59ba84d68a1f45d71d528a4ff34836
```

!!! warning 
    One can find many articles advising using Java JDK's `keytool` or `jarsigner` tool to verify an APK is signed.

    Those are most likely outdated as Jar signing was the first signing scheme used and appears to not be used by
    default anymore. See below for insights.

Using `--verbose` shows that `apksigner` verifies multiple signature scheme and informs which one is used:

```shell
$ /[some_path]/sdk/build-tools/34.0.0/apksigner apksigner verify --verbose --print-certs /tmp/AndroLMS-1.0-release.apk              
Verifies
Verified using v1 scheme (JAR signing): false
Verified using v2 scheme (APK Signature Scheme v2): true
Verified using v3 scheme (APK Signature Scheme v3): false
Verified using v3.1 scheme (APK Signature Scheme v3.1): false
Verified using v4 scheme (APK Signature Scheme v4): false
Verified for SourceStamp: false
Number of signers: 1
Signer #1 certificate DN: O=javatronic.fr
Signer #1 certificate SHA-256 digest: e8b09ece77c0f37a24c9cc5dbe1f83a16ffc563a337c03d938324c71b2c01ea9
Signer #1 certificate SHA-1 digest: c968ba63a8b8270e23d7c16247805f6fcb00333a
Signer #1 certificate MD5 digest: 26aee2775b3f788fc33dea2611ad7e31
Signer #1 key algorithm: RSA
Signer #1 key size (bits): 2048
Signer #1 public key SHA-256 digest: 211d040fd3924474e9052fb87eb549bc0e76cf96371d4a607f88046f88922e8c
Signer #1 public key SHA-1 digest: 72ad7d19e7cd951e92f9c2ea9756f28aac9d5367
Signer #1 public key MD5 digest: 1faa2d71812f475b21e40663c158866d
```