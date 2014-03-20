---
layout: post
title: Learning Ruby
tags: ruby
---

I joined a new project in january with several Ruby based technos (Capistrano, Puppet, ...) and since I am now using GitHub pages as a website/blog solution which is also Ruby powered, I believe its time to really learn the language.

This post will be the place where I will keep notes of this croisade out of Java.


Help & Documentation
--------------------

## Learning resources :

* [Rubylearning.com](http://rubylearning.com)
    - since it was the first result in Google, I started the course right away but then I found ...
* [Ruby quickstart, Ruby in Twenty Minutes](https://www.ruby-lang.org/en/documentation/quickstart/)
    - first time I heard of the Interactive Ruby command line tool `irb`, usefull for quick testing and learning
    - faster dive into Ruby. RubyLearning is more detailed and rigourous
* [RubyMonk](https://rubymonk.com/)
* [Ruby Quick ref](http://www.zenspider.com/Languages/Ruby/QuickRef.html)
* [Ruby complete documentation](http://www.ruby-doc.org/)

### Cheat sheets

#### The Ruby Cheat Sheet
* This is a command line tool to get access to some [Ruby Cheat sheets](http://cheat.errtheblog.com/) (and other language/tools such as bash)
* RubyLearning has a link to it
* Intallation

```sh
sudo gem install cheat
```

* Listing sheets with the `cheat sheets` command currently fails with a 404. I fear the projet is not maintained anymore
* sheets list I compiled and tested
    + cheat : the help of cheat
    + bash : basic bash command line usage
    + string : String litteral
    + strftime
    + assertions
    + migrations
    + sprintf
    + datamapper
    + and there seems to be a bunch of [funy cheat sheets](http://errtheblog.com/posts/91-the-best-of-cheat)

#### Ruby cheat sheet at Socrateos
Very useful cheat sheet, for Ruby 1.9 : [http://socrateos.blogspot.fr/2011/05/ruby-cheat-sheets.html](http://socrateos.blogspot.fr/2011/05/ruby-cheat-sheets.html)

#### Ruby minitest cheat sheet
I haven't started testing, so I don't have an opinion on this sheet yet : [http://danwin.com/2013/03/ruby-minitest-cheat-sheet/](http://danwin.com/2013/03/ruby-minitest-cheat-sheet/)

## Leaning notes

* listing of a Class methods
    - all methods, including inherited ones : `Foo.instance_methods`
    - all methods, including inherited ones : `Foo.instance_methods(false)`
* to make ruby files executable under a Unix like environement
    - add the following line as the first line of your Ruby file
    
    ```
    #!/usr/bin/env ruby
    ```

    - `chmod` the file to make it executable and then run it like a bash script
