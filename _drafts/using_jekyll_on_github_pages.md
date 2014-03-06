---
layout: post
title: Using Jekyll for GitHub pages
description: Personnal notes for installing and using Jekyll for GitHub pages
tags: sublime, github, ruby
---

Installing
----------

### Ruby and RubyGems as first prerequisite
* Ruby 1.9.3 is required (as of now)
  + installing rubygems directly only installs Ruby 1.8.x => need to install ruby manually
  + to list installed packages via APT, you can use `sudo dpkg --get-selections`
    - source [http://akyl.net/how-list-all-installed-packages-ubuntu-centos-and-other-linux-systems](http://akyl.net/how-list-all-installed-packages-ubuntu-centos-and-other-linux-systems)
  + ruby-dev package seems required to build gem github-pages
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

  + installation

```sh
sudo apt-get install ruby1.9.1
sudo apt-get install ruby1.9.1-dev
```

* Under Ubuntu 12.04 on my XPS 13, ruby 1.8 is the default alternative. To force 1.9.1 :

```sh
sudo unlink /etc/alternatives/ruby
sudo ln -s /usr/bin/ruby1.9.1 /etc/alternatives/ruby
```

* RubyGems
  + Under Ubuntu 12.04 on my XPS 13, there seems to be an already install rubygems 1.8.11, which was not installed via apt-get 

```sh
sudo apt-get install rubygems
```

### Installing Jekyll

  ```sh
  sudo gem install jekyll
  ```

### Installing GitHub Pages

Source : [https://help.github.com/articles/using-jekyll-with-pages#installing-jekyll](https://help.github.com/articles/using-jekyll-with-pages#installing-jekyll)

  ```sh
  sudo gem install github-pages
  ```

### Installing Rake

Rake is a build tool that we can use to automate several blog editing task

  ```sh
  sudo gem install rake
  ```

  + Rake build file is name `Rakefile` and is written in pure Ruby

### Running Jekyll

Run the command below on the root of your GitHub pages clone

* starts jekyll to diplay posts AND draft and watch for changes
* jekyll can then be stoped with CTRL+C
* by default website is visible on http://localhost:4000

```sh
jekyll serve --draft --watch
```

