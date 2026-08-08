from selenium.webdriver.common.by import By

from locators.base_page import BasePageLocators


class StatusPageLocators(BasePageLocators):
    CREATE_FORM_NAME_INPUT = (By.XPATH, "//input[@name='name']")
    CREATE_FORM_SLUG_INPUT = (By.XPATH, "//input[@name='slug']")

    NAME_HEADER = (By.XPATH, "//th//span[text()='Name']")
    SLUG_HEADER = (By.XPATH, "//th//span[text()='Slug']")

    NO_STATUS_MESSAGE = (By.XPATH, "//p[text()='No Task statuses yet.']")
