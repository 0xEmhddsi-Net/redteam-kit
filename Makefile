.PHONY: install fast context recon full offline report lint clean

PY ?= python

install:
	$(PY) -m pip install -r requirements.txt
	$(PY) -m pip install ruff

lint:
	ruff check .
	ruff format --check .

fast:
	$(PY) tests/json_injection.py $(ARGS)
	$(PY) tests/csv_injection.py $(ARGS)
	$(PY) tests/ansi_conceal.py $(ARGS)

context:
	$(PY) tests/canary_recall.py $(ARGS)

recon:
	$(PY) tests/slopsquat.py $(ARGS)

full: fast context recon
	$(MAKE) report

offline:
	DRK_FAKE=1 $(MAKE) fast

report:
	$(PY) -m harness.report

clean:
	rm -rf runs __pycache__ harness/__pycache__ tests/__pycache__ .ruff_cache
