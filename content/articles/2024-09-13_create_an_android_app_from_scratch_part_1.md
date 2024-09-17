title: Create an Android app from scratch, with CI, and no knowledge - Part 1
tags: Android

[TOC]

!!! warning " This is a multi-part article"
    You're reading part 1.
    
    * [Part 1]({filename}/articles/2024-09-13_create_an_android_app_from_scratch_part_1.md) focuses on bootstrapping an Android app dev project and run it on an emulated device
    * [Part 2]({filename}/articles/2024-09-14_create_an_android_app_from_scratch_part_2.md) focuses on deploying the app to my phone and create a CI pipeline producing APKs
    * Part 3 will focus on basic Jetpack Compose and Kotlin programming to create a demo UI for LMS

The context
===========

Work on [PyLMS](https://github.com/lesaint/PyLMS/) has proved that the approach is viable enough to continue.

However, a CLI or a Desktop GUI are not the best to access the information I may store in the tool. 
Only my phone is (almost) always at reach when a "Lacune Mémorielle Sociale" (aka LMS) hits me.

I need an Android App, but I have never programmed one (I only looked at Android programming quickly many years ago).

Last Monday (today is Friday), I decided to create one, with the following goals and constraints:

* create a UI that demonstrates the feasibility of listing persons and filtering them by inputting text
* use state-of-the-art Android programming
* my phone is the only target
* demonstrate deployment on it
* demonstrate building APKs with Github Actions
* setup minimal quality control (with SonarCloud)
* refactor PyLMS repository to hold both PyLMS and the Android App

!!! note " Disclaimer"
    This series describes what I did in less than 4 days, starting with zero knowledge on Android and Kotlin development, 
    googling and reading my way toward a solution.
    
    Any Android- and Kotlin-related statement reflects the knowledge acquired over that short period.

    Of course, I'm skipping all the back and forth, tries and errors, and only describing the end result.

Install Android Studio
======================

Android Studio (Koala Feature Drop at the moment) is THE IDE for Android Development.

I followed these steps to install it:

1. download from [Android Developers](https://developer.android.com/studio) ([direct link](https://redirector.gvt1.com/edgedl/android/studio/ide-zips/2024.1.2.12/android-studio-2024.1.2.12-linux.tar.gz), skips the licence to skip the licence agreement screen)
2. Unpack the `.tar.gz` to an appropriate location (`~/DEV/Android_Studio` in my case)
    ```
    tar xvfz android-studio-2024.1.2.12-linux.tar.gz
    mv android-studio 2024.1.2.12
    ln -s 2024.1.2.12
    ```
3. Install i386 libraries because I run a 64-bit version of Linux
    ```
    sudo apt-get install libc6:i386 libncurses5:i386 libstdc++6:i386 lib32z1 libbz2-1.0:i386
    ```
4. Open terminal and launch Android Studio
    ```
    ~/DEV/Android_Studio/current/bin/studio.sh
    ```
5. Do not import previous Android Studio settings
6. Complete the Android Studio Setup Wizard
    * I selected "custom install" but it would not let me install any other SDK than 35
    * I selected `~/DEV/Android_Studio/android` as destination

    ![screenshot Install Wizard Installation Type]({static}/images/2024-09-13_create_a_POC_android_app_from_scratch/setup_wizard_select_install_type.png)

    ![screenshot Install Wizard SDK Componnents Setup]({static}/images/2024-09-13_create_a_POC_android_app_from_scratch/setup_wizard_sdk_components_setup.png)

8. Wizard advised configuring hardware acceleration for the emulator (see [Install Emulator Acceleration](#install-emulator-acceleration))

    ![screenshot Install Wizard Emulator Settings]({static}/images/2024-09-13_create_a_POC_android_app_from_scratch/setup_wizard_emulator_settings.png)

7. Create Desktop entry with `Tools > Create Desktop Entry...`
8. Search `Android Studio` in Gnome's application hub and add it to favorites


!!! hint " Sources"
    * [Install Android Studio on Linux - Android Developers](https://developer.android.com/studio/install#linux)
    * [Set up the Android 14 SDK - Android Developers](https://developer.android.com/about/versions/14/setup-sdk)

Install Android SDK
===================

I checked `Settings > About my phone > About software` in phone, it runs Android 14.

I need to install Android SDK Platform 34 package for Android 14.0 ("UpsideDownCake") and remove SDK 35.

1. Open Settings with `File > Settings` and go to `Android SDKs`
2. Untick `Android API 35` and tick `Android 14.0 ("UpsideDownCake")` with API Level `34`

![screenshot Install Android SDK]({static}/images/2024-09-13_create_a_POC_android_app_from_scratch/install_android_sdk.png)

Bootstrap an application
========================

Use Android Studio `File > New > New Project...`:

![screenshot Android Studio Create Project wizard screen 1]({static}/images/2024-09-13_create_a_POC_android_app_from_scratch/new_project_wizard_1.png)
![screenshot Android Studio Create Project wizard screen 2]({static}/images/2024-09-13_create_a_POC_android_app_from_scratch/new_project_wizard_2.png)

* select template `Empty Activity`
* Name: `AndroLMS`
* Package: `fr.javatronic.lms.android`

Run on an emulator
==================

Create a device
---------------

1. Open the Device Manager

    ![screenshot Create Virtual Device in Device Manager]({static}/images/2024-09-13_create_a_POC_android_app_from_scratch/create_virtual_device_in_device_manager.png)

2. Open Create a new Hardware Profile

    ![screenshot Open New Hardware Profile]({static}/images/2024-09-13_create_a_POC_android_app_from_scratch/new_hardware_profile.png)

3. Create Galaxy S23 profile

    ![screenshot Create Hardware Profile screen]({static}/images/2024-09-13_create_a_POC_android_app_from_scratch/create_hardware_profile_screen.png)
    (S23 data comes from Samsung's skin website (see [Use a phone skin](#use-a-phone-skin)))

Install Emulator Acceleration
-----------------------------

1. Install and run `cpu-checker`
    ```
    $ sudo apt-get install cpu-checker
    $ sudo sudo kvm-ok
    INFO: /dev/kvm exists
    KVM acceleration can be used
    $ sudo apt-get remove cpu-checker
    ```
2. Install KVM
    ```
    sudo apt-get install qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils
    ```
3. verify with
    ```
    $ ~/DEV/Android_Studio/android/sdk/emulator/emulator -accel-check
    INFO    | Storing crashdata in: /tmp/android-lesaint/emu-crash-35.1.20.db, detection is enabled for process: 711988
    accel:
    0
    KVM (version 12) is installed and usable.
    accel
    ```

!!! hint " Sources"
    * [Configure VM acceleration on Linux - Android Developer](https://developer.android.com/studio/run/emulator-acceleration#vm-linux)
    * [Checking if android emulator is using KVM accelation or not? - Stackoverflow](https://stackoverflow.com/a/63975329)

Run the app
-----------

To run the app in Emulator:

![screenshot Run the app in emulator]({static}/images/2024-09-13_create_a_POC_android_app_from_scratch/run_the_app_in_emulator.png)

1. Make sure the device created earlier is selected
2. Maks sure `app` is selected
    * `app` is the name of Gradle submodule that contains the Android App in the Gradle project generated by Android Studio
3. Click on the 'Run' icon
    * if the icon is disabled, make sure the Gradle configuration is synchronized. If so you may be seeing this banner. Click on `Sync`. 

    ![screenshot Run the app in emulator]({static}/images/2024-09-13_create_a_POC_android_app_from_scratch/run_the_app_in_emulator.png)

4. The emulated device's screen appears in a panel on the right-hand side of the IDE
   (screenshot of `AndroLMS` MVP UI, not of the generated application)

![screenshot Emulated device screen]({static}/images/2024-09-13_create_a_POC_android_app_from_scratch/emulated_device_no_skin.png)

Stop the emulator
-----------------

Closing the tab with the device screen is not enough. To make sure the emulator is stopped, go to the Device Manager and click on the square icon.

![screenshot Stop the emulator]({static}/images/2024-09-13_create_a_POC_android_app_from_scratch/stop_the_emulator.png)

Use a phone skin
----------------

A "skin" can be used to better visualize the application's look on the screen with the device's borders around it and 
the whole shape of the device.

I googled and found a Samsung page where I can download a skin for the S23, with the specification of the S23's screen.

![screenshot S23 skin]({static}/images/2024-09-13_create_a_POC_android_app_from_scratch/s23_specifications.png)

1. Download the skin's zip file from the [website](https://developer.samsung.com/galaxy-emulator-skin/galaxy-s.html) to `~/DEV/Android_Studio/android/skin/`
2. Unzip it
3. Open the Device Manager and edit the S23 device

    ![screenshot Edit device in Device Manager]({static}/images/2024-09-13_create_a_POC_android_app_from_scratch/edit_device_from_device_manager.png)

4. Display advanced settings
   
    ![screenshot Show advanced settings of device]({static}/images/2024-09-13_create_a_POC_android_app_from_scratch/show_advanced_settings.png)

5. Scroll to the very bottom, tick "Enable device frame" and select the directory where the skin is stored `~/DEV/Android_Studio/android/skin/Galaxy_S23`

    ![screenshot Show advanced settings of device]({static}/images/2024-09-13_create_a_POC_android_app_from_scratch/select_skin.png)

6. Stop the emulator (see [Stop the emulator](#stop-the-emulator)) and run the app again (see [Run the app](#run-the-app))

    ![screenshot Emulated device screen with skin]({static}/images/2024-09-13_create_a_POC_android_app_from_scratch/emulated_device_with_skin.png)


!!! note
    Samsung documentation advises unchecking "Launch in the Running Devices tool window" to launch Android Emulator as a
    standalone application and ensure correct rendering of the skin.

    I initially followed this advise, which opened the emulator in a new window rather than in a tab, but reverted as I
    noticed the skin rendered correctly.

!!! hint " Sources"
    * [Galaxy S skins downloads - Samsung developer](https://developer.samsung.com/galaxy-emulator-skin/galaxy-s.html)
    * [Skin installation following instruction - Samsung developer](https://developer.samsung.com/galaxy-emulator-skin/guide.html)


