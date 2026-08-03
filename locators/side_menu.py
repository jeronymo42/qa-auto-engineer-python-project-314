from selenium.webdriver.common.by import By


class SideMenuLocators:
    DASHBOARD_LINK = (By.XPATH, "//a[@role='menuitem' and text()='Dashboard']")
    TASKS_LINK = (By.XPATH, "//a[@role='menuitem' and text()='Tasks']")
    USERS_LINK = (By.XPATH, "//a[@role='menuitem' and text()='Users']")
    LABELS_LINK = (By.XPATH, "//a[@role='menuitem' and text()='Labels']")
    TASK_STATUSES_LINK = (
        By.XPATH, "//a[@role='menuitem' and text()='Task statuses']")
