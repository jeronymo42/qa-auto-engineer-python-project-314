from config import APP_BASE_URL

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture
def driver():
    options = Options()
    # options.add_argument("--headless")  # Запуск без окна браузера
    driver = webdriver.Chrome(options=options)
    driver.fullscreen_window()
    driver.get(APP_BASE_URL)
    yield driver
    driver.quit()
