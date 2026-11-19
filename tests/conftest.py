import pytest
import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
from src.config.config import Config
from src.pages.login_page import LoginPage
from src.pages.home_page import HomePage

SCREENSHOTS_DIR = Path("screenshots")
TRACES_DIR = Path("traces")


def _launch_browser(playwright):
    browser_type = getattr(playwright, Config.BROWSER)
    return browser_type.launch(
        headless=Config.HEADLESS,
        slow_mo=Config.SLOW_MO,
    )


# ── Session-scoped browser (shared across all tests) ─────────────────────────

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = _launch_browser(p)
        yield browser
        browser.close()


# ── Function-scoped page — fresh context per test (recommended default) ───────

@pytest.fixture(scope="function")
def page(browser: Browser):
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    if Config.TRACE_ON_FAIL:
        context.tracing.start(screenshots=True, snapshots=True, sources=True)
    pg = context.new_page()
    yield pg
    pg.close()
    context.close()


# ── Class-scoped page — one context shared within a test class ────────────────

@pytest.fixture(scope="class")
def class_page(browser: Browser):
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    if Config.TRACE_ON_FAIL:
        context.tracing.start(screenshots=True, snapshots=True, sources=True)
    pg = context.new_page()
    yield pg
    pg.close()
    context.close()


# ── Page object fixtures ──────────────────────────────────────────────────────

@pytest.fixture(scope="function")
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)


@pytest.fixture(scope="function")
def home_page(page: Page) -> HomePage:
    return HomePage(page)


# ── Failure hooks: screenshot + trace ─────────────────────────────────────────

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        test_name = item.name.replace("/", "_")

        for fixture_name in ("page", "class_page"):
            pg: Page = item.funcargs.get(fixture_name)
            if pg is None:
                continue

            if Config.SCREENSHOT_ON_FAIL:
                SCREENSHOTS_DIR.mkdir(exist_ok=True)
                path = SCREENSHOTS_DIR / f"{test_name}_{ts}.png"
                pg.screenshot(path=str(path), full_page=True)
                print(f"\nScreenshot saved: {path}")

            if Config.TRACE_ON_FAIL:
                TRACES_DIR.mkdir(exist_ok=True)
                path = TRACES_DIR / f"{test_name}_{ts}.zip"
                pg.context.tracing.stop(path=str(path))
                print(f"Trace saved: {path} — open with: playwright show-trace {path}")
                return  # tracing already stopped

        # Stop tracing without saving if test passed (cleanup)
        for fixture_name in ("page", "class_page"):
            pg = item.funcargs.get(fixture_name)
            if pg and Config.TRACE_ON_FAIL:
                try:
                    pg.context.tracing.stop()
                except Exception:
                    pass
