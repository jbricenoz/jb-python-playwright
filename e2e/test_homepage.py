import pytest
from fixtures.pw_fixture import homepage, csv_service, email_service  # Import fixtures explicitly

# Uses pw_fixture.py fixtures: page, homepage

@pytest.mark.homepage
@pytest.mark.smoke
class TestHomePage:
    """Playwright test class for homepage."""
 
    @pytest.fixture(autouse=True)
    def before_and_after(self, page, email_service):
        # Before hook
        print("[Setup] Starting homepage test...")
        yield
        # After hook
        print("[Teardown] Finished homepage test.")
        email_service.send_report_email()

    @pytest.mark.homepage
    @pytest.mark.only    
    def test_homepage_title_and_nav_links(self, page, homepage):
        # Title check
        title = homepage.get_title()
        assert "Home Page" in title or "Magento" in title

        # Navigation menu links validation
        nav_links = homepage.nav_sections.get_menu_items_text()
        menu_links = homepage.nav_sections.menu_links.all()
        assert nav_links, "No navigation menu items found!"
        for link_el in menu_links:
            href = link_el.get_attribute("href")
            assert href, f"Menu link missing href: {link_el.inner_text()}"
            assert href.startswith("http"), f"Broken menu link: {href}"

"""
How to run this test file:

# Run all homepage tests (with output)
pytest -v e2e/test_homepage.py

# Run only homepage tests with 'homepage' marker
pytest -m homepage e2e/test_homepage.py

# Run all smoke tests
pytest -m smoke

# To see print output, use:
pytest -s e2e/test_homepage.py

# Run with Playwright browser options (examples):
pytest e2e/test_homepage.py --browser=firefox --headless
pytest e2e/test_homepage.py --browser=webkit --trace=on --video=on
pytest e2e/test_homepage.py --workers=2 --retries=1
"""
