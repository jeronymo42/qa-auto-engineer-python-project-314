from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from locators.main_page import MainPageLocators


class MainPage(BasePage, MainPageLocators):
    def __init__(self, driver):
        super().__init__(driver)

    def logout(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable(self.PROFILE_BUTTON))
        self.driver.find_element(*self.PROFILE_BUTTON).click()
        wait.until(EC.element_to_be_clickable(self.LOGOUT_BUTTON))
        self.driver.find_element(*self.LOGOUT_BUTTON).click()

        return self
