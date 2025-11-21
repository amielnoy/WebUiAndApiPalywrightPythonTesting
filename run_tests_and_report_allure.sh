#!/usr/bin/env bash
set -euo pipefail

RESULTS_DIR="allure-results"

echo "[INFO] Removing old allure results..."
if [[ "${CLEAR_ALLURE_RESULTS:-1}" == "1" ]]; then
  rm -rf "$RESULTS_DIR"
else
  echo "[INFO] Skipping cleanup of ${RESULTS_DIR} (CLEAR_ALLURE_RESULTS=${CLEAR_ALLURE_RESULTS:-0})"
fi

echo "[INFO] Running pytest..."
pytest --alluredir="$RESULTS_DIR" "$@"

if [[ "${SERVE_ALLURE:-1}" == "1" ]]; then
  echo "[INFO] Serving Allure report..."
  allure serve "$RESULTS_DIR"
else
  echo "[INFO] Skipping Allure serve (SERVE_ALLURE=${SERVE_ALLURE:-0}). You can run: allure serve ${RESULTS_DIR}"
fi
