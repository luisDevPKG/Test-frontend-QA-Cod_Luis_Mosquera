import pytest
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

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

    # Caso 1: Valido el inicio de sesion exitoso
    def test_login(self, login):
            page = login
            assert page.url == "https://www.saucedemo.com/inventory.html", "No se inicio sesion correctamente, no ha redirigido a la pagina de Inventario"

    # Caso 2: Agrego los 2 productos
    def test_add_products_to_cart(self, login):
            page = login
            # Intancio el modelo de la pagina de inventario
            inventory_page = InventoryPage(page)

            # Agrego productos al carrito
            inventory_page.add_product_to_cart('red_tshirt')
            inventory_page.add_product_to_cart('bike_light')

            # Valida que el contador del carrito se actualice correctamente
            page.wait_for_selector(inventory_page.cart_count)
            assert inventory_page.get_cart_count() == "2", "Algo ha fallado, solo se agrego un producto o no se agregaron los productos al arrito"
