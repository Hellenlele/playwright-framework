# Playwright Automation Framework

A Python test automation framework built with Playwright and pytest. It uses Page Objects, reusable UI components, environment-based configuration, isolated browser contexts, parallel execution, screenshots, and Playwright traces.

## Project structure

```text
src/
  components/   Reusable UI components
  config/       Environment-based configuration
  pages/        Page Objects
tests/
  testcases/    UI test suites
  conftest.py   Browser, page, and reporting fixtures
```

## Setup

```bash
chmod +x setup.sh
./setup.sh
source venv/bin/activate
```

Alternatively, install the dependencies manually:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install chromium
cp .env.example .env
```

## Run tests

```bash
pytest
pytest -k test_login
pytest -n auto
```

Configuration is read from `.env`. Copy `.env.example` to `.env` and adjust the values locally. The `.env` file and generated test artifacts are intentionally excluded from Git.

To inspect a saved trace:

```bash
playwright show-trace traces/<trace-file>.zip
```
