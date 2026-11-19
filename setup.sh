#!/usr/bin/env bash
set -e

echo "Setting up Playwright automation framework..."

[ ! -f .env ] && cp .env.example .env && echo "Created .env from .env.example"

python3 -m venv venv
source venv/bin/activate

pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

playwright install chromium
playwright install-deps chromium 2>/dev/null || true

mkdir -p reports screenshots traces

echo ""
echo "Setup complete. Activate the environment and run tests:"
echo ""
echo "  source venv/bin/activate"
echo "  pytest                          # run all tests"
echo "  pytest -k test_login            # run by name"
echo "  pytest -n auto                  # parallel execution"
echo "  playwright show-trace traces/<file>.zip   # inspect a trace"
