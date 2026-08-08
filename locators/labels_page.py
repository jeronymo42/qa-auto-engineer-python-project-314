from selenium.webdriver.common.by import By

from locators.base_page import BasePageLocators


class LabelsPageLocators(BasePageLocators):

    CREATE_FORM_LABEL_NAME_INPUT = (By.XPATH, "//input[@name='name']")
