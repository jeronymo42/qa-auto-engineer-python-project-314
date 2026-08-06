import logging
import sys
from time import sleep

import pytest
from selenium.webdriver.common.by import By

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
    login_page.is_visible(login_page.LOGIN_BUTTON)
    login_page.is_visible(login_page.USERNAME_INPUT)
    login_page.is_visible(login_page.PASSWORD_INPUT)


@pytest.mark.smoke
def test_login(driver):
    login_page = LoginPage(driver)
    login_page.login('test', 'test')
    assert login_page.is_visible(login_page.PROFILE_BUTTON)
    assert login_page.is_visible(login_page.HEADER)


@pytest.mark.smoke
def test_logout(main_page):
    main_page.logout()
    assert main_page.is_visible(main_page.LOGIN_BUTTON)
    assert main_page.is_visible(main_page.USERNAME_INPUT)
    assert main_page.is_visible(main_page.PASSWORD_INPUT)


def test_open_create_user_form(user_page):
    user_page.open_create_element_form()
    assert user_page.is_visible(user_page.USERS_CREATE_FORM_FIRST_NAME_INPUT)
    assert user_page.is_visible(user_page.USERS_CREATE_FORM_LAST_NAME_INPUT)
    assert user_page.is_visible(user_page.USERS_CREATE_FORM_EMAIL_INPUT)


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
    assert user_page.is_visible(user_page.USERS_TABLE_HEADER_ID)
    assert user_page.is_visible(user_page.USERS_TABLE_HEADER_EMAIL)
    assert user_page.is_visible(user_page.USERS_TABLE_HEADER_FIRST_NAME)
    assert user_page.is_visible(user_page.USERS_TABLE_HEADER_LAST_NAME)
    assert user_page.is_visible(user_page.USERS_TABLE_HEADER_CREATED_AT)


def test_user_edit(user_page):

    TEST_USER_EMAIL = 'test@test.com'
    TEST_USER_FIRST_NAME = 'test'
    TEST_USER_LAST_NAME = 'test'

    user_page.get_user_by_row_number(1).click()
    user_page.edit_user_email(TEST_USER_EMAIL)
    user_page.edit_user_first_name(TEST_USER_FIRST_NAME)
    user_page.edit_user_last_name(TEST_USER_LAST_NAME)
    user_page.save_form('updated')

    user_page.switch_to_users_page()

    user_row = user_page.find_user_row_by_data(1)
    assert user_page.get_user_email(user_row) == TEST_USER_EMAIL
    assert user_page.get_user_first_name(user_row) == TEST_USER_FIRST_NAME
    assert user_page.get_user_last_name(user_row) == TEST_USER_LAST_NAME


def test_user_edit_with_incorrect_email(user_page):
    TEST_USER_EMAIL = 'test'

    user_page.get_user_by_row_number(1).click()
    user_page.edit_user_email(TEST_USER_EMAIL)
    user_page.save_form('invalid')

    user_page.switch_to_users_page()

    user_row = user_page.find_user_row_by_data(1)
    assert user_page.get_user_email(user_row) != TEST_USER_EMAIL


def test_delete_user(user_page):
    user_row = user_page.get_user_by_row_number(1)
    user_email = user_page.get_user_email(user_row)
    user_first_name = user_page.get_user_first_name(user_row)
    user_last_name = user_page.get_user_last_name(user_row)

    user_row.click()
    user_page.delete_elements()

    assert user_page.is_invisible(
        (By.XPATH, f"//td/span[text()='{user_email}']/../.."))
    assert user_page.is_invisible(
        (By.XPATH, f"//td[text()='{user_first_name}']/../.."))
    assert user_page.is_invisible(
        (By.XPATH, f"//td[text()='{user_last_name}']/../.."))


def test_delete_all_users(user_page):
    user_page.select_all_users()
    user_page.delete_elements(8)

    assert user_page.is_visible(
        user_page.NO_USERS_MESSAGE
    )


def test_bulk_delete_users(user_page):
    USERS_DELETE_LIST = [1, 3, 5]
    user_page.select_users(USERS_DELETE_LIST)
    user_page.delete_elements(3)

    for user in USERS_DELETE_LIST:
        assert user_page.is_invisible(
            (By.XPATH, f"//td[text()='{user}']/../..")
        )


def test_open_create_task_form(task_page):
    task_page.open_create_element_form()
    task_page.header_loaded('Create Task')
    assert task_page.is_located(task_page.ASSIGNEE_INPUT)
    assert task_page.is_located(task_page.TITLE_INPUT)
    assert task_page.is_located(task_page.CONTENT_INPUT)
    assert task_page.is_located(task_page.STATUS_INPUT)
    assert task_page.is_located(task_page.LABEL_INPUT)


def test_create_simple_task(task_page):
    TASK_TITLE = 'test'
    task_page.open_create_element_form()
    task_page.fill_task(1, TASK_TITLE, f'Description of task {TASK_TITLE}', 5)
    task_page.save_form('created')
    task_page.switch_to_tasks_page()
    task_page.header_loaded('Tasks')
    assert task_page.find_task_by_title(TASK_TITLE)


def test_visibility_of_tasks_statuses(task_page):
    TASK_STATUSES = ['Draft', 'To Review',
                     'To Be Fixed', 'To Publish', 'Published']
    for status in TASK_STATUSES:
        assert task_page.is_visible((By.XPATH, f"//h6[text()='{status}']"))


def test_cards_title_and_slug(task_page):

    for i in range(1, 16):
        assert task_page.is_visible(
            (By.XPATH, f"//div[@role='button']//div[text()='Task {i}']"))
        assert task_page.is_visible(
            (By.XPATH, f"//div[@role='button']//p[text()='Description of task {i}']"))
