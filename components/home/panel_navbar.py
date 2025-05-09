from playwright.sync_api import Page

class PanelNavbar:
    def __init__(self, page: Page):
        self.page = page
        # Locators matching the provided HTML structure
        self.skip_to_content = page.locator('a.action.skip.contentarea')
        self.greet = page.locator('li.greet.welcome')
        self.not_logged_in = page.locator('span.not-logged-in')
        self.authorization_link = page.locator('li.authorization-link')
        # Use a more specific selector to avoid strict mode violation
        self.sign_in = page.get_by_role("link", name="Sign In").first
        self.create_account = page.get_by_role("link", name="Create an Account")

    def is_skip_to_content_visible(self):
        return self.skip_to_content.is_visible()

    def is_greet_visible(self):
        return self.greet.is_visible()

    def is_not_logged_in_visible(self):
        return self.not_logged_in.is_visible()

    def is_authorization_link_visible(self):
        return self.authorization_link.is_visible()

    def is_sign_in_visible(self):
        return self.sign_in.is_visible()

    def is_create_account_visible(self):
        return self.create_account.is_visible()


