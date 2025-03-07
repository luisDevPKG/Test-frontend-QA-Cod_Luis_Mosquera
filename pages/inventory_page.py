from playwright.sync_api import Page


class InventoryPage:
    def __init__(self, page: Page):
        self.page = page
        # diccionario con los selectores de los productos especificados
        self.products = {
            'red_tshirt': '//*[@id="add-to-cart-test.allthethings()-t-shirt-(red)"]',
            'bike_light': '//*[@id="add-to-cart-sauce-labs-bike-light"]'
        }
        self.cart_count = '//*[@id="shopping_cart_container"]/a/span'
        self.cart_button ='//*[@id="shopping_cart_container"]/a'

    # Agrega productos al carrito
    def add_product_to_cart(self, product_name: str):
        product_selector = self.products[product_name]
        self.page.click(product_selector)

    # Obtener el conteo de productos en el carro
    def get_cart_count(self):
        return self.page.inner_text(self.cart_count)

    # Ir al carro
    def go_to_cart(self):
        self.page.click(self.cart_button)