from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from locators.header_menu import HeaderMenuLocators
from locators.side_menu import SideMenuLocators
from locators.base_page import BasePageLocators


class BasePage(HeaderMenuLocators, SideMenuLocators, BasePageLocators):
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def header_loaded(self, header_text):
        return self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, f"//h6//span[text()='{header_text}']")))

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

    def switch_to_tasks_page(self):
        self.wait.until(EC.element_to_be_clickable(self.TASKS_LINK))
        self.driver.find_element(*self.TASKS_LINK).click()
        self.wait.until(EC.visibility_of_element_located(self.HEADER))
        return self

    def clear_input(self, input):
        input.send_keys(Keys.CONTROL + "a")
        input.send_keys(Keys.DELETE)
        return self

    def open_create_element_form(self):
        self.wait.until(EC.element_to_be_clickable(self.CREATE_BUTTON))
        self.driver.find_element(*self.CREATE_BUTTON).click()
        self.wait.until(EC.visibility_of_element_located(self.SAVE_BUTTON))
        return self

    def save_form(self, expected_status):
        statuses = {
            "created": self.ELEMENT_CREATED_MESSAGE,
            "updated": self.ELEMENT_UPDATED_MESSAGE,
            "deleted": self.ELEMENT_DELETED_MESSAGE,
            "invalid": self.ELEMENT_INVALID_MESSAGE
        }
        self.driver.find_element(
            *self.SAVE_BUTTON).click()
        self.wait.until(EC.visibility_of_element_located(
            statuses[expected_status]
        ))
        return self

    def delete_elements(self, number_of_elements=1):
        self.driver.find_element(
            *self.DELETE_BUTTON).click()
        if number_of_elements == 1:
            self.wait.until(EC.visibility_of_element_located(
                self.ELEMENT_DELETED_MESSAGE
            ))
        else:
            self.wait.until(EC.visibility_of_element_located(
                (By.XPATH,
                    f"//div[text()='{number_of_elements} elements deleted']")
            ))
        return self

    def is_visible(self, element):
        return self.wait.until(EC.visibility_of_element_located(element))

    def is_invisible(self, element):
        return self.wait.until(EC.invisibility_of_element(element))

    def is_clickable(self, element):
        return self.wait.until(EC.element_to_be_clickable(element))

    def is_located(self, element):
        return self.wait.until(EC.presence_of_element_located(element))
