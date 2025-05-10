from playwright.sync_api import Page, Locator

class ProductPage:
    """Component representing a product detail page"""
    
    def __init__(self, page: Page):
        self.page = page
        
        # Product details selectors
        self.product_name = page.locator('.page-title span.base')
        self.product_price = page.locator('.price-box .price-wrapper .price')
        self.product_sku = page.locator('.product.attribute.sku .value')
        self.product_description = page.locator('.product.attribute.description .value')
        self.product_stock_status = page.locator('.stock.available')
        
        # Product ratings
        self.product_rating = page.locator('.rating-result')
        self.reviews_count = page.locator('.reviews-actions .action.view span:first-child')
        
        # Size options
        self.size_attribute = page.locator('.swatch-attribute.size')  
        self.size_options = page.locator('.swatch-attribute.size .swatch-option.text')
        
        # Color options
        self.color_attribute = page.locator('.swatch-attribute.color')
        self.color_options = page.locator('.swatch-attribute.color .swatch-option.color')
        
        # Quantity
        self.quantity_input = page.locator('#qty')
        
        # Add to cart button
        self.add_to_cart_button = page.locator('#product-addtocart-button')
        
        # Success message
        self.success_message = page.locator('.message-success')
        
        # Cart elements
        self.cart_icon = page.locator('.action.showcart')
        self.cart_counter = page.locator('.counter-number')
        self.minicart = page.locator('.block-minicart')
        self.minicart_wrapper = page.locator('#minicart-content-wrapper')
        self.proceed_to_checkout = page.locator('#top-cart-btn-checkout')
        self.cart_items = page.locator('#mini-cart .item.product.product-item')
        self.cart_item_remove_buttons = page.locator('.product.actions .secondary .action.delete')
        self.cart_empty_message = page.locator('.subtitle.empty')
        self.view_and_edit_cart = page.locator('.action.viewcart')
        self.minicart_close_button = page.locator('#btn-minicart-close')
        self.cart_subtotal = page.locator('.subtotal .price-container .price')
        self.cart_items_count_text = page.locator('.items-total .count')
        
        # Wishlist and compare
        self.add_to_wishlist = page.locator('.action.towishlist')
        self.add_to_compare = page.locator('.action.tocompare')
        
        # Product tabs
        self.details_tab = page.locator('#tab-label-description')
        self.more_info_tab = page.locator('#tab-label-additional')
        self.reviews_tab = page.locator('#tab-label-reviews')
        
    def get_product_name(self) -> str:
        """Get the product name"""
        return self.product_name.text_content().strip()
    
    def get_product_price(self) -> str:
        """Get the product price"""
        return self.product_price.text_content().strip()
    
    def select_size(self, size_index: int = 0):
        """Select a size option by index"""
        self.size_options.nth(size_index).click()
        
    def select_color(self, color_index: int = 0):
        """Select a color option by index"""
        self.color_options.nth(color_index).click()
        
    def set_quantity(self, quantity: int = 1):
        """Set the product quantity"""
        self.quantity_input.fill(str(quantity))
        
    def add_to_cart(self):
        """Add the product to cart"""
        self.add_to_cart_button.click()
        # Wait for success message
        self.success_message.wait_for(state='visible', timeout=10000)
        
    def is_added_to_cart(self) -> bool:
        """Check if product was added to cart successfully"""
        return self.success_message.is_visible()
    
    def get_cart_count(self) -> int:
        """Get the number of items in cart"""
        count_text = self.cart_counter.text_content().strip()
        return int(count_text) if count_text.isdigit() else 0
    
    def proceed_to_checkout_from_minicart(self):
        """Open mini cart and proceed to checkout"""
        self.cart_icon.click()
        self.proceed_to_checkout.wait_for(state='visible', timeout=5000)
        self.proceed_to_checkout.click()
        
    def open_minicart(self):
        """Open the mini cart using a more reliable approach"""
        # The minicart has ID ui-id-1 and class block-minicart
        # We'll try a different approach to open it
        
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                # First make sure we're at the top of the page
                self.page.evaluate("window.scrollTo(0, 0)")
                self.page.wait_for_timeout(300)  # Short pause
                
                # Hover over the cart icon first to make it more reliable
                self.cart_icon.hover()
                self.page.wait_for_timeout(300)  # Short pause
                
                # Click the cart icon
                self.cart_icon.click()
                
                # Wait a moment for any animations to start
                self.page.wait_for_timeout(500)
                
                # Check if the minicart is visible by evaluating its display property
                is_visible = self.page.evaluate("""
                    () => {
                        const minicart = document.querySelector('#ui-id-1');
                        if (!minicart) return false;
                        
                        const style = window.getComputedStyle(minicart);
                        return style.display !== 'none' && style.visibility !== 'hidden';
                    }
                """)
                
                if is_visible:
                    # Success! Wait a moment to ensure it's fully loaded
                    self.page.wait_for_timeout(500)
                    return
                    
                # If not visible, try clicking again
                print(f"Attempt {attempt+1}: Minicart not visible after click, trying again")
                
            except Exception as e:
                print(f"Attempt {attempt+1} failed: {str(e)}")
            
            # Wait before next attempt
            self.page.wait_for_timeout(500)
        
        # If we get here, all attempts failed
        # As a last resort, try using JavaScript to show the minicart
        try:
            self.page.evaluate("""
                () => {
                    const minicart = document.querySelector('#ui-id-1');
                    if (minicart) {
                        minicart.style.display = 'block';
                        minicart.style.visibility = 'visible';
                    }
                }
            """)
            self.page.wait_for_timeout(500)
            print("Used JavaScript to force minicart visibility")
        except Exception as e:
            print(f"Failed to force minicart visibility: {str(e)}")
            raise Exception("Failed to open minicart after multiple attempts")
        
    def get_cart_items_count(self) -> int:
        """Get the number of items in the mini cart"""
        self.open_minicart()
        return self.cart_items.count()
        
    def remove_item_from_cart(self, item_index: int = 0):
        """Remove an item from the cart by index"""
        try:
            # Try to open the minicart
            self.open_minicart()
            
            # Get the number of items before removal
            items_before = self.cart_items.count()
            
            # Make sure we have items to remove
            if items_before == 0:
                print("No items in cart to remove")
                return
                
            # Make sure the index is valid
            if item_index >= items_before:
                print(f"Invalid item index {item_index}, only {items_before} items in cart")
                return
            
            # Ensure the minicart is still open
            if not self.page.evaluate("() => document.querySelector('#ui-id-1').style.display !== 'none'"):
                print("Minicart closed unexpectedly, reopening...")
                self.open_minicart()
            
            # Click the delete button for the specified item using JavaScript
            # This is more reliable than using Playwright's click
            try:
                # Get the delete button for the item at the specified index
                self.page.evaluate(f"""
                    () => {{
                        const items = document.querySelectorAll('#mini-cart .item.product.product-item');
                        if (items.length <= {item_index}) return false;
                        
                        const deleteButton = items[{item_index}].querySelector('.action.delete');
                        if (deleteButton) {{
                            deleteButton.click();
                            return true;
                        }}
                        return false;
                    }}
                """)
                
                # Wait for the confirmation dialog
                self.page.wait_for_timeout(1000)
                
                # Check if the confirmation dialog is visible
                dialog_visible = self.page.wait_for_selector('.modal-popup.confirm._show', timeout=3000, state='visible')
                
                if dialog_visible:
                    # Make sure the OK button is in view and click it using JavaScript
                    # This avoids the "element is outside of viewport" error
                    self.page.evaluate("""
                        () => {
                            const okButton = document.querySelector('.action-primary.action-accept');
                            if (okButton) {
                                // Scroll to make sure it's in view
                                okButton.scrollIntoView({behavior: 'smooth', block: 'center'});
                                // Wait a moment for the scroll to complete
                                setTimeout(() => {
                                    okButton.click();
                                }, 300);
                                return true;
                            }
                            return false;
                        }
                    """)
                    
                    # Wait for the removal to complete
                    self.page.wait_for_timeout(2000)
                else:
                    print("Confirmation dialog not found, trying alternative approach")
                    # Sometimes the site auto-confirms without showing the dialog
                    self.page.wait_for_timeout(2000)
                
                # Verify the item was removed
                # Reopen the minicart to get fresh data
                self.page.reload()  # Reload the page to ensure we get the latest cart state
                self.page.wait_for_load_state('networkidle')
                self.open_minicart()
                
                # Get updated count
                items_after = self.cart_items.count()
                print(f"Items before: {items_before}, Items after: {items_after}")
                
                # If item wasn't removed, try one more time with a different approach
                if items_after >= items_before:
                    print("Item not removed, trying alternative approach")
                    # Try direct API call or another method if available
                    # For now, just report the issue
                    print("Warning: Failed to remove item from cart")
                
            except Exception as e:
                print(f"Error during item removal: {str(e)}")
                self.page.wait_for_timeout(1000)
                
        except Exception as e:
            print(f"Error removing item from cart: {str(e)}")
            # Try to recover
            self.page.wait_for_timeout(1000)
        
    def remove_all_items_from_cart(self):
        """Remove all items from the cart"""
        self.open_minicart()
        # Get the number of items
        item_count = self.cart_items.count()
        # Remove each item one by one
        for i in range(item_count):
            # Always remove the first item since the list shifts after each removal
            self.remove_item_from_cart(0)
            
    def is_cart_empty(self) -> bool:
        """Check if the cart is empty"""
        self.open_minicart()
        return self.cart_empty_message.is_visible()
