import allure
from selene import browser, have, be


class LoginPage:
    def __init__(self):
        self.username_input = browser.element('#username')
        self.password_input = browser.element('#password')
        self.login_button = browser.element('#login_button')
        self.error_message = browser.element('div.error_status.card')

    @allure.step('Open login page')
    def open(self):
        browser.open('/login')
        return self

    @allure.step('Fill username: "{username}"')
    def fill_username(self, username: str):
        self.username_input.should(be.visible).type(username)
        return self

    @allure.step('Fill password')
    def fill_password(self, password: str):
        self.password_input.should(be.visible).type(password)
        return self

    @allure.step('Click login button')
    def submit(self):
        self.login_button.click()
        return self

    @allure.step('Login with credentials')
    def login(self, username: str, password: str):
        self.fill_username(username).fill_password(password).submit()
        return self

    @allure.step('Verify login form has required fields')
    def should_have_login_form(self):
        self.username_input.should(be.visible)
        self.password_input.should(be.visible)
        self.login_button.should(be.visible)
        return self

    @allure.step('Verify error message is displayed')
    def should_have_error(self):
        self.error_message.should(be.visible)
        return self
