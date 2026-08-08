from selenium.webdriver.common.by import By

from locators.base_page import BasePageLocators


class LabelsPageLocators(BasePageLocators):
    CREATE_FORM_LABEL_NAME_INPUT = (By.XPATH, "//input[@name='name']")
    ASSIGNEE_FILTER = (By.XPATH, "//div[@data-source='assignee_id']")
    STATUS_FILTER = (By.XPATH, "//div[@data-source='status_id']")
    LABEL_FILTER = (By.XPATH, "//div[@data-source='label_id']")
    ASSIGNEE_FILTER_INPUT = (By.XPATH, "//input[@name='assignee_id']")
    STATUS_FILTER_INPUT = (By.XPATH, "//input[@name='status_id']")
    LABEL_FILTER_INPUT = (By.XPATH, "//input[@name='label_id']")
