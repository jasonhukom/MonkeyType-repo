#!/usr/bin/env bash
# Creates a virtual environment (first run only), installs rich, and starts the typing test.
set -e
cd "$(dirname "$0")"

if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

.venv/bin/python -m pip install --quiet -r ../requirements.txt
exec .venv/bin/python speed-test.py
