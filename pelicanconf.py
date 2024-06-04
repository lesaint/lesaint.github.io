AUTHOR = "Sébastien Lesaint"
SITENAME = "Javatronic"
SITEURL = ""

PATH = "content"

TIMEZONE = "Europe/Paris"

DEFAULT_LANG = "en"

PLUGIN_PATHS = [
    "plugins"
]
PLUGINS = [
    "extract_toc"
]

# dynamic resources
ARTICLE_URL = "posts/{date:%Y}/{date:%m}/{date:%d}/{slug}/"
ARTICLE_SAVE_AS = "posts/{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html"
PAGE_URL = "pages/{slug}/"
PAGE_SAVE_AS = "pages/{slug}/index.html"

# static resources
DAMAPPING_DIR = "doc/damapping"
STATIC_PATHS = [
    "images",
    DAMAPPING_DIR,
    "extra/favicon.ico",
    "extra/CNAME",
    "extra/.nojekyll",
]
EXTRA_PATH_METADATA = {
    "extra/favicon.ico": {"path": "favicon.ico"},
    "extra/CNAME": {"path": "CNAME"},
    "extra/.nojekyll": {"path": ".nojekyll"},
}
ARTICLE_EXCLUDES = [
    DAMAPPING_DIR
]

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

MARKDOWN = {
  "extension_configs": {
    "markdown.extensions.toc": {
        "permalink": "true"
    },
    "markdown.extensions.codehilite": {"css_class": "highlight"},
    "markdown.extensions.extra": {},
    "markdown.extensions.meta": {},
    "markdown.extensions.sane_lists": {},
    "pymdownx.superfences": {},
  },
  "output_format": "html5",
}

# Social widget
SOCIAL = (
    ("LinkedIn", "https://linkedin.com/in/sebastien-lesaint/", "Linkedin profile"),
    ("Github", "https://github.com/lesaint/", "Personal Github"),
    ("Github", "https://github.com/sns-seb/", "Public Github at SonarSource"),
)

##################################
# Elegant theme related settings #
##################################
THEME = "theme-elegant"

# no search with local
SEARCH_URL = ""
LANDING_PAGE_TITLE = "Sébastien Lesaint"
PROJECTS_TITLE = "Active projects"
PROJECTS = [
    {
        "name": "PyLMS",
        "url": "https://github.com/lesaint/pylms",
        "description": "A demo, yet useful, project for Python development, software engineering best practices, "
                       "software and cloud architecting, and technology learning"
    },
    {
        "name": "Phanas Desktop",
        "url": "https://github.com/lesaint/phanas_desktop",
        "description": "The Python-based GUI program acting as the client app for my home backup strategy "
                       "across desktop devices at home"
    },
    {
        "name": "rsync-time-backup",
        "url": "https://github.com/lesaint/rsync-time-backup",
        "description": "The backbone on my home backup strategy. Notably adapted the bash script to very "
                       "limited Busybox-backed linux commands"
    },
]
