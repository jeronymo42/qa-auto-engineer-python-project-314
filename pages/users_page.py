from pages.base_page import BasePage
from locators.users_page import UsersPageLocators

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class UsersPage(BasePage, UsersPageLocators):

    def __init__(self, driver):
        super().__init__(driver)

    def get_user_email(self, user_row):
        email = user_row.find_element(By.XPATH, "./td[3]").text
        return email

    def get_user_first_name(self, user_row):
        first_name = user_row.find_element(By.XPATH, "./td[4]").text
        return first_name

    def get_user_last_name(self, user_row):
        last_name = user_row.find_element(By.XPATH, "./td[5]").text
        return last_name

    def edit_user_email(self, email):
        input = self.driver.find_element(
            *self.USERS_CREATE_FORM_EMAIL_INPUT)
        self.clear_input(input)
        input.send_keys(email)
        return self

    def edit_user_first_name(self, first_name):
        input = self.driver.find_element(
            *self.USERS_CREATE_FORM_FIRST_NAME_INPUT)
        self.clear_input(input)
        input.send_keys(first_name)
        return self

    def edit_user_last_name(self, last_name):
        input = self.driver.find_element(
            *self.USERS_CREATE_FORM_LAST_NAME_INPUT)
        self.clear_input(input)
        input.send_keys(last_name)
        return self

    def create_user(self, email, first_name, last_name):
        self.open_create_element_form()
        self.edit_user_email(email)
        self.edit_user_first_name(first_name)
        self.edit_user_last_name(last_name)
        self.save_form('created')
        return self

    def select_users(self, users):
        for user in users:
            row = self.find_table_row_by_data(page_header='Users', data=user)
            row.find_element(By.TAG_NAME, "input").click()
        return self
