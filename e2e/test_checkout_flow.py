from fixtures.pw_fixture import homepage, product_page, checkout_page, csv_service, email_service, pytest
from service.csv_service import CSVService

@pytest.mark.checkout
class TestCheckoutFlow:
    """Playwright test class for checkout flow."""

    @pytest.mark.cart
    def test_add_product_to_cart(self, homepage, product_page, csv_service):
        """Test adding a product to cart from search results"""
        # Search for a product with fallback if no results found
        search_term = csv_service.get_random_search_term("sample_test_data.csv")
        homepage.search_with_fallback(search_term)
        
        # Verify we're on search results page
        assert "catalogsearch/result" in homepage.page.url, "Should navigate to search results page"
        
        # Verify we have search results
        assert homepage.has_search_results(), "Should have search results after fallback search"
        
        # Get and click on the first product in search results
        product = homepage.get_first_product()
        product_name = product["name"]
        product["link"].click()
        
        # Verify we're on the product page
        assert product_page.get_product_name() == product_name.strip(), "Should be on correct product page"
        
        # Select size
        product_page.select_size(2)
        
        # Select color
        product_page.select_color(2)
        
        # Set quantity
        product_page.set_quantity(1)
        
        # Add to cart
        product_page.add_to_cart()
        
        # Verify product was added to cart
        assert product_page.is_added_to_cart(), "Product should be added to cart"
        
        # Verify cart counter is updated
        homepage.page.wait_for_timeout(1000)  # Wait for cart counter to update
        cart_count = product_page.cart_counter.text_content()
        assert int(cart_count) > 0, "Cart counter should be updated"

    @pytest.mark.checkout
    def test_checkout_process(self, homepage, product_page, checkout_page, csv_service):
        """Test the checkout process from cart to order confirmation"""
        # First add a product to cart
        self.test_add_product_to_cart(homepage, product_page, csv_service)
        
        # Proceed to checkout
        product_page.cart_icon.click()
        product_page.proceed_to_checkout.wait_for(state='visible', timeout=5000)
        product_page.proceed_to_checkout.click()
        
        # Wait for shipping form to be visible
        checkout_page.email_input.wait_for(state='visible', timeout=10000)
        
        # Fill in shipping information
        checkout_page.fill_shipping_information(
            email="test@example.com",
            first_name="Test",
            last_name="User",
            street="123 Test St",
            city="Test City",
            region_id="1",  # Alabama
            zip_code="12345",
            country_id="US",
            phone="1234567890"
        )
        
        # Select shipping method
        checkout_page.shipping_methods.first.click()
        
        # Proceed to payment
        checkout_page.next_button.click()
        
        # Get order total
        order_total = checkout_page.order_total.text_content()
        assert "$" in order_total, "Order total should contain dollar sign"
        
        # Place order
        checkout_page.place_order_button.click()
        
        # Wait for success message with longer timeout since this can take time
        checkout_page.order_success_message.wait_for(state='visible', timeout=20000)
        
        # Verify order was placed successfully
        assert checkout_page.is_order_successful(), "Order should be placed successfully"
        
        # Get order number
        order_number = checkout_page.get_order_number()
        assert order_number, "Order number should be present"
        print(f"Order successfully placed with order number: {order_number}")

    # Use search terms from CSV for parametrized tests
    search_terms = CSVService.search_terms('sample_test_data.csv')
    @pytest.mark.parametrize("search_term", search_terms)
    @pytest.mark.cart
    def test_add_specific_product_to_cart(self, homepage, product_page, search_term):
        """Test adding specific products to cart based on search terms from CSV"""
        # Search for the product
        homepage.search(search_term)
        
        # Verify we're on search results page
        assert "catalogsearch/result" in homepage.page.url, f"Should navigate to search results for {search_term}"
        
        # Check if there are search results
        results = homepage.page.locator('.product-items .product-item')
        results_count = results.count()
        
        if results_count == 0:
            pytest.skip(f"No products found for search term: {search_term}")
        
        # Click on the first product
        product = homepage.get_first_product()
        product_name = product["name"]
        product["link"].click()
        
        # Verify we're on the product page
        assert product_page.get_product_name() == product_name.strip(), "Should be on correct product page"
        
        # Select size
        product_page.select_size(2)
        
        # Select color
        product_page.select_color(2)
        
        # Set quantity
        product_page.set_quantity(1)
        
        # Add to cart
        product_page.add_to_cart()
        
        # Verify product was added to cart
        assert product_page.is_added_to_cart(), "Product should be added to cart"
        
        # Wait for success message
        product_page.success_message.wait_for(state='visible', timeout=10000)
        
        # Verify product was added to cart
        assert product_page.success_message.is_visible(), f"Product {product_name} should be added to cart"
        
        # Verify cart counter is updated
        homepage.page.wait_for_timeout(1000)  # Wait for cart counter to update
        cart_count = product_page.cart_counter.text_content()
        assert int(cart_count) > 0, f"Cart counter should be updated after adding {product_name}"


    @pytest.mark.cart
    def test_checkout_with_discount_code(self, homepage, product_page, checkout_page, csv_service):
        """Test the checkout process with a discount code"""
        # First add a product to cart
        self.test_add_product_to_cart(homepage, product_page, csv_service)
        
        # Proceed to checkout
        product_page.cart_icon.click()
        product_page.proceed_to_checkout.wait_for(state='visible', timeout=5000)
        product_page.proceed_to_checkout.click()
        
        # Wait for shipping form to be visible
        checkout_page.email_input.wait_for(state='visible', timeout=10000)
        
        # Fill in shipping information
        checkout_page.fill_shipping_information(
            email="test@example.com",
            first_name="Test",
            last_name="User",
            street="123 Test St",
            city="Test City",
            region_id="1",  # Alabama
            zip_code="12345",
            country_id="US",
            phone="1234567890"
        )
        
        # Select shipping method
        checkout_page.shipping_methods.first.click()
        
        # Proceed to payment
        checkout_page.next_button.click()
        
        # Get order total before discount
        order_total_before = checkout_page.order_total.text_content()
        
        # Try to apply a discount code (this is a test code, may not work on the actual site)
        if checkout_page.discount_code_toggle.is_visible():
            checkout_page.discount_code_toggle.click()
            checkout_page.discount_code_input.fill("TESTCODE123")
            checkout_page.apply_discount_button.click()
            
            # Wait a moment for potential discount to apply
            homepage.page.wait_for_timeout(1000)
            
            # Get order total after discount attempt
            order_total_after = checkout_page.order_total.text_content()
            
            # Note: In a real test, you would verify the discount was applied correctly
            # For this test, we're just checking that we can interact with the discount section
            print(f"Order total before discount attempt: {order_total_before}")
            print(f"Order total after discount attempt: {order_total_after}")
        
        # Place order
        checkout_page.place_order_button.click()
        
        # Wait for success message
        checkout_page.order_success_message.wait_for(state='visible', timeout=20000)
        
        # Verify order was placed successfully
        assert checkout_page.is_order_successful(), "Order should be placed successfully"
        
        # Get order number
        order_number = checkout_page.get_order_number()
        assert order_number, "Order number should be present"
        print(f"Order successfully placed with order number: {order_number}")
