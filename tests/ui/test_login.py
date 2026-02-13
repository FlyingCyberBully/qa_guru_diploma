import allure
import pytest

from pages.login_page import LoginPage

pytestmark = [
    pytest.mark.ui,
    allure.epic('UI'),
    allure.feature('Login'),
]


@allure.story('Login Form')
class TestLogin:

    @allure.title('Login page has required fields')
    @allure.tag('smoke')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_page_has_required_fields(self):
        LoginPage().open().should_have_login_form()

    @allure.title('Login with invalid credentials shows error')
    @allure.tag('regression')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_with_invalid_credentials(self):
        login_page = LoginPage().open()
        login_page.login(username='invalid_user', password='wrong_pass')
        login_page.should_have_error()
