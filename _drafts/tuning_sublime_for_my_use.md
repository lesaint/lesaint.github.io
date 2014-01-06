---
layout: post
title: Tuning Sublime for my use
description: Personnal notes for tuning Sublime Text 2
tags: sublime
---

Keyboard shortcuts
------------------

* make delete line shortcut actually useable
    - default shurtcut ctrl+shift+k can not be used with a single hand
    - open use shorcut preferences : Preferences > Key Bindings - User
    - add the following line (which overwrite default's ctrl+d key binding for command find_under_expand)

    ```json
    	{ "keys": ["ctrl+d"], "command": "run_macro_file", "args": {"file": "Packages/Default/Delete Line.sublime-macro"} }
    ```

