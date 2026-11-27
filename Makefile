.PHONY: install lint compile todo demo offline verify-negative fast context recon full report clean

PY ?= python
EXPECTED = json_injection csv_injection ansi_conceal canary_recall prompt_extraction slopsquat
FAST = tests/json_injection.py tests/csv_injection.py tests/ansi_conceal.py
ALL = $(FAST) tests/canary_recall.py tests/prompt_extraction.py tests/slopsquat.py

install:
	$(PY) -m pip install -r requirements.txt
	$(PY) -m pip install ruff

lint:
	ruff check .
	ruff format --check .

compile:
	$(PY) -m compileall -q harness tests

todo:
	@echo "not yet written:"
	@for t in $(EXPECTED); do [ -f tests/$$t.py ] || echo "  tests/$$t.py"; done

demo: compile
	@for t in $(FAST); do DRK_FAKE=1 $(PY) $$t $(ARGS) || exit $$?; done
	$(MAKE) report

offline: compile
	@for t in $(ALL); do DRK_FAKE=1 $(PY) $$t $(ARGS) || exit $$?; done

verify-negative: compile
	@for t in $(ALL); do status=0; DRK_FAKE=1 $(PY) $$t --bad-fake --report-dir reports/bad-fake || status=$$?; test $$status -eq 1 || exit 1; done

fast: compile
	@for t in $(FAST); do $(PY) $$t $(ARGS) || exit $$?; done

context:
	$(PY) tests/canary_recall.py $(ARGS)
	$(PY) tests/prompt_extraction.py $(ARGS)

recon:
	$(PY) tests/slopsquat.py $(ARGS)

full: fast context recon
	$(MAKE) report

report:
	$(PY) -m harness.report

clean:
	$(PY) -c "import shutil; from pathlib import Path; [shutil.rmtree(p, ignore_errors=True) for p in (Path('runs'), Path('__pycache__'), Path('harness/__pycache__'), Path('tests/__pycache__'), Path('.ruff_cache'))]"
