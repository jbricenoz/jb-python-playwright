import pytest
from playwright.sync_api import sync_playwright
from components.home.homepage import HomePage
from components.product.product_page import ProductPage
from components.checkout.checkout_page import CheckoutPage
from components.orders.orders_returns import OrdersReturnsPage
from service.csv_service import CSVService
from service.email_service import EmailService

BROWSERS = ["chromium", "firefox", "webkit"]

# Parametrize browser_type so tests run in all browsers unless --browser is specified
@pytest.fixture(scope="session")
def browser_types(pytestconfig):
    cli_browser = pytestconfig.getoption("browser")
    if cli_browser and cli_browser in BROWSERS:
        return [cli_browser]
    return BROWSERS

@pytest.fixture(params=BROWSERS, scope="session")
def browser_type(request, browser_types):
    # Only parametrize over the selected browsers
    if request.param in browser_types:
        return request.param
    pytest.skip(f"Skipping {request.param} as it's not selected.")

@pytest.fixture
def page(browser_type):
    with sync_playwright() as p:
        browser = getattr(p, browser_type).launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        # page.wait_for_load_state("networkidle")
        yield page
        context.close()
        browser.close()

@pytest.fixture
def homepage(page, pytestconfig, autouse=True):
    base_url = pytestconfig.getoption('base_url') or pytestconfig.getini('base_url')
    if not base_url:
        raise RuntimeError("base_url is not set in pytest or playwright config.")
    page.goto(base_url)
    page.wait_for_timeout(1000)
    home = HomePage(page)
    return home

@pytest.fixture
def csv_service():
    return CSVService()

@pytest.fixture
def email_service():
    return EmailService()

@pytest.fixture
def product_page(homepage):
    return ProductPage(homepage.page)

@pytest.fixture
def checkout_page(homepage):
    return CheckoutPage(homepage.page)

@pytest.fixture
def orders_returns_page(homepage):
    return OrdersReturnsPage(homepage.page)

@pytest.fixture(autouse=True)
def before_and_after(page, email_service):
    # Before hook
    print("[Setup]")
    yield
    # After hook
    print("[Teardown]")
    email_service.send_report_email()

# You can add more project-wide fixtures here as needed.
