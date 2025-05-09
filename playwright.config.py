import os
from pathlib import Path

# ===== Playwright Base Configs =====
BASE_URL = os.getenv("BASE_URL", "https://magento.softwaretestingboard.com/")
# Supported browsers: chromium (Chrome/Edge), firefox, webkit (Safari). IE11 is not natively supported by Playwright;
# for legacy/IE testing, use a cloud/grid provider or Selenium.
BROWSER = os.getenv("BROWSER", "chromium")  # chromium, chrome, firefox, webkit, safari, edge
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
TIMEOUT = int(os.getenv("PLAYWRIGHT_TIMEOUT", "30000"))  # ms
RETRIES = int(os.getenv("PLAYWRIGHT_RETRIES", "2"))  # test retries on failure
WORKERS = int(os.getenv("PLAYWRIGHT_WORKERS", "2"))  # parallel workers
TRACE = os.getenv("PLAYWRIGHT_TRACE", "off")  # on, off, retain-on-failure
VIDEO = os.getenv("PLAYWRIGHT_VIDEO", "off")  # on, off, retain-on-failure
SCREENSHOT = os.getenv("PLAYWRIGHT_SCREENSHOT", "only-on-failure")  # on, off, only-on-failure
SLOWMO = int(os.getenv("PLAYWRIGHT_SLOWMO", "0"))  # ms delay

# Directory paths
ROOT_DIR = Path(__file__).parent
DATA_DIR = ROOT_DIR / "data"
REPORTS_DIR = ROOT_DIR / "reports"
SCREENSHOTS_DIR = ROOT_DIR / "screenshots"

# ===== Pytest Plugin Options =====
def pytest_addoption(parser):
    parser.addoption("--base-url", action="store", default=BASE_URL, help="Base URL for tests")
    parser.addoption("--browser", action="store", default=BROWSER, help="Browser: chromium, chrome, firefox, webkit, safari, edge")
    parser.addoption("--headless", action="store_true", default=HEADLESS, help="Run browser in headless mode")
    parser.addoption("--headed", action="store_true", default=not HEADLESS, help="Run browser in headed mode")
    parser.addoption("--timeout", action="store", default=TIMEOUT, help="Test timeout in ms")
    parser.addoption("--retries", action="store", default=RETRIES, help="Number of retries for flaky tests")
    parser.addoption("--workers", action="store", default=WORKERS, help="Number of parallel workers")
    parser.addoption("--trace", action="store", default=TRACE, help="Trace mode: on, off, retain-on-failure")
    parser.addoption("--video", action="store", default=VIDEO, help="Video recording: on, off, retain-on-failure")
    parser.addoption("--screenshot", action="store", default=SCREENSHOT, help="Screenshot: on, off, only-on-failure")
    parser.addoption("--slowmo", action="store", default=SLOWMO, help="Slow down Playwright operations by ms")

# ===== Pytest Setup: Ensure Output Dirs Exist =====
def pytest_configure(config):
    for d in [REPORTS_DIR, SCREENSHOTS_DIR]:
        d.mkdir(parents=True, exist_ok=True)

# ===== Notes for Users =====
"""
Supported browsers:
- chromium (Chrome/Edge)
- chrome (alias for chromium)
- firefox
- webkit (Safari)
- edge (alias for chromium)
- safari (alias for webkit)
- IE11: Not natively supported. Use Selenium or cloud/grid services for legacy browser testing.

Other Playwright config options (set via env or CLI):
- PLAYWRIGHT_TIMEOUT: Default timeout for all actions (ms)
- PLAYWRIGHT_RETRIES: Number of retries for failed tests
- PLAYWRIGHT_WORKERS: Number of parallel test workers
- PLAYWRIGHT_TRACE: Collect traces (on, off, retain-on-failure)
- PLAYWRIGHT_VIDEO: Record video (on, off, retain-on-failure)
- PLAYWRIGHT_SCREENSHOT: Take screenshots (on, off, only-on-failure)
- PLAYWRIGHT_SLOWMO: Slow down Playwright operations (ms)

Example CLI usage:
pytest e2e/ --browser=firefox --headless --retries=1 --trace=on --video=on --timeout=60000
"""
