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
PAGE_ORDER_BY = "header_position"

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
    "markdown.extensions.admonition": {},
  },
  "output_format": "html5",
}

# Social widget
SOCIAL = (
    ("LinkedIn", "https://linkedin.com/in/sebastien-lesaint/", "Linkedin profile"),
    ("Github", "https://github.com/lesaint/", "Personal Github"),
    ("Github", "https://github.com/sns-seb/", "Public Github at SonarSource"),
)

##########################
# Search engine indexing #
##########################
STATIC_PATHS.append("extra/robots.txt")
EXTRA_PATH_METADATA["extra/robots.txt"] = {"path": "robots.txt"}

STATIC_PATHS.append("extra/google_property_verification_file")
EXTRA_PATH_METADATA["extra/google_property_verification_file"] = {"path": "googled2a1d235c02ddb0d.html"}

PLUGINS.append("extended_sitemap")
EXTENDED_SITEMAP_PLUGIN = {
    'priorities': {
        'index': 1.0,
        'articles': 0.8,
        'pages': 0.9,
        'others': 0.4
    },
    'changefrequencies': {
        'index': 'daily',
        'articles': 'weekly',
        'pages': 'monthly',
        'others': 'monthly',
    }
}

##################################
# Elegant theme related settings #
##################################
THEME = "theme-elegant"

# no search with local
SEARCH_URL = ""
LANDING_PAGE_TITLE = "Sébastien Lesaint"
PROJECTS = [
    {
        "title": "Active projects",
        "lines": [
            {
                "name": "PyLMS",
                "url": "https://github.com/lesaint/pylms",
                "description": "A tool to remind me of people's names and relationships, also serving as a learning "
                               "and demonstration project."
            },
            {
                "name": "Phanas Desktop",
                "url": "https://github.com/lesaint/phanas_desktop",
                "description": "The Python-based GUI program acting as the client application for my home backup"
                               " strategy across desktop devices"
            },
            {
                "name": "rsync-time-backup",
                "url": "https://github.com/lesaint/rsync-time-backup",
                "description": "The backbone on my home backup strategy. Notably adapted the bash script to very "
                               "limited Busybox-backed linux commands"
            },
        ]
    },
    {
        "title": "Completed projects",
        "lines": [
            {
                "name": "Public-Git-Sync",
                "url": "https://github.com/lesaint/public-git-sync",
                "description": "Created a tool at SonarSource, 100% based on hardcore Git and bash, to synchronize "
                               "public code of a branch in a private repository to a branch in a public repository"
            },
            {
                "name": "Jirac",
                "url": "https://github.com/jirac/jirac",
                "description": "Command line Bash utility to generate Jira comments from Git commits on a Maven project"
            },
            {
                "name": 'Hands-on: Annotation Processing @Nailed("it")',
                "url": "https://github.com/fbiville/annotation-processing-ftw?tab=readme-ov-file#annotation-processing-nailedit",
                "description": 'Created and animated a Hands-On lab at Devoxx FR in 2015 with <a href="https://github.com/fbiville" target="_blank">Florent Biville</a>'
            },
        ]
    },
    {
        "title": "Abandoned projects",
        "lines": [
            {
                "name": "DAMapping",
                "url": "https://www.javatronic.fr/damapping/presentations/damapping_why_and_how.html#/",
                "description": "A stack of components to implement object mapping in Java with complete source "
                               "control for the developer | Abandoned because of exhaustion of time and interest due "
                               "to starting an intense job"
            },
        ]
    },
]
