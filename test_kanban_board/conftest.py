from config import APP_BASE_URL

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from pages.login_page import LoginPage
from pages.users_page import UsersPage
from pages.tasks_page import TasksPage


@pytest.fixture
def driver():
    options = Options()
    # options.add_argument("--headless")  # Запуск без окна браузера
    # options.add_argument("--start-fullscreen")
    driver = webdriver.Chrome(options=options)
    driver.get(APP_BASE_URL)
    yield driver
    driver.quit()


@pytest.fixture
def main_page(driver):
    login_page = LoginPage(driver)
    login_page.login('test', 'test')
    yield login_page
    driver.quit()


@pytest.fixture
def user_page(main_page):
    users_page = UsersPage(main_page.driver)
    users_page.switch_to_users_page()
    return users_page


@pytest.fixture
def task_page(main_page):
    main_page.switch_to_tasks_page()
    tasks_page = TasksPage(main_page.driver)
    return tasks_page
