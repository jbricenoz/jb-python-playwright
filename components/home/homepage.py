from playwright.sync_api import Page
from .header_content import HeaderContent
from .nav_sections import NavSections
from .panel_navbar import PanelNavbar

class HomePage:

    def __init__(self, page: Page):
        self.page = page
        self.header_content = HeaderContent(page)
        self.nav_sections = NavSections(page)
        self.panel_navbar = PanelNavbar(page)

    # Proxy method for navigation menu visibility
    def is_nav_menu_visible(self):
        return self.nav_sections.is_main_menu_visible()

    def get_title(self):
        return self.page.title()

    def is_nav_menu_visible(self):
        return self.nav_sections.menu_list.is_visible()

    def is_cart_icon_visible(self):
        return self.header_content.cart_link.is_visible()

    def is_sign_in_visible(self):
        return self.panel_navbar.is_sign_in_visible()

    def is_create_account_visible(self):
        return self.panel_navbar.is_create_account_visible()

    def is_whats_new_visible(self):
        return self.nav_sections.is_whats_new_visible()

    def is_logo_visible(self):
        return self.header_content.logo_img.is_visible()

    # Example: proxying a method from a subcomponent
    def search(self, query: str):
        self.header_content.search(query)

    def get_menu_items_text(self):
        return self.nav_sections.get_menu_items_text()

    def get_account_links_text(self):
        return self.nav_sections.get_account_links_text()
