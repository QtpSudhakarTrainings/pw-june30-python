from .base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.txt_username = page.get_by_placeholder("Username").describe("Username Textbox in Login Page")
        self.txt_password = page.get_by_role("textbox", name="Password").describe("Password Textbox in Login Page")
        self.btn_login = page.get_by_role("button", name="Login").describe("Login Button in Login Page")

    def enter_username(self, username: str) -> None:
        self.txt_username.fill(username)
        print(f"User Name Entered: {username}")

    def enter_password(self, password: str) -> None:
        self.txt_password.fill(password)
        print(f"Password Entered: {password}")

    def click_login(self) -> None:
        self.btn_login.click()
        print("Login button clicked")
