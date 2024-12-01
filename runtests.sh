#!/bin/sh
set -e
pip install -r requirements-test.txt
flake8 schedule school_schedule
mypy schedule school_schedule
wait-for-it db:5432
pytest --reuse-db
