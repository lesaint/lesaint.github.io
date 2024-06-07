title: Display Table of Content on Elegant for Pelican
tags: Pelican

[TOC]

I did the following to enable Table of Contents display, on the side of posts, in Elegant theme:

## Enable `toc` extension

Python Markdown's extension [Table of Contents](https://python-markdown.github.io/extensions/toc/)

```python
MARKDOWN = {
  'extension_configs': {
    'markdown.extensions.toc': {}
  }
}
```

## Install `extract_toc`

Install the Pelican's plugin `extract_toc`

* this plugin is part of `pelican-plugins` [repository](https://github.com/getpelican/pelican-plugins)
* at some point, this plugin should be moved to its own repository
* to save on downloading the whole repo, I'm simply to going to copy it here

  ```shell
  mkdir plugins
  cd plugins
  git clone https://github.com/getpelican/pelican-plugins.git
  cp -r pelican-plugins/extract_toc .
  ```

## Install `extract_toc`'s dependency

Add to `requirements.txt`

```shell
beautifulsoup4
```

## Enable `extract_toc`

Add to `pelicanconf.py`:

```python
PLUGIN_PATHS = [
    "plugins"
]
PLUGINS = [
    "extract_toc"
]
```

## Enable permalinks

Add setting to Python Markdown TOC extension to enable permalinks to posts' headings:

```python
MARKDOWN = {
  'extension_configs': {
    'markdown.extensions.toc': {}
  }    
}
```


!!! note " Sources"

    * extract_toc's [README](https://github.com/getpelican/pelican-plugins/tree/master/extract_toc)
    * Elegant's documentation: [Add a Table of Contents to Your Articles](https://elegant.oncrashreboot.com/how-elegant-displays-table-of-contents)
    * Elegant's documentation: [Permalinks to Headings](https://elegant.oncrashreboot.com/permalinks-to-headings)
