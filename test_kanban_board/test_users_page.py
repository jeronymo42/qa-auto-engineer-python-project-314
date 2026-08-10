import pytest

from selenium.webdriver.common.by import By

from pages.users_page import UsersPage


@pytest.mark.users
def test_open_create_user_form(user_page: UsersPage):
    user_page.open_create_element_form()
    assert user_page.is_visible(user_page.USERS_CREATE_FORM_FIRST_NAME_INPUT)
    assert user_page.is_visible(user_page.USERS_CREATE_FORM_LAST_NAME_INPUT)
    assert user_page.is_visible(user_page.USERS_CREATE_FORM_EMAIL_INPUT)


@pytest.mark.users
def test_new_user_create(user_page: UsersPage):
    TEST_USER_EMAIL = "test@test.com"
    TEST_USER_FIRST_NAME = "test"
    TEST_USER_LAST_NAME = "test"

    user_page.create_user(
        TEST_USER_EMAIL, TEST_USER_FIRST_NAME, TEST_USER_LAST_NAME)

    user_page.switch_to_page("users")

    user_row = user_page.find_table_row_by_data(
        page_header="Users", data=TEST_USER_EMAIL
    )
    assert user_page.get_user_first_name(user_row) == TEST_USER_FIRST_NAME
    assert user_page.get_user_last_name(user_row) == TEST_USER_LAST_NAME
    assert user_page.get_user_email(user_row) == TEST_USER_EMAIL


@pytest.mark.users
def test_users_table_displayed_correct(user_page: UsersPage):
    assert user_page.is_visible(user_page.USERS_TABLE_HEADER_ID)
    assert user_page.is_visible(user_page.USERS_TABLE_HEADER_EMAIL)
    assert user_page.is_visible(user_page.USERS_TABLE_HEADER_FIRST_NAME)
    assert user_page.is_visible(user_page.USERS_TABLE_HEADER_LAST_NAME)
    assert user_page.is_visible(user_page.USERS_TABLE_HEADER_CREATED_AT)


@pytest.mark.users
def test_user_edit(user_page: UsersPage):

    TEST_USER_EMAIL = "test@test.com"
    TEST_USER_FIRST_NAME = "test"
    TEST_USER_LAST_NAME = "test"

    user_page.find_table_row_by_data("Users", 1).click()
    user_page.edit_user_email(TEST_USER_EMAIL)
    user_page.edit_user_first_name(TEST_USER_FIRST_NAME)
    user_page.edit_user_last_name(TEST_USER_LAST_NAME)
    user_page.save_form("updated")

    user_page.switch_to_page("users")

    user_row = user_page.find_table_row_by_data(page_header="Users", data=1)
    assert user_page.get_user_email(user_row) == TEST_USER_EMAIL
    assert user_page.get_user_first_name(user_row) == TEST_USER_FIRST_NAME
    assert user_page.get_user_last_name(user_row) == TEST_USER_LAST_NAME


@pytest.mark.users
def test_user_edit_with_incorrect_email(user_page: UsersPage):
    TEST_USER_EMAIL = "test"

    user_page.find_table_row_by_data("Users", 1).click()
    user_page.edit_user_email(TEST_USER_EMAIL)
    user_page.save_form("invalid")

    user_page.switch_to_page("users")

    user_row = user_page.find_table_row_by_data(page_header="Users", data=1)
    assert user_page.get_user_email(user_row) != TEST_USER_EMAIL


@pytest.mark.users
def test_delete_user(user_page: UsersPage):
    user_row = user_page.find_table_row_by_data("Users", 1)
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


@pytest.mark.users
def test_delete_all_users(user_page: UsersPage):
    user_page.select_all_rows()
    user_page.delete_elements(8)

    assert user_page.is_visible(user_page.NO_USERS_MESSAGE)


@pytest.mark.users
def test_bulk_delete_users(user_page: UsersPage):
    USERS_DELETE_LIST = [1, 3, 5]
    user_page.select_users(USERS_DELETE_LIST)
    user_page.delete_elements(3)

    for user in USERS_DELETE_LIST:
        assert user_page.is_invisible(
            (By.XPATH, f"//td[text()='{user}']/../.."))
