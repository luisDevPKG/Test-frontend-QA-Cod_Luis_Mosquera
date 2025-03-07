from playwright.sync_api import Page


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username_input = '//*[@id="user-name"]'
        self.password_input = '//*[@id="password"]'
        self.login_button = '//*[@id="login-button"]'

    # Llena el formulario del login
    def login(self, username: str, password: str):
        self.page.fill(self.username_input, username)
        self.page.fill(self.password_input, password)
        self.page.click(self.login_button)
