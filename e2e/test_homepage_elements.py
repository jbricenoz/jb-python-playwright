import pytest
from fixtures.pw_fixture import homepage, csv_service, email_service  # Import fixtures explicitly
from service.csv_service import CSVService

@pytest.mark.homepage
@pytest.mark.smoke
def test_homepage_nav_menu_visible(homepage):
    assert homepage.is_nav_menu_visible(), "Navigation menu should be visible"

@pytest.mark.homepage
@pytest.mark.smoke
def test_homepage_logo_visible(homepage):
    assert homepage.is_logo_visible(), "Logo should be visible"

@pytest.mark.homepage
@pytest.mark.smoke
def test_homepage_cart_icon_visible(homepage):
    assert homepage.is_cart_icon_visible(), "Cart icon should be visible"

@pytest.mark.homepage
@pytest.mark.smoke
def test_homepage_sign_in_visible(homepage):
    assert homepage.is_sign_in_visible(), "Sign In link should be visible"

@pytest.mark.homepage
@pytest.mark.smoke
def test_homepage_create_account_visible(homepage):
    assert homepage.is_create_account_visible(), "Create Account link should be visible"

@pytest.mark.homepage
@pytest.mark.smoke
def test_homepage_whats_new_visible(homepage):
    assert homepage.is_whats_new_visible(), "What's New section should be visible"

@pytest.mark.homepage
@pytest.mark.smoke
def test_logo_visible(homepage):
    assert homepage.is_logo_visible(), "Logo should be visible"

@pytest.mark.homepage
def test_menu_items(homepage):
    menu_items = homepage.get_menu_items_text()
    assert menu_items, "Menu items should not be empty"

@pytest.mark.homepage
def test_account_links(homepage):
    account_links = homepage.get_account_links_text()
    assert account_links, "Account links should not be empty"


# Read all search terms from the CSV at collection time
search_data = CSVService.read_csv('sample_test_data.csv')
search_terms = [row['search_term'].strip() for row in search_data if row.get('search_term', '').strip()]
@pytest.mark.homepage
@pytest.mark.parametrize("search_term", search_terms)
def test_homepage_search(homepage, search_term):
    homepage.search(search_term)
    assert "search" in homepage.page.url or "result" in homepage.page.url, f"Should navigate to search results page for search term: {search_term}"
