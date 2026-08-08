from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from locators.header_menu import HeaderMenuLocators
from locators.side_menu import SideMenuLocators
from locators.base_page import BasePageLocators


class BasePage(HeaderMenuLocators, SideMenuLocators, BasePageLocators):
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def header_loaded(self, header_text):
        return self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, f"//h6//span[text()='{header_text}']")
            )
        )

    def logout(self):
        self.wait.until(EC.element_to_be_clickable(self.PROFILE_BUTTON))
        self.driver.find_element(*self.PROFILE_BUTTON).click()
        self.wait.until(EC.element_to_be_clickable(self.LOGOUT_BUTTON))
        self.driver.find_element(*self.LOGOUT_BUTTON).click()
        return self

    def switch_to_page(self, page_name):
        pages = {
            "users": self.USERS_LINK,
            "tasks": self.TASKS_LINK,
            "status": self.TASK_STATUSES_LINK,
            "labels": self.LABELS_LINK,
        }
        self.wait.until(EC.element_to_be_clickable(pages[page_name]))
        self.driver.find_element(*pages[page_name]).click()
        self.wait.until(EC.visibility_of_element_located(self.HEADER))
        return self

    def find_table_row_by_data(self, page_header, data):
        self.header_loaded(page_header)
        goal_item_xpath = f"//td/span[text()='{data}']/../.."
        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, goal_item_xpath)
            )
        )
        return self.driver.find_element(By.XPATH, goal_item_xpath)

    def find_table_row_by_number(self, row_num):
        return self.driver.find_element(By.XPATH, f"//tbody/tr[{row_num}]")

    def clear_input(self, input):
        input.send_keys(Keys.CONTROL + "a")
        input.send_keys(Keys.DELETE)
        return self

    def open_create_element_form(self):
        self.wait.until(EC.element_to_be_clickable(self.CREATE_BUTTON))
        self.driver.find_element(*self.CREATE_BUTTON).click()
        self.wait.until(EC.visibility_of_element_located(self.SAVE_BUTTON))
        return self

    def save_form(self, expected_status):
        statuses = {
            "created": self.ELEMENT_CREATED_MESSAGE,
            "updated": self.ELEMENT_UPDATED_MESSAGE,
            "deleted": self.ELEMENT_DELETED_MESSAGE,
            "invalid": self.ELEMENT_INVALID_MESSAGE,
        }
        self.driver.find_element(*self.SAVE_BUTTON).click()
        self.wait.until(EC.visibility_of_element_located(statuses[expected_status]))
        return self

    def get_all_rows(self):
        return self.driver.find_elements(By.XPATH, "//tbody/tr")

    def get_table_title_row(self):
        return self.driver.find_element(By.XPATH, "//thead/tr")

    def get_table_titles(self):
        title_row = self.get_table_title_row()
        titles_elems = title_row.find_elements(By.XPATH, "./th")
        result = []
        for title_elem in titles_elems:
            result.append(title_elem.text)
        return result[1:]

    def select_row_by_number(self, row_number):
        row = self.driver.find_element(By.XPATH, f"//tbody/tr[{row_number}]")
        row.find_element(By.TAG_NAME, "input").click()
        return row

    def select_all_rows(self):
        self.wait.until(EC.presence_of_element_located(self.MAIN_CHECKBOX))
        self.driver.find_element(*self.MAIN_CHECKBOX).click()
        return self

    def delete_elements(self, number_of_elements=1):
        self.wait.until(EC.element_to_be_clickable(self.DELETE_BUTTON))
        self.driver.find_element(*self.DELETE_BUTTON).click()
        if number_of_elements == 1:
            self.wait.until(
                EC.visibility_of_element_located(self.ELEMENT_DELETED_MESSAGE)
            )
        else:
            self.wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, f"//div[text()='{number_of_elements} elements deleted']")
                )
            )
        return self

    def is_visible(self, element):
        return self.wait.until(EC.visibility_of_element_located(element))

    def is_invisible(self, element):
        return self.wait.until(EC.invisibility_of_element(element))

    def is_clickable(self, element):
        return self.wait.until(EC.element_to_be_clickable(element))

    def is_located(self, element):
        return self.wait.until(EC.presence_of_element_located(element))

    def is_not_located(self, element):
        return self.wait.until(EC.invisibility_of_element_located(element))

    def is_not_empty(self, element):
        return bool(element.text)
