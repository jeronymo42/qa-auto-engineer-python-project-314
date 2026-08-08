from selenium.webdriver.common.by import By

from locators.base_page import BasePageLocators


class TasksPageLocators(BasePageLocators):

    ASSIGNEE_INPUT = (By.XPATH, "//input[@name='assignee_id']")
    ASSIGNEE_COMBOBOX = (
        By.XPATH, "//input[@name='assignee_id']/preceding-sibling::div")
    ASSIGNEE_FILTER_CONTAINER = (By.XPATH, "//input[@name='assignee_id']/..")
    TITLE_INPUT = (By.XPATH, "//input[@name='title']")
    CONTENT_INPUT = (By.XPATH, "//textarea[@name='content']")
    STATUS_INPUT = (By.XPATH, "//input[@name='status_id']")
    STATUS_COMBOBOX = (
        By.XPATH, "//input[@name='status_id']/preceding-sibling::div")
    STATUS_FILTER_CONTAINER = (By.XPATH, "//input[@name='status_id']/..")
    LABEL_INPUT = (By.XPATH, "//input[@name='label_id']")
    LABEL_COMBOBOX = (
        By.XPATH, "//input[@name='label_id']/preceding-sibling::div")
    LABEL_FILTER_CONTAINER = (By.XPATH, "//input[@name='label_id']/..")

    FILTER_LIST_ITEM = (By.XPATH, "//li[@role='option']")

    ADD_FILTER_BUTTON = (By.XPATH, "//button[text()='Add filter']")

    TASK_CARD = (By.XPATH, "//div[@role='button']")

    TASK_TABLE_HEADER_DRAFT = (By.XPATH, "//h6[text()='Draft']")
    TASK_TABLE_HEADER_TO_REVIEW = (By.XPATH, "//h6[text()='To Review']")
    TASK_TABLE_HEADER_TO_BE_FIXED = (By.XPATH, "//h6[text()='To Be Fixed']")
    TASK_TABLE_HEADER_TO_PUBLISH = (By.XPATH, "//h6[text()='To Publish']")
    TASK_TABLE_HEADER_PUBLISHED = (By.XPATH, "//h6[text()='Published']")

    EDIT_TASK_BUTTON = (By.XPATH, "//a[@aria-label='Edit']")