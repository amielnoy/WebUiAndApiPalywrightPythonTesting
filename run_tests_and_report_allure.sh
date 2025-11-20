#!/usr/bin/env bash
set -euo pipefail

RESULTS_DIR="allure-results"

echo "[INFO] Removing old allure results..."
rm -rf "$RESULTS_DIR"

echo "[INFO] Running pytest..."
pytest --alluredir="$RESULTS_DIR" "$@"

echo "[INFO] Serving Allure report..."
allure serve "$RESULTS_DIR"