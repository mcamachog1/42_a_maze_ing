VENV := venv
PYTHON := $(VENV)/bin/python3
PIP := $(VENV)/bin/pip
FLAKE8 := $(VENV)/bin/flake8
MYPY := $(VENV)/bin/mypy

install:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) a_maze_ing.py config.txt

debug:
	$(PYTHON) -m pdb a_maze_ing.py config.txt

lint:
	$(FLAKE8) . --exclude=venv,__pycache__
	$(MYPY) . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	$(FLAKE8) . --exclude=venv,__pycache__
	$(MYPY) . --strict

clean:
	rm -rf __pycache__ .mypy_cache
