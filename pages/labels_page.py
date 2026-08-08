from pages.base_page import BasePage
from locators.labels_page import LabelsPageLocators

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class LabelsPage(BasePage, LabelsPageLocators):

    def __init__(self, driver):
        super().__init__(driver)

    def edit_label_name(self, label_name):
            input = self.driver.find_element(
                *self.CREATE_FORM_LABEL_NAME_INPUT)
            self.clear_input(input)
            input.send_keys(label_name)
            return self

    def get_label_name_from_row(self, row):
        return row.find_element(By.XPATH, "./td[3]").text

