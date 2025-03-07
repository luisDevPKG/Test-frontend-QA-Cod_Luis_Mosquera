from playwright.sync_api import Page


class CartPage:
    def __init__(self, page: Page):
        self.page = page
        self.product_names = 'div.inventory_item_name'
        self.product_prices = 'div.inventory_item_price'
        self.checkout_button = '//*[@id="checkout"]'

    def obtener_informacion_productos(self):
        product_names = [element.text_content().strip() for element in
                         self.page.locator(self.product_names).all()]
        product_prices = [element.text_content().strip() for element in
                          self.page.locator(self.product_prices).all()]
        # Retorno lista de tuplas: (nombre, precio)
        return list(zip(product_names, product_prices))

    def redirigir_checkout(self):
        self.page.click(self.checkout_button)