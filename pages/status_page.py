from pages.base_page import BasePage
from locators.status_page import StatusPageLocators

from selenium.webdriver.common.by import By


class StatusPage(BasePage, StatusPageLocators):
    def __init__(self, driver):
        super().__init__(driver)

    def fill_form(self, name, slug):
        self.clear_input(self.driver.find_element(*self.CREATE_FORM_NAME_INPUT))
        self.driver.find_element(*self.CREATE_FORM_NAME_INPUT).send_keys(name)

        self.clear_input(self.driver.find_element(*self.CREATE_FORM_SLUG_INPUT))
        self.driver.find_element(*self.CREATE_FORM_SLUG_INPUT).send_keys(slug)
        return self

    def create_status(self, name, slug):
        self.open_create_element_form()
        self.fill_form(name, slug)
        self.save_form("created")
        return self

    def get_name_from_row(self, row):
        return row.find_element(By.XPATH, "./td[3]").text

    def get_slug_from_row(self, row):
        return row.find_element(By.XPATH, "./td[4]").text

    def select_row_by_number(self, row_number):
        row = self.driver.find_element(By.XPATH, f"//tbody/tr[{row_number}]")
        row.find_element(By.TAG_NAME, "input").click()
        return row
