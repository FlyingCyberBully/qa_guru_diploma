import allure
import pytest

from wiki_mobile.screens.onboarding_screen import OnboardingScreen

pytestmark = [
    pytest.mark.mobile,
    allure.epic('Mobile'),
    allure.feature('Onboarding'),
]


@allure.story('First Launch')
class TestOnboarding:

    @allure.title('Onboarding screen is displayed on first launch')
    @allure.tag('smoke')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_onboarding_screen_visible(self):
        OnboardingScreen().should_be_visible()

    @allure.title('User can skip onboarding')
    @allure.tag('smoke')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_skip_onboarding(self):
        from wiki_mobile.screens.main_screen import MainScreen

        OnboardingScreen().skip()
        MainScreen().should_be_visible()
