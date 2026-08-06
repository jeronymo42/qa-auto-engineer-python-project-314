from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from pages.base_page import BasePage
from locators.main_page import MainPageLocators


class MainPage(BasePage, MainPageLocators):
    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(self.driver, 10)

    def logout(self):
        self.wait.until(EC.element_to_be_clickable(self.PROFILE_BUTTON))
        self.driver.find_element(*self.PROFILE_BUTTON).click()
        self.wait.until(EC.element_to_be_clickable(self.LOGOUT_BUTTON))
        self.driver.find_element(*self.LOGOUT_BUTTON).click()

        return self

    def switch_to_users_page(self):
        self.wait.until(EC.element_to_be_clickable(self.USERS_LINK))
        self.driver.find_element(*self.USERS_LINK).click()
        self.wait.until(EC.visibility_of_element_located(self.HEADER))
        return self

    def open_create_user_form(self):
        self.wait.until(EC.element_to_be_clickable(self.USERS_CREATE_BUTTON))
        self.driver.find_element(*self.USERS_CREATE_BUTTON).click()
        self.wait.until(EC.visibility_of_element_located(
            self.USERS_CREATE_FORM_FIRST_NAME_INPUT))
        return self

    def find_user_row_by_data(self, data):
        self.wait.until(EC.visibility_of_element_located(
            self.USERS_TABLE_HEADER_EMAIL))
        return self.driver.find_element(
            By.XPATH, f"//td/span[text()='{data}']/../..")

    def get_user_email(self, user_row):
        email = user_row.find_element(By.XPATH, "./td[3]").text
        return email

    def get_user_first_name(self, user_row):
        first_name = user_row.find_element(By.XPATH, "./td[4]").text
        return first_name

    def get_user_last_name(self, user_row):
        last_name = user_row.find_element(By.XPATH, "./td[5]").text
        return last_name

    def get_user_by_row_number(self, row_number):
        return self.driver.find_element(
            By.XPATH, f"//tbody/tr[{row_number}]")

    def clear_input(self, input):
        input.send_keys(Keys.CONTROL + "a")
        input.send_keys(Keys.DELETE)
        return self

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
        self.open_create_user_form()
        self.edit_user_email(email)
        self.edit_user_first_name(first_name)
        self.edit_user_last_name(last_name)
        self.save_user('created')
        return self

    def save_user(self, expected_status):
        statuses = {
            "created": self.ELEMENT_CREATED_MESSAGE,
            "updated": self.ELEMENT_UPDATED_MESSAGE,
            "deleted": self.ELEMENT_DELETED_MESSAGE,
            "invalid": self.ELEMENT_INVALID_MESSAGE
        }
        self.driver.find_element(
            *self.USERS_CREATE_FORM_SAVE_BUTTON).click()
        self.wait.until(EC.visibility_of_element_located(
            statuses[expected_status]
        ))
        return self

    def delete_users(self, number_of_users=1):
        self.driver.find_element(
            *self.DELETE_BUTTON).click()
        if number_of_users == 1:
            self.wait.until(EC.visibility_of_element_located(
                self.ELEMENT_DELETED_MESSAGE
            ))
        else:
            self.wait.until(EC.visibility_of_element_located(
                (By.XPATH,
                 f"//div[text()='{number_of_users} elements deleted']")
            ))
        return self

    def select_all_users(self):
        self.driver.find_element(*self.MAIN_CHECKBOX).click()
        return self

    def select_users(self, users):
        for user in users:
            row = self.find_user_row_by_data(user)
            row.find_element(By.TAG_NAME, "input").click()
        return self
