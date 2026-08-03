import logging
import sys

import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.login_page import LoginPage


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
    force=True,
)
logger = logging.getLogger(__name__)


def build_screenshot_path(base_url: str, test_name: str) -> str:
    safe_base_url = (
        base_url.replace("http://", "http_")
        .replace("https://", "https_")
        .replace(":", "_")
        .strip('/')
        .replace("/", "_")
    )
    safe_test_name = test_name.replace(" ", "_")
    return f"screenshots/failure_{safe_base_url}_{safe_test_name}.png"


@pytest.mark.smoke
def test_base_functionality(driver):
    login_page = LoginPage(driver)
    assert 'Task manager' in driver.title
    wait = WebDriverWait(driver, 10)
    assert wait.until(EC.visibility_of_element_located(
        login_page.USERNAME_INPUT)), "Username input not found"
    assert wait.until(EC.visibility_of_element_located(
        login_page.PASSWORD_INPUT)), "Password input not found"
    assert wait.until(EC.visibility_of_element_located(
        login_page.LOGIN_BUTTON)), "Login button not found"
