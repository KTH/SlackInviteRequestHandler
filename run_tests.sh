#!/bin/sh

if [[ -z "${SKIP_INSTALL}" ]]; then
  echo "To skip install run: SKIP_INSTALL=True ./run_tests.sh"
  poetry install 
else
  echo "Skipping poetry install"
fi

SMTP_HOST=smtp.kth.se SMTP_USER=${SMTP_USER} SMTP_PASSWORD=${SMTP_PASSWORD} poetry run green -vv --run-coverage --failfast "tests.py"