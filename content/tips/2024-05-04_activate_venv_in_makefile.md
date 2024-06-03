title: Activate venv in Makefile
tags: python, makefile

I finally found a solution to have Python command use the venv of the project when calling them from Make.

## Use .ONESHELL and a macro

By default, make runs each line of a recipe in a different subshell. `.ONESHELL` makes make run a whole recipe in a single shell.

The alternative is to activate the venv with every single python command, eg.: `. venv/bin/activate && pip install -r requirements.txt`.

```makefile
.ONESHELL:
VENV_DIR=.venv
ACTIVATE_VENV:=. $(VENV_DIR)/bin/activate

install: 
    python3 -m venv "$(VENV_DIR)"
	$(ACTIVATE_VENV)
	pip install --upgrade --requirement requirements.txt

run: install
    $(ACTIVATE_VENV)
    python foo.my
```

> sources:
> 
> * stackoverflow: [effect and usage of .ONESHELL](https://stackoverflow.com/a/55404948)
> * stackoverflow: [using a macro to factor activation code](https://stackoverflow.com/a/73837995)

## Tracking requirements.txt changes

The above can be combined with appropriate makefile usage as to prime venv only once, and then track changes to `requirements.txt`.

```makefile
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
```

> source: stackoverflow: [using a touch file](https://stackoverflow.com/a/46188210)