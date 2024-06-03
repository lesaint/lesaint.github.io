AUTHOR = 'Sébastien Lesaint'
SITENAME = 'Javatronic'
SITEURL = ""

PATH = "content"

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

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

# Blogroll
LINKS = (
    ("Pelican", "https://getpelican.com/"),
    ("Python.org", "https://www.python.org/"),
    ("Jinja2", "https://palletsprojects.com/p/jinja/"),
    ("You can modify those links in your config file", "#"),
)

# Social widget
SOCIAL = (
    ("You can add links in your config file", "#"),
    ("Another social link", "#"),
)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True