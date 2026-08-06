from selenium.webdriver.common.by import By


class MainPageLocators:
    HEADER = (By.XPATH, "//h6[@id='react-admin-title']")
    USERS_TABLE_HEADER_ID = (By.XPATH, "//th//span[text()='Id']")
    USERS_TABLE_HEADER_EMAIL = (By.XPATH, "//th//span[text()='Email']")
    USERS_TABLE_HEADER_FIRST_NAME = (
        By.XPATH, "//th//span[text()='First name']")
    USERS_TABLE_HEADER_LAST_NAME = (By.XPATH, "//th//span[text()='Last name']")
    USERS_TABLE_HEADER_CREATED_AT = (
        By.XPATH, "//th//span[text()='Created at']")
    USERS_CREATE_BUTTON = (By.XPATH, "//a[@aria-label='Create']")
    USERS_EXPORT_BUTTON = (By.XPATH, "//button[@aria-label='Export']")

    USERS_CREATE_FORM_FIRST_NAME_INPUT = (
        By.XPATH, "//input[@name='firstName']")
    USERS_CREATE_FORM_LAST_NAME_INPUT = (
        By.XPATH, "//input[@name='lastName']")
    USERS_CREATE_FORM_EMAIL_INPUT = (
        By.XPATH, "//input[@name='email']")
    USERS_CREATE_FORM_SAVE_BUTTON = (
        By.XPATH, "//button[text()='Save']")
    DELETE_BUTTON = (
        By.XPATH, "//button[@aria-label='Delete']")

    ELEMENT_CREATED_MESSAGE = (By.XPATH, "//div[text()='Element created']")
    ELEMENT_UPDATED_MESSAGE = (By.XPATH, "//div[text()='Element updated']")
    ELEMENT_DELETED_MESSAGE = (By.XPATH, "//div[text()='Element deleted']")
    ELEMENT_INVALID_MESSAGE = (
        By.XPATH, "//div[text()='The form is not valid. Please check for errors']")

    MAIN_CHECKBOX = (By.XPATH, "//th//input")

    NO_USERS_MESSAGE = (By.XPATH, "//p[text()='No Users yet.']")
