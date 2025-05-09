from playwright.sync_api import Page

class HeaderContent:
    def __init__(self, page: Page):
        self.page = page
        # Hamburger/toggle nav
        self.toggle_nav = page.locator('span.action.nav-toggle')
        # Logo
        self.logo_link = page.locator('a.logo')
        self.logo_img = page.locator('a.logo img')
        # Minicart
        self.minicart_wrapper = page.locator('div.minicart-wrapper')
        self.cart_link = page.locator('a.action.showcart')
        self.cart_text = page.locator('a.action.showcart .text')
        self.cart_counter = page.locator('a.action.showcart .counter.qty')
        # Minicart dialog
        self.minicart_dialog = page.locator('div.mage-dropdown-dialog')
        self.minicart_close_btn = page.locator('button#btn-minicart-close')
        self.minicart_empty_msg = page.locator('strong.subtitle.empty')
        # Search
        self.search_form = page.locator('form#search_mini_form')
        self.search_input = page.locator('input#search')
        self.search_button = page.locator('button.action.search')
        self.advanced_search_link = page.locator('a.action.advanced')
        # Compare products
        self.compare_products_link = page.locator('a.action.compare')
        self.compare_products_counter = page.locator('a.action.compare .counter.qty')

    def click_toggle_nav(self):
        self.toggle_nav.click()

    def click_logo(self):
        self.logo_link.click()

    def open_cart(self):
        self.cart_link.click()
        self.page.wait_for_selector('div.mage-dropdown-dialog', state='visible')

    def close_cart(self):
        self.minicart_close_btn.click()
        self.page.wait_for_selector('div.mage-dropdown-dialog', state='hidden')

    def search(self, query: str):
        self.search_input.fill(query)
        self.search_button.click()
        self.page.wait_for_load_state('networkidle')

    def open_advanced_search(self):
        self.advanced_search_link.click()

    def is_cart_empty(self):
        return self.minicart_empty_msg.is_visible()

    def get_cart_counter(self):
        if self.cart_counter.is_visible():
            return self.cart_counter.inner_text()
        return None

    def get_compare_counter(self):
        if self.compare_products_counter.is_visible():
            return self.compare_products_counter.inner_text()
        return None
