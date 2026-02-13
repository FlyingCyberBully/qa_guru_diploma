import allure
from selene import browser, have, be


class MoviePage:
    def __init__(self):
        self.title = browser.element('div.header_poster_wrapper section h2 a')
        self.overview = browser.element('div.header_poster_wrapper div.overview p')
        self.user_score = browser.element('div.user_score_chart')
        self.cast_section = browser.element('section.cast_cards')
        self.facts_section = browser.element('section.facts')

    @allure.step('Open movie page by id: {movie_id}')
    def open(self, movie_id: int, slug: str = ''):
        path = f'/movie/{movie_id}'
        if slug:
            path += f'-{slug}'
        browser.open(path)
        return self

    @allure.step('Verify movie title is: "{expected_title}"')
    def should_have_title(self, expected_title: str):
        self.title.should(have.text(expected_title))
        return self

    @allure.step('Verify movie overview contains: "{text}"')
    def should_have_overview_containing(self, text: str):
        self.overview.should(have.text(text))
        return self

    @allure.step('Verify user score is displayed')
    def should_have_user_score(self):
        self.user_score.should(be.visible)
        return self

    @allure.step('Verify cast section is displayed')
    def should_have_cast_section(self):
        self.cast_section.should(be.visible)
        return self
