---
layout: post
title: Using Jekyll for GitHub pages
description: Personnal notes for installing and using Jekyll for GitHub pages
tags: sublime, github, ruby
---

Installing
----------

- Ruby and RubyGems as first prerequisite
  + Ruby 1.93 required (as of now)
    * installing rubygems directly only installs Ruby 1.8.x => need to install ruby manually
    * ruby-dev package seems required to build gem github-pages
      - otherwise, you might get an error :
        + resource : [http://stackoverflow.com/questions/7645918/require-no-such-file-to-load-mkmf-loaderror](http://stackoverflow.com/questions/7645918/require-no-such-file-to-load-mkmf-loaderror)
      
      ```
      ERROR:  Error installing github-pages:
      ERROR: Failed to build gem native extension.

            /usr/bin/ruby1.9.1 extconf.rb
            /usr/lib/ruby/1.9.1/rubygems/custom_require.rb:36:in `require': cannot load such file -- mkmf (LoadError)
              from /usr/lib/ruby/1.9.1/rubygems/custom_require.rb:36:in `require'
              from extconf.rb:1:in `<main>'
      ```

    * installation

  ```sh
  sudo apt-get install ruby
  sudo apt-get install ruby1.9.1-dev
  ```

  + RubyGems

  ```sh
  sudo apt-get install rubygems
  ```

- Installing Jekyll

  ```sh
  sudo gem install jekyll
  ```

- Installing GitHub Pages specific package
  + Source : [https://help.github.com/articles/using-jekyll-with-pages#installing-jekyll](https://help.github.com/articles/using-jekyll-with-pages#installing-jekyll)

  ```sh
  sudo gem install github-pages
  ```

- Installing Rake
  + Rake is a build tool that we can use to automate several blog editing task
  
  ```sh
  sudo gem install rake
  ```

  + Rake build file is name `Rakefile` and is written in pure Ruby

Markdown Editing in Sublime Text
-----------------------

- Excellent resource
  - [http://www.macstories.net/roundups/sublime-text-2-and-markdown-tips-tricks-and-links/](http://www.macstories.net/roundups/sublime-text-2-and-markdown-tips-tricks-and-links/)
- Install Sublime Text
  - see [Installing Sublime for my use]({% post_url 2014-01-08-installing_sublime_for_my_use %})
- Extends Sublime for better editing experience (via Package Control)
  - Add package MarkdownEditing
    - installation
      + [http://ttscoff.github.com/MarkdownEditing/](http://ttscoff.github.com/MarkdownEditing/)
      + CTRL+SHIFT+P > Install Package
      + package name is "MarkdownEditing"
    - configuration
      + set "GitHub flavored Markdown" as default
        * open a Markdown file
        * select your flavor from the menu: View > Syntax > Open all with current extension as
      + overwrite few properties of MarkdownEditing to have black theme, not centered editing, no wrapping
        * open user preferences Preferences > Package Settings > MarkdownEditing > Markdown GFM Settings - User
        * change content with below

        ```json
        {
          "extensions":
          [
            "md",
            "mdown",
            "txt",
            "markdown"
          ],

          "color_scheme": "Packages/MarkdownEditing/MarkdownEditor-Dark.tmTheme",

          // Layout
          "draw_centered": false,
          "word_wrap": false,
          "wrap_width": 120
        }
        ```

  - Add Syntax highlighting sublime-markdown-extended (for reference, not used, MarkdownEditing is better)
    + [https://github.com/jonschlinkert/sublime-markdown-extended](https://github.com/jonschlinkert/sublime-markdown-extended)
    + CTRL+SHIFT+P > Install Package
    + package name is "Markdown Extended"
  - Add Color Theme Monokai Extended (not used for markdown, but good theme for other files)
    + [https://github.com/jonschlinkert/sublime-monokai-extended](https://github.com/jonschlinkert/sublime-monokai-extended)
    + CTRL+SHIFT+P > Install Package
    + package name is "Monokai Extended"
    + select as default color theme
      * Preferences > Color sheme > Monakai Extended > Monakai Extended
      * Bright sheme hurts my eyes

 