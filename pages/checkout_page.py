from playwright.sync_api import Page


class CheckoutPage:
    def __init__(self, page: Page):
        self.page = page
        self.checkout_button = '//*[@id="checkout"]'
        self.first_name_input = '//*[@id="first-name"]'
        self.last_name_input = '//*[@id="last-name"]'
        self.zip_code_input = '//*[@id="postal-code"]'
        self.continue_button = '//*[@id="continue"]'
        self.subtotal = '//*[@id="checkout_summary_container"]/div/div[2]/div[6]'
        self.tax = '//*[@id="checkout_summary_container"]/div/div[2]/div[7]'
        self.total = '//*[@id="checkout_summary_container"]/div/div[2]/div[8]'
        self.finish_button = '//*[@id="finish"]'
        self.confirmation_message = '//*[@id="checkout_complete_container"]/h2'

    def redirigir_checkout(self):
        self.page.click(self.checkout_button)

    def formulario_checkout(self, first_name: str, last_name: str, zip_code: str):
        self.page.fill(self.first_name_input, first_name)
        self.page.fill(self.last_name_input, last_name)
        self.page.fill(self.zip_code_input, zip_code)
        self.page.click(self.continue_button)

    # Obtengo los valores subtotal, tax y total y los retorno en una tupla
    def resumen_pedido(self) -> tuple:
        subtotal = self.page.locator(self.subtotal).text_content().strip()
        tax = self.page.locator(self.tax).text_content().strip()
        total = self.page.locator(self.total).text_content().strip()
        return subtotal, tax, total

    def completar_compra(self):
        self.page.click(self.finish_button)

    def confirmacion_compra(self):
        return self.page.locator(self.confirmation_message).text_content().strip()
