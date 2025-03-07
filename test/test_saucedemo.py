import pytest
import json
import os


from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

class TestSauceDemo:

    # Cargar datos desde el archivo JSON
    def cargar_datos(self):
        ruta_archivo = os.path.join(os.path.dirname(__file__), "..", "utils", "data.json")
        with open(ruta_archivo, "r") as file:
            return json.load(file)

    @pytest.fixture(scope="class")
    def browser(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False, slow_mo=500)
            page = browser.new_page()
            yield page
            browser.close()

    # Inicio de sesion y retorno la pagina autenticada
    @pytest.fixture(scope="class")
    def login(self, browser):
        data = self.cargar_datos()
        page = browser
        page.goto("https://www.saucedemo.com/")

        # Intancio el modelo de la pagina de login
        login_page = LoginPage(page)
        login_page.login(data["login"]["username"],data["login"]["password"])

        # Esperar la redirección al inventario
        page.wait_for_selector(".inventory_list")
        return page

    # Agregar productos al carrito
    @pytest.fixture(scope="class")
    def agregar_productos (self, login):
        data = self.cargar_datos()
        page = login

        inventory_page = InventoryPage(page)
        # Agregar productos al carrito
        for producto in data["productos"]:
            inventory_page.agregar_productos_al_carrito(producto["name"])

        return inventory_page

    # Caso 1: Valido el inicio de sesion exitoso
    def test_login(self, login):
        page = login
        assert page.url == "https://www.saucedemo.com/inventory.html", "No se inicio sesion correctamente, no ha redirigido a la pagina de Inventario"

    # Caso 2: Agrego los 2 productos
    def test_agregar_productos_al_carrito(self, login, agregar_productos):
        page = login
        # Intancio el modelo de la pagina de inventario
        inventory_page = agregar_productos

        # Valida que el contador del carrito se actualice correctamente
        page.wait_for_selector(inventory_page.cart_count)
        assert inventory_page.obtener_el_conteo_carrito() == "2", "Algo ha fallado, solo se agrego un producto o no se agregaron los productos al arrito"

    # Caso 3: Validar carrito compras
    def test_validar_carrito_compras(self, login, agregar_productos):
        data = self.cargar_datos()
        page = login
        cart_page = CartPage(page)

        # Ir al carrito
        cart_page.ir_al_carrito()
        page.wait_for_selector(".cart_list")

        # Verificar productos en el carrito
        cart_products = cart_page.obtener_informacion_productos()
        print(cart_products)

        # Productos esperados
        expected_products = [
            (producto["display_name"], producto["price"]) for producto in data["productos"]
        ]
        # Comparación de listas
        assert cart_products == expected_products, f"Productos en el carrito incorrectos: {cart_products}"

    # Caso 4: Checkout y finalizar pedido
    def test_validar_checkout(self, login, agregar_productos):
        data = self.cargar_datos()
        page = login
        cart_page = CartPage(page)
        checkout_page = CheckoutPage(page)

        # Ir al carrito
        cart_page.ir_al_carrito()
        page.wait_for_selector(".cart_list")

        # Proceder al checkout
        checkout_page.redirigir_checkout()
        checkout_page.formulario_checkout(data["checkout"]["first_name"], data["checkout"]["last_name"], data["checkout"]["postal_code"])

        # Obtener valores del resumen
        subtotal, tax, total = checkout_page.resumen_pedido()

        # Verifico informacion del pedido
        assert subtotal == data["checkout"]["expected_summary"]["subtotal"], f"Subtotal incorrecto: {subtotal}"
        assert tax == data["checkout"]["expected_summary"]["tax"], f"Impuesto incorrecto: {tax}"
        assert total == data["checkout"]["expected_summary"]["total"], f"Total incorrecto: {total}"

        checkout_page.completar_compra()

        # Obtener y verificar mensaje de confirmación
        confirmation_message = checkout_page.confirmacion_compra()
        assert confirmation_message == data["checkout"]["confirmation_message"], f"Ha ocurrido un error, Mensaje incorrecto: {confirmation_message}"