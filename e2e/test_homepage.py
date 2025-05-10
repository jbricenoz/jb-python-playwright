from fixtures.pw_fixture import homepage, csv_service, email_service, pytest  # Import fixtures explicitly
# Uses pw_fixture.py fixtures: page, homepage, csv_service, email_service, pytest

@pytest.mark.homepage
@pytest.mark.smoke
class TestHomePage:
    """Playwright test class for homepage."""

    @pytest.mark.homepage    
    def test_homepage_title_and_nav_links(self, homepage):
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
