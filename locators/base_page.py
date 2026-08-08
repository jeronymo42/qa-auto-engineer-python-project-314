from selenium.webdriver.common.by import By


class BasePageLocators:
    HEADER = (By.XPATH, "//h6[@id='react-admin-title']")

    DELETE_BUTTON = (By.XPATH, "//button[@aria-label='Delete']")
    SAVE_BUTTON = (By.XPATH, "//button[text()='Save']")

    ELEMENT_CREATED_MESSAGE = (By.XPATH, "//div[text()='Element created']")
    ELEMENT_UPDATED_MESSAGE = (By.XPATH, "//div[text()='Element updated']")
    ELEMENT_DELETED_MESSAGE = (By.XPATH, "//div[text()='Element deleted']")
    ELEMENT_INVALID_MESSAGE = (
        By.XPATH,
        "//div[text()='The form is not valid. Please check for errors']",
    )

    MAIN_CHECKBOX = (By.XPATH, "//th//input")

    CREATE_BUTTON = (By.XPATH, "//a[@aria-label='Create']")
    EXPORT_BUTTON = (By.XPATH, "//button[@aria-label='Export']")
