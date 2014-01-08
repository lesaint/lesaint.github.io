---
layout: post
title: Installing Sublime for my use
description: How I installed Sublime Text 2 on Ubuntu
tags: sublime
---

Installing
----------

* Download Sublime from website
    - download linux 64 bit version at [http://www.sublimetext.com/2](http://www.sublimetext.com/2)
        - latest version at the time of my writing is 2.0.2
    - save to `/opt/INSTALL_MEDIA`
* create `/opt/sublimetext` directory

```sh
cd /opt
sudo mkdir sublimetext
sudo chown lesaint:lesaint sublimetext
```

* cp tar file to `/opt/sublime`, decompress it and create symbolic link to the current version
    
```sh
cp ../INSTALL_MEDIA/Sublime\ Text\ 2.0.2\ x64.tar.bz2 .
tar xvfj Sublime\ Text\ 2.0.2\ x64.tar.bz2
mv Sublime\ Text\ 2 2.0.2
ln -s 2.0.2 sublime
```

Executing
---------

* add sublime to local bin directory for convenient command line use
    
```sh
ln -s /opt/sublimetext/sublime/sublime_text /usr/local/bin/sublime
```

* create sidebar launcher in Unity
    - create a desktop file in `~/.local/share/applications/` called `sublimetext.desktop` with following content

    ```
    [Desktop Entry]
    Name=Sublime Text 2
    Exec="/opt/sublimetext/sublime/sublime_text" %F
    MimeType=text/plain;
    Terminal=false
    Type=Application
    Icon=/opt/sublimetext/sublime/Icon/256x256/sublime_text.png
    Categories=GNOME;GTK;Utility;TextEditor;Development;
    Actions=New;

    [Desktop Action New]
    Name=New Editor Window
    Exec="/opt/sublimetext/sublime/sublime_text" --new-window
    MimeType=text/plain;
    OnlyShowIn=Unity;
    ```

    - resources :
        + [http://www.sublimetext.com/forum/viewtopic.php?f=2&t=3457#p43852](http://www.sublimetext.com/forum/viewtopic.php?f=2&t=3457#p43852)
        + [http://www.saintsjd.com/2012/10/create-a-sidebar-launcher-for-sublime-text-2-in-ubuntu-unity/](http://www.saintsjd.com/2012/10/create-a-sidebar-launcher-for-sublime-text-2-in-ubuntu-unity/)

Minimal Sublime tuning
----------------------

* Install Package Control extension
    - see instructions at [https://sublime.wbond.net/installation](https://sublime.wbond.net/installation)
* Keyboard shortcuts
    - make delete line shortcut actually useable
        + default shurtcut ctrl+shift+k can not be used with a single hand
        + open use shorcut preferences : Preferences > Key Bindings - User
        + add the following line (which overwrite default's ctrl+d key binding for command find_under_expand)

        ```json
            { "keys": ["ctrl+d"], "command": "run_macro_file", "args": {"file": "Packages/Default/Delete Line.sublime-macro"} }
        ```
