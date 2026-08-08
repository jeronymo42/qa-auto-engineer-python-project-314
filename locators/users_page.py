from selenium.webdriver.common.by import By

from locators.base_page import BasePageLocators


class UsersPageLocators(BasePageLocators):
    USERS_TABLE_HEADER_ID = (By.XPATH, "//th//span[text()='Id']")
    USERS_TABLE_HEADER_EMAIL = (By.XPATH, "//th//span[text()='Email']")
    USERS_TABLE_HEADER_FIRST_NAME = (By.XPATH, "//th//span[text()='First name']")
    USERS_TABLE_HEADER_LAST_NAME = (By.XPATH, "//th//span[text()='Last name']")
    USERS_TABLE_HEADER_CREATED_AT = (By.XPATH, "//th//span[text()='Created at']")
    USERS_CREATE_FORM_FIRST_NAME_INPUT = (By.XPATH, "//input[@name='firstName']")
    USERS_CREATE_FORM_LAST_NAME_INPUT = (By.XPATH, "//input[@name='lastName']")
    USERS_CREATE_FORM_EMAIL_INPUT = (By.XPATH, "//input[@name='email']")
    NO_USERS_MESSAGE = (By.XPATH, "//p[text()='No Users yet.']")
