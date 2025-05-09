from playwright.sync_api import Page

class NavSections:
    def __init__(self, page: Page):
        self.page = page
        # Main container
        self.sections = page.locator('div.sections.nav-sections')
        self.section_items = page.locator('div.section-items.nav-sections-items')
        # Collapsible section titles
        self.section_titles = page.locator('div.section-item-title.nav-sections-item-title')
        self.menu_section_title = page.locator('div.section-item-title.nav-sections-item-title:has-text("Menu")')
        self.account_section_title = page.locator('div.section-item-title.nav-sections-item-title:has-text("Account")')
        # Section contents
        self.menu_section_content = page.locator(r'div.section-item-content#store\.menu')
        self.account_section_content = page.locator(r'div.section-item-content#store\.links')
        # Navigation (menu)
        self.navigation = page.locator('nav.navigation')
        # Only select the first/top-level menu list to avoid strict mode violation
        self.menu_list = page.locator('nav.navigation > ul.ui-menu').nth(0)
        self.menu_items = page.locator('nav.navigation > ul.ui-menu > li.level0')
        # Top-level menu links
        self.menu_links = page.locator('nav.navigation > ul.ui-menu > li.level0 > a')
        # Account links inside Account section
        self.account_links = page.locator('div#store\\.links ul.header.links a')

    def is_main_menu_visible(self):
        return self.menu_list.is_visible()

    def is_whats_new_visible(self):
        return self.page.get_by_role("menuitem", name="What's New").is_visible()

    def expand_menu_section(self):
        self.menu_section_title.click()

    def expand_account_section(self):
        self.account_section_title.click()

    def get_menu_items_text(self):
        return [item.inner_text() for item in self.menu_links.all()]

    def get_account_links_text(self):
        return [item.inner_text() for item in self.account_links.all()]

    def click_menu_link_by_text(self, text: str):
        self.page.locator(f'nav.navigation ul.ui-menu > li.level0 > a:has-text("{text}")').click()

    def click_account_link_by_text(self, text: str):
        self.page.locator(f'div#store\\.links ul.header.links a:has-text("{text}")').click()
