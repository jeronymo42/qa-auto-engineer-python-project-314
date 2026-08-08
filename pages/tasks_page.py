from pages.base_page import BasePage
from locators.tasks_page import TasksPageLocators

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains


class TasksPage(BasePage, TasksPageLocators):
    STATUS_MAP = {
        "Draft": 1,
        "To Review": 2,
        "To Be Fixed": 3,
        "To Publish": 4,
        "Published": 4,
    }

    EMAIL_MAP = {
        "john@google.com": 1,
        "jack@yahoo.com": 2,
        "jane@gmail.com": 3,
        "alice@hotmail.com": 4,
        "peter@outlook.com": 5,
        "sarah@example.com": 6,
        "michael@example.com": 7,
        "emily@example.com": 8,
    }

    FILTER_TYPES = {
        "assignee": TasksPageLocators.ASSIGNEE_FILTER_CONTAINER,
        "status": TasksPageLocators.STATUS_FILTER_CONTAINER,
        "label": TasksPageLocators.LABEL_FILTER_CONTAINER,
    }

    def __init__(self, driver):
        super().__init__(driver)

    def choose_option(self, assignee_number=1):
        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//ul[@role='listbox']/li[{assignee_number}]")
            )
        )
        self.driver.find_element(
            By.XPATH, f"//ul[@role='listbox']/li[{assignee_number}]"
        ).click()
        return self

    def fill_task(self, assignee: str, title: str, content: str, status: str):
        self.driver.find_element(*self.ASSIGNEE_COMBOBOX).click()
        assignee_number = self.EMAIL_MAP[assignee]
        self.choose_option(assignee_number)
        self.driver.find_element(*self.TITLE_INPUT).send_keys(title)
        self.driver.find_element(*self.CONTENT_INPUT).send_keys(content)
        self.driver.find_element(*self.STATUS_COMBOBOX).click()
        status_number = self.STATUS_MAP[status]
        self.choose_option(status_number)
        return self

    def find_task_by_title(self, title):
        return self.is_visible(
            (By.XPATH, f"//div[@role='button']//div[text()='{title}']")
        )

    def find_task_in_column(self, task_title, column_elem):
        return column_elem.find_element(By.XPATH, f".//div[text()='{task_title}']")

    def find_column_by_name(self, column_name):
        return self.driver.find_element(
            By.XPATH, f"//div[@data-rfd-droppable-id='{self.STATUS_MAP[column_name]}']"
        )

    def is_task_in_column(self, task_title, column_name):
        column_elem = self.find_column_by_name(column_name)
        return len(
            column_elem.find_elements(By.XPATH, f".//div[text()='{task_title}']")
        )

    def filter_by(self, filter_type, filter_value):
        self.driver.find_element(*self.FILTER_TYPES[filter_type]).click()
        goal_item = filter(
            lambda x: x.text == filter_value,
            self.driver.find_elements(*self.FILTER_LIST_ITEM),
        )

        goal_item = next(goal_item)
        self.wait.until(EC.element_to_be_clickable(goal_item)).click()
        self.wait.until(EC.visibility_of_element_located(self.ADD_FILTER_BUTTON))
        return self

    def clear_filter(self, filter_type):
        self.driver.find_element(*self.FILTER_TYPES[filter_type]).click()
        self.driver.find_element(By.XPATH, "//li[@role='option'][1]").click()
        self.is_invisible(self.ADD_FILTER_BUTTON)
        return self

    def count_cards(self):
        return len(self.driver.find_elements(*self.TASK_CARD))

    def edit_task_title(self, old_title, new_title):
        self.driver.find_element(
            By.XPATH,
            f"//div[@role='button']//div[text()='{old_title}']/../..//a[@aria-label='Edit']",
        ).click()
        title_input = self.driver.find_element(*self.TITLE_INPUT)
        self.clear_input(title_input)
        self.driver.find_element(*self.TITLE_INPUT).send_keys(new_title)
        self.save_form("updated")
        return self

    def delete_task(self, task_title):
        self.driver.find_element(
            By.XPATH, f"//div[text()='{task_title}']/../..//a[@aria-label='Edit']"
        ).click()
        self.driver.find_element(*self.DELETE_BUTTON).click()
        self.wait.until(
            EC.invisibility_of_element_located(self.ELEMENT_DELETED_MESSAGE)
        )

    def find_column_by_number(self, number):
        return self.driver.find_element(
            By.XPATH, f"//div[@data-rfd-droppable-id='{number}']"
        )

    def move_card(self, task_title, column_name):
        task = self.find_task_by_title(task_title)
        column = self.find_column_by_name(column_name)

        start = task.location
        finish = column.location
        ActionChains(self.driver).drag_and_drop_by_offset(
            task, finish["x"] - start["x"], finish["y"] - start["y"]
        ).perform()
        return self

    def change_status(self, task_title, new_status):
        self.driver.find_element(
            By.XPATH,
            f"//div[@role='button']//div[text()='{task_title}']/../..//a[@aria-label='Edit']",
        ).click()
        self.driver.find_element(*self.STATUS_COMBOBOX).click()
        status_number = self.STATUS_MAP[new_status]
        self.choose_option(status_number)
        self.save_form("updated")
        return self
