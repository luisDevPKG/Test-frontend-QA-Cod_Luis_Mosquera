from playwright.sync_api import Page


class CartPage:
    def __init__(self, page: Page):
        self.page = page
        self.cart_button ='//*[@id="shopping_cart_container"]/a'
        self.product_names = 'div.inventory_item_name'
        self.product_prices = 'div.inventory_item_price'

    # Ir al carro
    def ir_al_carrito(self):
        self.page.click(self.cart_button)

    def obtener_informacion_productos(self):
        product_names = [element.text_content().strip() for element in
                         self.page.locator(self.product_names).all()]
        product_prices = [element.text_content().strip() for element in
                          self.page.locator(self.product_prices).all()]
        # Retorno lista de tuplas: (nombre, precio)
        return list(zip(product_names, product_prices))

