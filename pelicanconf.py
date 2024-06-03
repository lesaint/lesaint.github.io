AUTHOR = 'Sébastien Lesaint'
SITENAME = 'Javatronic'
SITEURL = ""

PATH = "content"

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = 'en'

# static resources
STATIC_PATHS = ['images', 'extra/CNAME']
EXTRA_PATH_METADATA = {
    'extra/CNAME': {'path': 'CNAME'},
}

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

THEME = "theme-elegant"

LANDING_PAGE_TITLE = "Sébastien Lesaint"
PROJECTS_TITLE = "Active projects"
PROJECTS = [
    {
        'name': 'PyLMS',
        'url': 'https://github.com/lesaint/pylms',
        'description': 'A demo, yet useful, project for Python development, software engineering best practices, '
                       'software and cloud architecting, and technology learning'
    },
    {
        'name': 'Phanas Desktop',
        'url': 'https://github.com/lesaint/phanas_desktop',
        'description': 'The Python-based GUI program acting as the client app for my home backup strategy '
                       'across desktop devices at home'
    },
    {
        'name': 'rsync-time-backup',
        'url': 'https://github.com/lesaint/rsync-time-backup',
        'description': 'The backbone on my home backup strategy. Notably adapted the bash script to very '
                       'limited Busybox-backed linux commands'
    },
]
