from selenium.webdriver.common.by import By


class HeaderMenuLocators:
    OPEN_HEADER_MENU_BUTTON = (By.XPATH, "//button[@aria-label='Open menu']")
    CLOSE_HEADER_MENU_BUTTON = (By.XPATH, "//button[@aria-label='Close menu']")
    THEME_TOGGLE_BUTTON = (
        By.XPATH, "//button[@aria-label='Toggle light/dark mode']")
    PROFILE_BUTTON = (By.XPATH, "//button[@aria-label='Profile']")
    LOGOUT_BUTTON = (By.XPATH, "//span[text()='Logout']")
