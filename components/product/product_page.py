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
        self.proceed_to_checkout = page.locator('#top-cart-btn-checkout')
        
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
