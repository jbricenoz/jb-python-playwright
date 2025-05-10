from playwright.sync_api import Page

class OrdersReturnsPage:
    """Component representing the Orders and Returns page"""
    
    def __init__(self, page: Page):
        self.page = page
        
        # Page title
        self.page_title = page.locator('.page-title span.base')
        
        # Form
        self.form = page.locator('#oar-widget-orders-and-returns-form')
        
        # Order Information fields
        self.order_id_input = page.locator('#oar-order-id')
        self.billing_lastname_input = page.locator('#oar-billing-lastname')
        self.find_order_by_select = page.locator('#quick-search-type-id')
        
        # Email field (visible by default)
        self.email_field = page.locator('#oar-email')
        self.email_input = page.locator('#oar_email')
        
        # ZIP code field (hidden by default)
        self.zip_field = page.locator('#oar-zip')
        self.zip_input = page.locator('#oar_zip')
        
        # Submit button
        self.continue_button = page.locator('button.action.submit.primary')
        
        # Error messages
        self.error_message = page.locator('.message-error')
        
        # Order Details Page Elements
        self.order_number = page.locator('.page-title span.base')
        self.order_status = page.locator('.order-status')
        self.order_date = page.locator('.order-date span:not(.label)')
        self.reorder_button = page.locator('.action.order')
        self.print_order_button = page.locator('.action.print')
        
        # Order Items Table
        self.order_items_table = page.locator('#my-orders-table')
        self.product_names = page.locator('.product.name.product-item-name')
        
        # Shipping and Billing Information
        self.shipping_address = page.locator('.box.box-order-shipping-address .box-content')
        self.billing_address = page.locator('.box.box-order-billing-address .box-content')
        self.shipping_method = page.locator('.box.box-order-shipping-method .box-content')
        self.payment_method = page.locator('.box.box-order-billing-method .box-content')
        
        # Order Totals
        self.subtotal = page.locator('tr.subtotal .amount .price')
        self.shipping_total = page.locator('tr.shipping .amount .price')
        self.grand_total = page.locator('tr.grand_total .amount .price')
        
    def navigate(self):
        """Navigate to the Orders and Returns page"""
        self.page.goto('https://magento.softwaretestingboard.com/sales/guest/form/')
        self.page.wait_for_load_state('networkidle')
        
    def is_page_loaded(self):
        """Check if the Orders and Returns page is loaded"""
        return self.page_title.is_visible() and self.page_title.text_content() == "Orders and Returns"
        
    def select_find_order_by(self, option: str):
        """Select an option from the 'Find Order By' dropdown
        
        Args:
            option: Either 'email' or 'zip'
        """
        self.find_order_by_select.select_option(option)
        
        # Wait for the appropriate field to be visible
        if option == 'email':
            self.email_field.wait_for(state='visible')
        elif option == 'zip':
            self.zip_field.wait_for(state='visible')
            
    def fill_order_details(self, order_id: str, billing_lastname: str, email_or_zip: str, find_by: str = 'email'):
        """Fill in the order details form
        
        Args:
            order_id: The order ID
            billing_lastname: The billing last name
            email_or_zip: Either the email or ZIP code, depending on find_by
            find_by: Either 'email' or 'zip'
        """
        self.order_id_input.fill(order_id)
        self.billing_lastname_input.fill(billing_lastname)
        self.select_find_order_by(find_by)
        
        if find_by == 'email':
            self.email_input.fill(email_or_zip)
        elif find_by == 'zip':
            self.zip_input.fill(email_or_zip)
            
    def submit_form(self):
        """Submit the form"""
        self.continue_button.click()
        self.page.wait_for_load_state('networkidle')
        
    def search_order(self, order_id: str, billing_lastname: str, email_or_zip: str, find_by: str = 'email'):
        """Search for an order
        
        Args:
            order_id: The order ID
            billing_lastname: The billing last name
            email_or_zip: Either the email or ZIP code, depending on find_by
            find_by: Either 'email' or 'zip'
        """
        self.fill_order_details(order_id, billing_lastname, email_or_zip, find_by)
        self.submit_form()
        
    def has_error_message(self):
        """Check if there is an error message"""
        return self.error_message.is_visible()
        
    def get_error_message(self):
        """Get the error message text"""
        if self.has_error_message():
            return self.error_message.text_content()
        return None
        
    def is_order_details_page_displayed(self):
        """Check if the order details page is displayed"""
        # Check for key elements that should be present on the order details page
        return (
            self.order_number.is_visible() and
            self.order_status.is_visible() and
            self.order_items_table.is_visible()
        )
        
    def get_order_number(self):
        """Get the order number from the order details page"""
        if self.order_number.is_visible():
            # Extract just the order number from text like "Order # 000054232"
            text = self.order_number.text_content()
            if "#" in text:
                return text.split("#")[1].strip()
            return text
        return None
        
    def get_order_status(self):
        """Get the order status"""
        if self.order_status.is_visible():
            return self.order_status.text_content()
        return None
        
    def get_order_date(self):
        """Get the order date"""
        if self.order_date.is_visible():
            return self.order_date.text_content()
        return None
        
    def get_product_names(self):
        """Get the names of products in the order"""
        if self.product_names.count() > 0:
            return [name.text_content() for name in self.product_names.all()]
        return []
        
    def get_shipping_address(self):
        """Get the shipping address"""
        if self.shipping_address.is_visible():
            return self.shipping_address.text_content()
        return None
        
    def get_billing_address(self):
        """Get the billing address"""
        if self.billing_address.is_visible():
            return self.billing_address.text_content()
        return None
        
    def get_payment_method(self):
        """Get the payment method"""
        if self.payment_method.is_visible():
            return self.payment_method.text_content().strip()
        return None
        
    def get_order_total(self):
        """Get the grand total of the order"""
        if self.grand_total.is_visible():
            return self.grand_total.text_content()
        return None
        
    def verify_order_details(self, expected_order_id=None, expected_email=None):
        """Verify the order details match the expected values
        
        Args:
            expected_order_id: The expected order ID
            expected_email: The expected email address
            
        Returns:
            bool: True if the details match, False otherwise
        """
        # Check if we're on the order details page
        if not self.is_order_details_page_displayed():
            print("Order details page is not displayed")
            return False
            
        # Verify order ID if provided
        if expected_order_id:
            actual_order_id = self.get_order_number()
            print(f"Verifying order ID - Expected: {expected_order_id}, Actual: {actual_order_id}")
            if not actual_order_id:
                print("Order ID is not displayed")
                return False
            if expected_order_id not in actual_order_id:
                print(f"Order ID mismatch: expected {expected_order_id}, got {actual_order_id}")
                return False
        return True
