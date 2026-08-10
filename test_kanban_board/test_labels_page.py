import pytest

from selenium.webdriver.common.by import By

from pages.labels_page import LabelsPage


@pytest.mark.labels
def test_open_create_label_form(labels_page: LabelsPage):
    labels_page.open_create_element_form()
    labels_page.header_loaded("Create Label")
    assert labels_page.is_located(labels_page.CREATE_FORM_LABEL_NAME_INPUT)
    assert labels_page.is_located(labels_page.SAVE_BUTTON)


@pytest.mark.labels
def test_create_simple_label(labels_page: LabelsPage):
    LABEL_TITLE = "test"
    labels_page.open_create_element_form()
    labels_page.edit_label_name(LABEL_TITLE)
    labels_page.save_form("created")
    labels_page.switch_to_page("labels")
    labels_page.header_loaded("Labels")
    assert labels_page.find_table_row_by_data("Labels", LABEL_TITLE)


@pytest.mark.labels
def test_labels_list_display(labels_page: LabelsPage):
    TABLE_HEADERS = ["Id", "Name", "Created at"]
    table_headers = labels_page.get_table_titles()
    assert TABLE_HEADERS == table_headers

    table_rows = labels_page.get_all_rows()
    assert len(table_rows) == 5
    for table_row in table_rows:
        assert labels_page.is_not_empty(table_row)


@pytest.mark.labels
def test_edit_label(labels_page: LabelsPage):
    OLD_NAME = "enhancement"
    NEW_NAME = "_test"
    goal_row = labels_page.find_table_row_by_data("Labels", OLD_NAME)
    goal_row.click()
    labels_page.edit_label_name(OLD_NAME + NEW_NAME)
    labels_page.save_form("updated")
    labels_page.switch_to_page("labels")
    assert labels_page.find_table_row_by_data("Labels", OLD_NAME + NEW_NAME)


@pytest.mark.labels
def test_delete_label(labels_page: LabelsPage):
    test_row_1 = labels_page.find_table_row_by_number(1)
    old_name_1 = labels_page.get_label_name_from_row(test_row_1)
    labels_page.select_row_by_number(1)
    labels_page.delete_elements()
    assert labels_page.is_invisible((By.XPATH, f"//td[text()='{old_name_1}']"))
