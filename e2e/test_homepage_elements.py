from fixtures.pw_fixture import homepage, csv_service, email_service, pytest  # Import fixtures explicitly
from service.csv_service import CSVService

class TestHomepageElements:
    """Playwright test class for homepage elements."""

    @pytest.mark.homepage
    @pytest.mark.smoke
    async def test_homepage_nav_menu_visible(self, homepage):
        assert await homepage.is_nav_menu_visible(), "Navigation menu should be visible"

    @pytest.mark.homepage
    @pytest.mark.smoke
    async def test_homepage_logo_visible(self, homepage):
        assert await homepage.is_logo_visible(), "Logo should be visible"

    @pytest.mark.homepage
    @pytest.mark.smoke
    async def test_homepage_cart_icon_visible(self, homepage):
        assert await homepage.is_cart_icon_visible(), "Cart icon should be visible"

    @pytest.mark.homepage
    @pytest.mark.smoke
    async def test_homepage_sign_in_visible(self, homepage):
        assert await homepage.is_sign_in_visible(), "Sign In link should be visible"

    @pytest.mark.homepage
    @pytest.mark.smoke
    async def test_homepage_create_account_visible(self, homepage):
        assert await homepage.is_create_account_visible(), "Create Account link should be visible"

    @pytest.mark.homepage
    @pytest.mark.smoke
    async def test_homepage_whats_new_visible(self, homepage):
        assert await homepage.is_whats_new_visible(), "What's New section should be visible"

    @pytest.mark.homepage
    @pytest.mark.smoke
    async def test_logo_visible(self, homepage):
        assert await homepage.is_logo_visible(), "Logo should be visible"

    @pytest.mark.homepage
    async def test_menu_items(self, homepage):
        menu_items = await homepage.get_menu_items_text()
        assert menu_items, "Menu items should not be empty"

    @pytest.mark.homepage
    async def test_account_links(self, homepage):
        account_links = await homepage.get_account_links_text()
        assert account_links, "Account links should not be empty"

    @pytest.mark.search
    @pytest.mark.parametrize("search_term", CSVService.search_terms('sample_test_data.csv'))
    def test_homepage_search(self, homepage, search_term):
        homepage.search(search_term)
        assert "search" in homepage.page.url or "result" in homepage.page.url, f"Should navigate to search results page for search term: {search_term}"
