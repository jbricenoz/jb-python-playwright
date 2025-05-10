from playwright.sync_api import Page, Locator

class CheckoutPage:
    """Component representing the checkout page"""
    
    def __init__(self, page: Page):
        self.page = page
        
        # Page title and header
        self.page_title = page.locator('.page-title span.base')
        
        # Progress bar
        self.progress_bar = page.locator('.opc-progress-bar')
        self.progress_bar_items = page.locator('.opc-progress-bar-item')
        
        # Estimated total
        self.estimated_total_label = page.locator('.estimated-label')
        self.estimated_total_price = page.locator('.estimated-price')
        
        # Authentication
        self.authentication_wrapper = page.locator('.authentication-wrapper')
        self.sign_in_button = page.locator('.action-auth-toggle')
        self.login_email = page.locator('#login-email')
        self.login_password = page.locator('#login-password')
        self.login_button = page.locator('.action.action-login')
        self.forgot_password_link = page.locator('.action.action-remind')
        
        # Email section
        self.email_input = page.locator('#checkout-step-shipping #customer-email')
        self.email_tooltip = page.locator('#customer-email-fieldset .field-tooltip-content')
        
        # Shipping address form
        self.shipping_address_title = page.locator('#shipping .step-title')
        self.first_name_input = page.locator('input[name="firstname"]')
        self.last_name_input = page.locator('input[name="lastname"]')
        self.company_input = page.locator('input[name="company"]')
        self.street_input = page.locator('input[name="street[0]"]')
        self.street2_input = page.locator('input[name="street[1]"]')
        self.street3_input = page.locator('input[name="street[2]"]')
        self.city_input = page.locator('input[name="city"]')
        self.region_dropdown = page.locator('select[name="region_id"]')
        self.region_input = page.locator('input[name="region"]')
        self.zip_input = page.locator('input[name="postcode"]')
        self.country_dropdown = page.locator('select[name="country_id"]')
        self.phone_input = page.locator('input[name="telephone"]')
        self.phone_tooltip = page.locator('.field[name="shippingAddress.telephone"] .field-tooltip-content')
        
        # Shipping methods section
        self.shipping_methods_title = page.locator('#opc-shipping_method .step-title')
        self.shipping_methods_table = page.locator('.table-checkout-shipping-method')
        self.shipping_methods = page.locator('.table-checkout-shipping-method input[type="radio"]')
        self.shipping_method_flatrate = page.locator('input[value="flatrate_flatrate"]')
        self.shipping_method_tablerate = page.locator('input[value="tablerate_bestway"]')
        self.shipping_method_rows = page.locator('.table-checkout-shipping-method tbody tr.row')
        self.shipping_method_prices = page.locator('.table-checkout-shipping-method .col-price .price')
        
        # Next button in shipping methods
        self.next_button = page.locator('button.action.continue.primary')
        
        # Payment section
        self.payment_section = page.locator('#payment')
        self.payment_section_title = page.locator('#payment .step-title')
        self.payment_methods_list = page.locator('#checkout-payment-method-load')
        self.payment_methods = page.locator('.payment-method')
        self.payment_method_check = page.locator('#checkmo')
        self.payment_method_radio_buttons = page.locator('input[name="payment[method]"]')
        
        # Billing address section
        self.billing_address_same_as_shipping = page.locator('input[id^="billing-address-same-as-shipping"]')
        self.billing_address_details = page.locator('.billing-address-details')
        self.billing_address_edit_button = page.locator('.action.action-edit-address')
        
        # Discount code section
        self.discount_code_section = page.locator('.payment-option.discount-code')
        self.discount_code_toggle = page.locator('#block-discount-heading')
        self.discount_code_input = page.locator('#discount-code')
        self.apply_discount_button = page.locator('.action.action-apply')
        
        # Order summary
        self.order_summary = page.locator('.opc-block-summary')
        self.order_summary_title = page.locator('.opc-block-summary .title')
        self.items_in_cart = page.locator('.block.items-in-cart')
        self.cart_items = page.locator('.minicart-items .product-item')
        self.cart_item_options = page.locator('.product.options')
        self.cart_item_options_toggle = page.locator('.product.options .toggle')
        self.cart_item_price = page.locator('.subtotal .price')
        self.order_total = page.locator('.grand.totals .price')
        
        # Place order button
        self.place_order_button = page.locator('.action.primary.checkout')
        
        # Order success
        self.order_success_message = page.locator('.checkout-success')
        self.order_number = page.locator('.checkout-success p span')
        
    def fill_shipping_information(self, email: str, first_name: str, last_name: str, 
                                 street: str, city: str, region_id: str, 
                                 zip_code: str, country_id: str = 'US', phone: str = '1234567890'):
        """Fill in the shipping information form"""
        self.email_input.fill(email)
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.street_input.fill(street)
        self.city_input.fill(city)
        self.region_dropdown.select_option(region_id)
        self.zip_input.fill(zip_code)
        self.country_dropdown.select_option(country_id)
        self.phone_input.fill(phone)
        
    def select_shipping_method(self, method_index: int = 0):
        """Select a shipping method by index"""
        self.shipping_methods.nth(method_index).click()
        
    def proceed_to_payment(self):
        """Proceed to payment step"""
        self.next_button.click()
        # Wait for payment methods to be visible
        self.page.wait_for_selector('.payment-method', state='visible', timeout=10000)
        
    def select_payment_method(self, method_index: int = 0):
        """Select a payment method by index"""
        self.payment_method_radio_buttons.nth(method_index).click()
        
    def use_same_billing_address(self, same_as_shipping: bool = True):
        """Set whether billing address is same as shipping"""
        current_state = self.billing_address_same_as_shipping.is_checked()
        if current_state != same_as_shipping:
            self.billing_address_same_as_shipping.click()
            
    def apply_discount_code(self, code: str):
        """Apply a discount code"""
        self.discount_code_toggle.click()
        self.discount_code_input.fill(code)
        self.apply_discount_button.click()
        
    def get_order_total(self) -> str:
        """Get the order total amount"""
        return self.order_total.text_content().strip()
    
    def place_order(self):
        """Place the order"""
        self.place_order_button.click()
        # Wait for success message
        self.order_success_message.wait_for(state='visible', timeout=15000)
        
    def get_order_number(self) -> str:
        """Get the order number from success page"""
        return self.order_number.text_content().strip()
    
    def is_order_successful(self) -> bool:
        """Check if order was placed successfully"""
        return self.order_success_message.is_visible()
        
    def login_during_checkout(self, email: str, password: str):
        """Login during checkout process"""
        self.sign_in_button.click()
        self.login_email.fill(email)
        self.login_password.fill(password)
        self.login_button.click()
        # Wait for login to complete
        self.page.wait_for_load_state('networkidle')
