#!/usr/bin/env bash
set -euo pipefail

RESULTS_DIR="${RESULTS_DIR:-allure-results}"
REPORT_DIR="${REPORT_DIR:-allure-report}"
PYTEST_ARGS=${PYTEST_ARGS:-""}

# OPEN_REPORT: 1 = open after generate, 0 = don't open
OPEN_REPORT="${OPEN_REPORT:-1}"

# OPEN_METHOD:
#   auto   -> try "allure open" then OS opener (default)
#   serve  -> use "allure serve" (temp server)
#   static -> open the generated index.html directly
OPEN_METHOD="${OPEN_METHOD:-auto}"

# 1) Clean previous results/report
rm -rf "$RESULTS_DIR" "$REPORT_DIR"

# 2) Run tests to collect new Allure results
pytest -n auto --alluredir="$RESULTS_DIR" ${PYTEST_ARGS}

# 3) Generate Allure report (static files)
allure generate "$RESULTS_DIR" -o "$REPORT_DIR" --clean

## 4) Open the report as requested
#allure serve