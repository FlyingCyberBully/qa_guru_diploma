import allure
from selene import browser, have, be


class SearchResultsPage:
    def __init__(self):
        self.results_wrapper = browser.element('section.main_content.search_results')
        self.movie_results = browser.element('div.search_results.movie')
        self.result_cards = browser.all('div.search_results.movie div.card.v4')
        self.result_titles = browser.all('div.search_results.movie a.result h2')

    @allure.step('Verify search results are displayed')
    def should_have_results(self):
        self.movie_results.should(be.visible)
        self.result_cards.should(have.size_greater_than(0))
        return self

    @allure.step('Verify results contain movie: "{title}"')
    def should_have_movie(self, title: str):
        self.movie_results.should(have.text(title))
        return self

    @allure.step('Verify results page is loaded')
    def should_be_loaded(self):
        self.results_wrapper.should(be.visible)
        return self

    @allure.step('Open first result')
    def open_first_result(self):
        self.result_cards.first.element('a.result').click()
        from pages.movie_page import MoviePage

        return MoviePage()
