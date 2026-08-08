from selenium.webdriver.common.by import By


class LoginPageLocators:
    USERNAME_INPUT = (By.XPATH, "//input[@name='username']")
    PASSWORD_INPUT = (By.XPATH, "//input[@name='password']")
    LOGIN_BUTTON = (By.XPATH, "//button[text()='Sign in']")
    ERROR_MESSAGE = (
        By.XPATH,
        "//div[text()='The form is not valid. Please check for errors']",
    )
