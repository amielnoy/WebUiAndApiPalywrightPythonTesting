#!/usr/bin/env bash
set -euo pipefail

RESULTS_DIR="${RESULTS_DIR:-allure-results}"
REPORT_DIR="${REPORT_DIR:-allure-report}"
PYTEST_ARGS=${PYTEST_ARGS:-""}

# 1) Clean previous results/report
rm -rf "$RESULTS_DIR" "$REPORT_DIR"

# 2) Run tests to collect new Allure results
pytest --alluredir="$RESULTS_DIR" ${PYTEST_ARGS}

# 3) Generate Allure report
allure generate "$RESULTS_DIR" -o "$REPORT_DIR" --clean

# 4) Open the report
# Prefer 'allure open' when available; fall back to opening the HTML file.
if command -v allure >/dev/null 2>&1; then
  # This starts a local server and opens browser
  allure open "$REPORT_DIR"
else
  # Fallback: open the static HTML directly
  if command -v xdg-open >/dev/null 2>&1; then
    xdg-open "$REPORT_DIR/index.html" >/dev/null 2>&1 || true
  elif [[ "$OSTYPE" == "darwin"* ]]; then
    open "$REPORT_DIR/index.html" >/dev/null 2>&1 || true
  else
    echo "Open the report at: file://$(pwd)/$REPORT_DIR/index.html"
  fi
fi