title: Migrating from Jekyll to Pelican
tags: Pelican, Javatronic


# Boostrap

Setup project directory:

```shell
python3 -m venv .venv
echo "pelican[markdown]" > requirements.txt
source .venv/bin/activate
pip install -r requirements.txt
pelican-quickstart
```

Options for quickstart configuration:

```
> Where do you want to create your new web site? [.] 
> What will be the title of this web site? Javatronic
> Who will be the author of this web site? Sébastien Lesaint
> What will be the default language of this web site? [fr] en
> What is your URL prefix? (see above example; no trailing slash) https://www.javatronic.fr
> Do you want to enable article pagination? (Y/n) y
> How many articles per page do you want? [10] 10
> What is your time zone? [Europe/Rome] Europe/Paris
> Do you want to generate a tasks.py/Makefile to automate generation and publishing? (Y/n) y
> Do you want to upload your website using FTP? (y/N) n
> Do you want to upload your website using SSH? (y/N) n
> Do you want to upload your website using Dropbox? (y/N) n
> Do you want to upload your website using S3? (y/N) n
> Do you want to upload your website using Rackspace Cloud Files? (y/N) n
> Do you want to upload your website using GitHub Pages? (y/N) y
> Is this your personal page (username.github.io)? (y/N) y
```

> source: https://docs.getpelican.com/en/latest/quickstart.html


# Customize for markdown

Add the following to `pelicanconf.py`, which:

* Markdown support is enabled by installing `pelican[markdown]`
* Enable TOC extension to generate Table of Content where `[TOC]` is present in markdown
  * depth limited to 2
* Enable [Extra](https://python-markdown.github.io/extensions/extra/) extension for [Fenced Code Blocks](https://python-markdown.github.io/extensions/fenced_code_blocks/) and because the others can't hurt
* Enable [New Line To Break](https://python-markdown.github.io/extensions/nl2br/) and [Sane Lists](https://python-markdown.github.io/extensions/sane_lists/) because they just make sense
* Enable `pymdownx.superfences` extension
  * I need it to support code blocks within lists

```python
MARKDOWN = {
  'extension_configs': {
    'markdown.extensions.toc': {
      'title': 'Table of contents:',
      'toc_depth': 2
    },
    'markdown.extensions.codehilite': {'css_class': 'highlight'},
    'markdown.extensions.extra': {},
    'markdown.extensions.meta': {},
    'markdown.extensions.sane_lists': {},
    'markdown.extensions.nl2br': {},
    'pymdownx.superfences': {},
  },
  'output_format': 'html5',
}
```

> sources:
>
>  * [Pelican's documentation for setting `MARKDOWN`](https://docs.getpelican.com/en/stable/settings.html#basic-settings)
>  * [Python Markdown built-in extensions](https://python-markdown.github.io/extensions/)
>  * [Documentation of superfences](https://facelessuser.github.io/pymdown-extensions/extensions/superfences/)
>  * [Installation of PyMDown Extensions](https://facelessuser.github.io/pymdown-extensions/installation/) superfences is a part of

# Migrating markdown files content

The following content in markdown must be changed.

## metadata
* syntax is different
* some items do not exist in Pelican: `layout`, `image`, `comments`, `share`, `redirect_from`
* `category` metadata can be dropped as we will use directories instead of metadata
* `description` metadata can be renamed to `summary`
* content of `tags` metadata must be converted to a comma-separated list
* `"` (quotes) must be removed from `title` metadata

## Table of content

* syntax is different: `{:toc}` must be replaced by `[TOC]`
* title `* Table of Contents` can be removed as  it is inserted by the markdown plugin

## code blocks

* syntax is different: `{% highlight foo}` replaced by `` ```foo `` and `{% endhighlight %}` replaced by `` ``` ``

## links

* syntax for internal links is different: from `[foo]({% posturl bar %})` to `[foo]({filename}bar)`
    * `articles/bar` must become `/articles/bar.md` if current file is not in the `articles` category (aka. root relative)
    * otherwise, it can become `bar.md` (aka. file relative)
    * for simplicity, we will use root relative everywhere
* syntax for links to resources is different and resources have a different location
    * `{{ site.url }}/resourcs/foo.png` must become `{static}/images/foo.png`
    * (resources could also be "attached" but, so far, I haven't seen the use case, so I'll keep to `{static}`)

> sources:
> 
> * [Pelican's doc on linking to internal content](https://docs.getpelican.com/en/latest/content.html#linking-to-internal-content)
> * [Pelican's doc on linking resources](https://docs.getpelican.com/en/latest/content.html#linking-to-static-files)

# Manual migration attempt

* find all code block types
```shell
grep --no-filename "{% highlight" *.md | xargs -L1 echo | sort | uniq
```
* replace opening blocks
```shell
sed -i "s/{% highlight sh %}/\`\`\`shell/g" *.md 
sed -i "s/{% highlight java %}/\`\`\`java/g" *.md 
sed -i "s/{% highlight xml %}/\`\`\`xml/g" *.md 
sed -i "s/{% highlight json %}/\`\`\`json/g" *.md 
```
* replace closing blocks
```shell
sed -i "s/{% endhighlight %}/\`\`\`/g" *.md
```
* remove heading and trailing `---` of Jekyll header
```shell
sed -i "/^\-\-\-/d" *.md
```

Altering the metadata, including converting data on multiple lines to a single line, is too hard of a challenge to do
with bash. The tool is not appropriate. Let's switch to Python.

# Python-based migration

See [migrate_md.py](https://github.com/lesaint/jekyll_to_pelican_migration/blob/main/migrate_md.py) on Github.

Copy Markdown files to the Pelican's location, using a specific subdirectory just for the sake of 
segregating old migrated posts from new ones, and run the script on them:

```shell
mkdir -p content/from_jekyll/articles
cp _posts/articles/*.md content/articles/
mkdir -p content/from_jekyll/tips
cp _posts/tips/*.md content/articles/
```

```shell
git clone git@github.com:lesaint/jekyll_to_pelican_migration.git ../jekyll_to_pelican_migration
(cd content/articles && ../../../jekyll_to_pelican_migration/migrate_md.py *.md)
(cd content/tips && ../../../jekyll_to_pelican_migration/migrate_md.py *.md)
```

Copy images files of posts to Pelican's location

```shell
cp -r resources/how_to_debug_an_annotation_processor content/images/
```

If rendering of Markdown files is now ok, remove `.md.backup` files:

```shell
rm content/*/*.md.backup
```
