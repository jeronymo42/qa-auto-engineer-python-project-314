from config import APP_BASE_URL

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from pages.login_page import LoginPage
from pages.main_page import MainPage


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
    main_page = MainPage(driver)
    yield main_page
    driver.quit()
