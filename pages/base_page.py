from locators.header_menu import HeaderMenuLocators
from locators.side_menu import SideMenuLocators


class BasePage(HeaderMenuLocators, SideMenuLocators):
    def __init__(self, driver):
        self.driver = driver
