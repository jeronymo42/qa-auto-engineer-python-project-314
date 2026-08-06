from pages.base_page import BasePage
from locators.tasks_page import TasksPageLocators

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class TasksPage(BasePage, TasksPageLocators):

    def __init__(self, driver):
        super().__init__(driver)

    def choose_option(self, assignee_number=1):
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, f"//ul[@role='listbox']/li[{assignee_number}]")
        ))
        self.driver.find_element(
            By.XPATH, f"//ul[@role='listbox']/li[{assignee_number}]").click()
        return self

    def fill_task(self, assignee, title, content, status):
        self.driver.find_element(*self.ASSIGNEE_COMBOBOX).click()
        self.choose_option(assignee)
        self.driver.find_element(*self.TITLE_INPUT).send_keys(title)
        self.driver.find_element(*self.CONTENT_INPUT).send_keys(content)
        self.driver.find_element(*self.STATUS_COMBOBOX).click()
        self.choose_option(status)
        return self

    def find_task_by_title(self, title):
        return self.is_visible((By.XPATH, f"//div[@role='button']//div[text()='{title}']"))
