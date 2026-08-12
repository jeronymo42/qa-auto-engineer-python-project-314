import pytest

from selenium.webdriver.common.by import By

from pages.status_page import StatusPage


@pytest.mark.status
def test_open_create_status_form(status_page: StatusPage):
    status_page.open_create_element_form()
    status_page.header_loaded("Create Task status")
    assert status_page.is_located(status_page.CREATE_FORM_NAME_INPUT)
    assert status_page.is_located(status_page.CREATE_FORM_SLUG_INPUT)
    assert status_page.is_located(status_page.SAVE_BUTTON)


@pytest.mark.status
def test_create_new_status(status_page: StatusPage):
    TEST_STATUS = ["Test Name", "test-slug"]
    status_page.create_status(*TEST_STATUS)
    status_page.switch_to_page("status")
    status_page.header_loaded("Task statuses")
    goal_row = status_page.find_table_row_by_data("Task statuses", TEST_STATUS[0])

    assert status_page.get_name_from_row(goal_row) == TEST_STATUS[0]
    assert status_page.get_slug_from_row(goal_row) == TEST_STATUS[1]


@pytest.mark.status
def test_check_statuses_display(status_page: StatusPage):
    STATUSES = ["Draft", "To Review", "To Be Fixed", "To Publish", "Published"]

    for status in STATUSES:
        goal_row = status_page.find_table_row_by_data("Task statuses", status)

        assert status_page.get_name_from_row(goal_row) == status


@pytest.mark.status
def test_name_and_slug_headers(status_page: StatusPage):
    assert status_page.is_visible(status_page.NAME_HEADER)
    assert status_page.is_visible(status_page.SLUG_HEADER)


@pytest.mark.status
def test_edit_status(status_page: StatusPage):
    OLD_NAME = "To Publish"
    OLD_SLUG = "to_publish"
    NEW_NAME = "Picked"
    NEW_SLUG = "test"
    goal_row = status_page.find_table_row_by_data("Task statuses", OLD_NAME)
    assert status_page.get_name_from_row(goal_row) == OLD_NAME
    assert status_page.get_slug_from_row(goal_row) == OLD_SLUG

    goal_row.click()

    status_page.fill_form(NEW_NAME, NEW_SLUG)
    status_page.save_form("updated")

    status_page.switch_to_page("status")
    goal_row = status_page.find_table_row_by_data("Task statuses", NEW_NAME)
    assert status_page.get_name_from_row(goal_row) == NEW_NAME
    assert status_page.get_slug_from_row(goal_row) == NEW_SLUG


@pytest.mark.status
def test_delete_status(status_page: StatusPage):
    test_row_1 = status_page.select_row_by_number(1)
    old_name_1 = status_page.get_name_from_row(test_row_1)
    old_slug_1 = status_page.get_slug_from_row(test_row_1)

    test_row_2 = status_page.select_row_by_number(3)
    old_name_2 = status_page.get_name_from_row(test_row_2)
    old_slug_2 = status_page.get_slug_from_row(test_row_2)

    status_page.delete_elements(2)
    assert status_page.is_invisible((By.XPATH, f"//td[text()='{old_name_1}']/../.."))
    assert status_page.is_invisible((By.XPATH, f"//td[text()='{old_slug_1}']/../.."))
    assert status_page.is_invisible((By.XPATH, f"//td[text()='{old_name_2}']/../.."))
    assert status_page.is_invisible((By.XPATH, f"//td[text()='{old_slug_2}']/../.."))


@pytest.mark.status
def test_bulk_delete_status(status_page: StatusPage):
    status_page.select_all_rows()
    status_page.delete_elements(5)
    assert status_page.is_visible(status_page.NO_STATUS_MESSAGE)
