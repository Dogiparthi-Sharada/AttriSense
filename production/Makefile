# AttriSense production Makefile.
# Run from anywhere via: `make -C production <target>`

.PHONY: help install data train uplift fairness eval test lint format run docker clean

PYTHON := ../.venv/bin/python
PIP    := ../.venv/bin/pip
STREAMLIT := ../.venv/bin/streamlit
PORT   ?= 8520

help:  ## Show this help.
	@grep -E '^[a-zA-Z_-]+:.*## ' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  %-12s %s\n", $$1, $$2}'

install:  ## Install runtime + dev dependencies into ../.venv.
	$(PIP) install -e ".[causal,dev]"

data:  ## Regenerate the synthetic workforce CSV.
	cd .. && $(PYTHON) generate_demo_workforce_data.py

train:  ## Train the model and write predictions to SQLite.
	cd .. && $(PYTHON) train_retention_risk_model.py

uplift:  ## Compute the causal uplift recommendation table.
	cd .. && PYTHONPATH=production/src $(PYTHON) -m attrisense.causal_uplift

fairness:  ## Run the fairness audit and write outputs/fairness_report.json.
	cd .. && PYTHONPATH=production/src $(PYTHON) -m attrisense.fairness

eval:  ## Run the NL→SQL evaluation harness against the gold set.
	cd .. && PYTHONPATH=production/src $(PYTHON) -m attrisense.nl_sql_eval

test:  ## Run pytest with the production conftest path.
	cd .. && PYTHONPATH=production/src:. $(PYTHON) -m pytest production/tests -ra -q

lint:  ## Run ruff lint over the production source and tests.
	cd .. && $(PYTHON) -m ruff check production/src production/tests

format:  ## Auto-format production source with black + ruff fixers.
	cd .. && $(PYTHON) -m black production/src production/tests
	cd .. && $(PYTHON) -m ruff check --fix production/src production/tests

run:  ## Launch the production Streamlit dashboard. Override port with PORT=NNNN.
	cd .. && PYTHONPATH=production/src:. $(STREAMLIT) run production/streamlit_app.py \
	    --server.address=0.0.0.0 --server.port=$(PORT) --server.headless=true \
	    --browser.gatherUsageStats=false

docker:  ## Build the production Docker image.
	cd .. && docker build -f production/Dockerfile -t attrisense:latest .

clean:  ## Remove generated outputs and caches.
	cd .. && rm -rf outputs/fairness_report.json outputs/nl_sql_eval_report.json __pycache__ \
	    production/src/attrisense/__pycache__ production/tests/__pycache__ .pytest_cache
