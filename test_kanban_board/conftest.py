from test_kanban_board.config import APP_BASE_URL

import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from pages.login_page import LoginPage
from pages.users_page import UsersPage
from pages.status_page import StatusPage
from pages.tasks_page import TasksPage
from pages.labels_page import LabelsPage


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")  # Запуск без окна браузера
    options.add_argument("--start-fullscreen")
    driver = webdriver.Chrome(options=options)
    driver.get(APP_BASE_URL)
    WebDriverWait(driver, 10).until(EC.title_contains("Task manager"))
    yield driver
    driver.quit()


@pytest.fixture
def main_page(driver):
    login_page = LoginPage(driver)
    login_page.login("SomeTestUser", "@SomeStrongPassword1")
    yield login_page
    driver.quit()


@pytest.fixture
def user_page(main_page):
    users_page = UsersPage(main_page.driver)
    users_page.switch_to_page("users")
    return users_page


@pytest.fixture
def status_page(main_page):
    main_page.switch_to_page("status")
    tasks_page = StatusPage(main_page.driver)
    return tasks_page


@pytest.fixture
def tasks_page(main_page):
    main_page.switch_to_page("tasks")
    tasks_page = TasksPage(main_page.driver)
    return tasks_page


@pytest.fixture
def labels_page(main_page):
    main_page.switch_to_page("labels")
    tasks_page = LabelsPage(main_page.driver)
    return tasks_page
