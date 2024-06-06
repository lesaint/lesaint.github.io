title: No more out-of-the-box search support for Elegant theme anymore
tags: Pelican, Javatronic, Python

# tipue_search abandoned

Element theme documentation suggests using the following configuration to enable search, which relies on the `tipue_search` plugin:

```python
PLUGINS = ['tipue_search']
DIRECT_TEMPLATES = ['search']
```

Unfortunately, this plugin and the jquery code it relies on is abandoned, as stated on Pelican Plugin's page of the plugin:

![screenshot tipue_search abandoned message]({static}/images/2024-05-03_enabling_search_in_elegant_theme/tipue_search_abandoned_screenshot.png)

`pelican_search` plugin should be used instead, but how?

> sources:
> 
> * https://elegant.oncrashreboot.com/add-search
> * [tipue_search's plugin Github page](https://github.com/pelican-plugins/tipue-search?tab=readme-ov-file)

# pelican_search abandoned

pelican_search relies on `stork` and this tool should be installed prior to install and run the Pelican plugin: 

Install Stork  on Ubuntu:

```shell
cd ~/bin
wget -O stork https://files.stork-search.net/releases/v1.6.0/stork-ubuntu-20-04
chmod +x stork
```

Unfortunately, running stork fails on Ubuntu 22.04:

```shell
$ stork
stork: error while loading shared libraries: libssl.so.1.1: cannot open shared object file: No such file or directory
```

At this point, I started searching for a solution.
Found one for 2-years old Ubuntu 20 ([https://stackoverflow.com/a/72633324](https://stackoverflow.com/a/72633324)) that required manually installing a specific
version of OpenSSL and that I would not have followed even if it applied to Ubuntu 22.

And then I found out the one maintainer of the project had stepped out a year ago:

![screenshot stork_search abandoned message]({static}/images/2024-05-03_enabling_search_in_elegant_theme/stork_search_abandoned_screenshot.png)

> sources: 
> 
> * [Stork install instructions](https://stork-search.net/docs/install)
> * [Maintainer's post on winding down from project](https://github.com/jameslittle230/stork/discussions/360)

# Search with Google

I don't have enough time to investigate alternative solutions to stork and the pelican_search plugin.

However, I can customize the Elegant Theme search field, that I have forked.

In file `base.html`, I can replace

```html
<li><form class="navbar-search" action="{{ SITEURL }}/{{ SEARCH_URL }}" onsubmit="return validateForm(this.elements['q'].value);"> <input type="text" class="search-query" placeholder="Search" name="q" id="tipue_search_input"></form></li>
```

by the following and create a Google search in a new window with `site:www.javatronic.fr` as a filter:

```html
{% if SEARCH_URL %}
<li><form class="navbar-search" action="{{SEARCH_URL}}" onsubmit="return validateForm(this.elements['q'][0].value);" target="_blank"> <input type="text" class="search-query" placeholder="Search" name="q" id="tipue_search_input"><input type="hidden" name="q" value="site:{{ SITEURL }}"></form></li>
{% endif %}
```
                      


