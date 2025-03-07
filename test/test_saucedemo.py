import pytest
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage

class TestSauceDemo:

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
        page = browser
        page.goto("https://www.saucedemo.com/")

        # Intancio el modelo de la pagina de login
        login_page = LoginPage(page)
        login_page.login("standard_user", "secret_sauce")

        # Esperar la redirección al inventario
        page.wait_for_selector(".inventory_list")
        return page

    @pytest.fixture(scope="class")
    def agregar_productos (self, login):
        page = login
        # Agregar productos al carrito
        inventory_page = InventoryPage(page)
        inventory_page.agregar_productos_al_carrito('red_tshirt')
        inventory_page.agregar_productos_al_carrito('bike_light')

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
        page = login
        inventory_page = agregar_productos

        # Ir al carrito
        inventory_page.ir_al_carrito()
        page.wait_for_selector(".cart_list")

        # Verificar productos en el carrito
        cart_page = CartPage(page)
        cart_products = cart_page.obtener_informacion_productos()
        print(cart_products)

        # Productos esperados
        expected_products = [
            ("Test.allTheThings() T-Shirt (Red)", "$15.99"),
            ("Sauce Labs Bike Light", "$9.99")
        ]
        # Comparación de listas
        assert cart_products == expected_products, f"Productos en el carrito incorrectos: {cart_products}"