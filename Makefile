PY?=
PELICAN?=pelican
PELICANOPTS=

BASEDIR=$(CURDIR)
INPUTDIR=$(BASEDIR)/content
OUTPUTDIR=$(BASEDIR)/output
CONFFILE=$(BASEDIR)/pelicanconf.py
PUBLISHCONF=$(BASEDIR)/publishconf.py

GITHUB_PAGES_BRANCH=gh-pages

THEME_DIR:=theme-elegant
DAMAPPING_DIR:=content/doc/damapping
HEAD_DESCRIPTION:=$(shell git log -1 --pretty=format:"(%h) %s" HEAD | tr '"' "'")


DEBUG ?= 0
ifeq ($(DEBUG), 1)
	PELICANOPTS += -D
endif

RELATIVE ?= 0
ifeq ($(RELATIVE), 1)
	PELICANOPTS += --relative-urls
endif

SERVER ?= "0.0.0.0"

PORT ?= 0
ifneq ($(PORT), 0)
	PELICANOPTS += -p $(PORT)
endif


help:
	@echo 'Makefile for a pelican Web site                                           '
	@echo '                                                                          '
	@echo 'Usage:                                                                    '
	@echo '   make venv                           initialize venv                    '
	@echo '   make venvclean                      delete venv                        '
	@echo '   make html                           (re)generate the web site          '
	@echo '   make clean                          remove the generated files         '
	@echo '   make regenerate                     regenerate files upon modification '
	@echo '   make publish                        generate using production settings '
	@echo '   make serve [PORT=8000]              serve site at http://localhost:8000'
	@echo '   make serve-global [SERVER=0.0.0.0]  serve (as root) to $(SERVER):80    '
	@echo '   make devserver [PORT=8000]          serve and regenerate together      '
	@echo '   make devserver-global               regenerate and serve on 0.0.0.0    '
	@echo '   make github                         upload the web site via gh-pages   '
	@echo '                                                                          '
	@echo 'Set the DEBUG variable to 1 to enable debugging, e.g. make DEBUG=1 html   '
	@echo 'Set the RELATIVE variable to 1 to enable relative urls                    '
	@echo '                                                                          '


# use .ONESHELL to activate venv and use it across a recipe without adding it before each command (source: https://stackoverflow.com/a/55404948)
.ONESHELL:
VENV_DIR=.venv
# source: https://stackoverflow.com/a/73837995
ACTIVATE_VENV:=. $(VENV_DIR)/bin/activate

$(VENV_DIR)/touchfile: requirements.txt
	test -d "$(VENV_DIR)" || python3 -m venv "$(VENV_DIR)"
	$(ACTIVATE_VENV)
	pip install --upgrade --requirement requirements.txt
	touch "$(VENV_DIR)/touchfile"

venv: $(VENV_DIR)/touchfile

venvclean:
	rm -rf $(VENV_DIR)

$(THEME_DIR)/README.md:
	test -d "$(THEME_DIR)" || git clone --depth 1 https://github.com/lesaint/pelicant-theme-elegant "$(THEME_DIR)"

eleganttheme: $(THEME_DIR)/README.md

$(DAMAPPING_DIR)/index.html:
	test -d "$(DAMAPPING_DIR)" || git clone --depth 1 --branch "gh-pages" --single-branch https://github.com/lesaint/damapping.git "$(DAMAPPING_DIR)" && rm -Rf "$(DAMAPPING_DIR)/.git"

damapping: $(DAMAPPING_DIR)/index.html

html: venv eleganttheme damapping
	$(ACTIVATE_VENV)
	"$(PELICAN)" "$(INPUTDIR)" -o "$(OUTPUTDIR)" -s "$(CONFFILE)" $(PELICANOPTS)

clean: venv
	[ ! -d "$(OUTPUTDIR)" ] || rm -rf "$(OUTPUTDIR)"

regenerate: venv eleganttheme damapping
	$(ACTIVATE_VENV)
	"$(PELICAN)" -r "$(INPUTDIR)" -o "$(OUTPUTDIR)" -s "$(CONFFILE)" $(PELICANOPTS)

serve: venv eleganttheme damapping
	$(ACTIVATE_VENV)
	"$(PELICAN)" -l "$(INPUTDIR)" -o "$(OUTPUTDIR)" -s "$(CONFFILE)" $(PELICANOPTS)

serve-global: venv eleganttheme damapping
	$(ACTIVATE_VENV)
	"$(PELICAN)" -l "$(INPUTDIR)" -o "$(OUTPUTDIR)" -s "$(CONFFILE)" $(PELICANOPTS) -b $(SERVER)

devserver: venv eleganttheme damapping
	$(ACTIVATE_VENV)
	"$(PELICAN)" -lr "$(INPUTDIR)" -o "$(OUTPUTDIR)" -s "$(CONFFILE)" $(PELICANOPTS)

devserver-global: venv eleganttheme damapping
	$(ACTIVATE_VENV)
	"$(PELICAN)" -lr "$(INPUTDIR)" -o "$(OUTPUTDIR)" -s "$(CONFFILE)" $(PELICANOPTS) -b 0.0.0.0

publish: venv eleganttheme damapping
	$(ACTIVATE_VENV)
	"$(PELICAN)" "$(INPUTDIR)" -o "$(OUTPUTDIR)" -s "$(PUBLISHCONF)" $(PELICANOPTS)

github: publish
	$(ACTIVATE_VENV)
	ghp-import -m "Publish: $(HEAD_DESCRIPTION)" -b "$(GITHUB_PAGES_BRANCH)" "$(OUTPUTDIR)"
	git push origin $(GITHUB_PAGES_BRANCH)


.PHONY: venv venvclean html help clean regenerate serve serve-global devserver devserver-global publish github