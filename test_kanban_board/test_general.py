import logging
import sys
from time import sleep

import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from pages.login_page import LoginPage
from pages.main_page import MainPage


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


@pytest.mark.smoke
def test_login(driver):
    login_page = LoginPage(driver)
    login_page.login('test', 'test')
    main_page = MainPage(login_page.driver)
    wait = WebDriverWait(main_page.driver, 10)
    assert wait.until(EC.visibility_of_element_located(
        main_page.PROFILE_BUTTON)), "Profile button not found"
    assert wait.until(EC.visibility_of_element_located(
        main_page.HEADER)), "Board header not found"


@pytest.mark.smoke
def test_logout(main_page: MainPage):
    main_page.logout()
    login_page = LoginPage(main_page.driver)
    wait = WebDriverWait(main_page.driver, 10)
    assert wait.until(EC.visibility_of_element_located(
        login_page.USERNAME_INPUT)), "Username input not found"
    assert wait.until(EC.visibility_of_element_located(
        login_page.PASSWORD_INPUT)), "Password input not found"
    assert wait.until(EC.visibility_of_element_located(
        login_page.LOGIN_BUTTON)), "Login button not found"


def test_open_create_user_form(user_page):
    user_page.open_create_user_form()
    assert user_page.driver.find_element(
        *user_page.USERS_CREATE_FORM_FIRST_NAME_INPUT).is_displayed()
    assert user_page.driver.find_element(
        *user_page.USERS_CREATE_FORM_LAST_NAME_INPUT).is_displayed()
    assert user_page.driver.find_element(
        *user_page.USERS_CREATE_FORM_EMAIL_INPUT).is_displayed()
    sleep(2)


def test_new_user_create(user_page):
    TEST_USER_EMAIL = 'test@test.com'
    TEST_USER_FIRST_NAME = 'test'
    TEST_USER_LAST_NAME = 'test'

    user_page.create_user(
        TEST_USER_EMAIL, TEST_USER_FIRST_NAME, TEST_USER_LAST_NAME)

    user_page.switch_to_users_page()

    user_row = user_page.find_user_row_by_data(TEST_USER_EMAIL)
    assert user_page.get_user_first_name(user_row) == TEST_USER_FIRST_NAME
    assert user_page.get_user_last_name(user_row) == TEST_USER_LAST_NAME
    assert user_page.get_user_email(user_row) == TEST_USER_EMAIL


def test_users_table_displayed_correct(user_page):
    assert user_page.driver.find_element(
        *user_page.USERS_TABLE_HEADER_ID).is_displayed()
    assert user_page.driver.find_element(
        *user_page.USERS_TABLE_HEADER_EMAIL).is_displayed()
    assert user_page.driver.find_element(
        *user_page.USERS_TABLE_HEADER_FIRST_NAME).is_displayed()
    assert user_page.driver.find_element(
        *user_page.USERS_TABLE_HEADER_LAST_NAME).is_displayed()
    assert user_page.driver.find_element(
        *user_page.USERS_TABLE_HEADER_CREATED_AT).is_displayed()


def test_user_edit(user_page):

    TEST_USER_EMAIL = 'test@test.com'
    TEST_USER_FIRST_NAME = 'test'
    TEST_USER_LAST_NAME = 'test'

    user_page.get_user_by_row_number(1).click()
    user_page.edit_user_email(TEST_USER_EMAIL)
    user_page.edit_user_first_name(TEST_USER_FIRST_NAME)
    user_page.edit_user_last_name(TEST_USER_LAST_NAME)
    user_page.save_user('updated')

    user_page.switch_to_users_page()

    user_row = user_page.find_user_row_by_data(1)
    assert user_page.get_user_email(user_row) == TEST_USER_EMAIL
    assert user_page.get_user_first_name(user_row) == TEST_USER_FIRST_NAME
    assert user_page.get_user_last_name(user_row) == TEST_USER_LAST_NAME


def test_user_edit_with_incorrect_email(user_page):
    TEST_USER_EMAIL = 'test'

    user_page.get_user_by_row_number(1).click()
    user_page.edit_user_email(TEST_USER_EMAIL)
    user_page.save_user('invalid')

    user_page.switch_to_users_page()

    user_row = user_page.find_user_row_by_data(1)
    assert user_page.get_user_email(user_row) != TEST_USER_EMAIL


def test_delete_user(user_page):
    user_row = user_page.get_user_by_row_number(1)
    user_email = user_page.get_user_email(user_row)
    user_first_name = user_page.get_user_first_name(user_row)
    user_last_name = user_page.get_user_last_name(user_row)

    user_row.click()
    user_page.delete_users()

    assert user_page.wait.until(EC.invisibility_of_element_located(
        (By.XPATH, f"//td/span[text()='{user_email}']/../..")
    ))
    assert user_page.wait.until(EC.invisibility_of_element_located(
        (By.XPATH, f"//td[text()='{user_first_name}']/../..")
    ))
    assert user_page.wait.until(EC.invisibility_of_element_located(
        (By.XPATH, f"//td[text()='{user_last_name}']/../..")
    ))


def test_delete_all_users(user_page):
    user_page.select_all_users()
    user_page.delete_users(8)

    assert user_page.wait.until(EC.visibility_of_element_located(
        user_page.NO_USERS_MESSAGE
    ))


def test_bulk_delete_users(user_page):
    USERS_DELETE_LIST = [1, 3, 5]
    user_page.select_users(USERS_DELETE_LIST)
    user_page.delete_users(3)

    for user in USERS_DELETE_LIST:
        assert user_page.wait.until(EC.invisibility_of_element_located(
            (By.XPATH, f"//td[text()='{user}']/../..")
        ))
