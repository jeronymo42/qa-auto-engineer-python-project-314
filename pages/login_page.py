from locators.login_page import LoginPageLocators
from pages.base_page import BasePage


class LoginPage(BasePage, LoginPageLocators):
    def __init__(self, driver):
        super().__init__(driver)

    def login(self, username, password):
        self.driver.find_element(*self.USERNAME_INPUT).send_keys(username)
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        self.driver.find_element(*self.LOGIN_BUTTON).click()

        return self
