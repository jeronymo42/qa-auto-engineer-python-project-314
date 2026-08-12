import pytest
from selenium.webdriver.common.by import By

from pages.tasks_page import TasksPage


@pytest.mark.smoke
@pytest.mark.tasks
def test_open_create_task_form(tasks_page: TasksPage):
    tasks_page.open_create_element_form()
    tasks_page.header_loaded("Create Task")
    assert tasks_page.is_located(tasks_page.ASSIGNEE_INPUT)
    assert tasks_page.is_located(tasks_page.TITLE_INPUT)
    assert tasks_page.is_located(tasks_page.CONTENT_INPUT)
    assert tasks_page.is_located(tasks_page.STATUS_INPUT)
    assert tasks_page.is_located(tasks_page.LABEL_INPUT)


@pytest.mark.smoke
@pytest.mark.tasks
def test_create_simple_task_status(tasks_page: TasksPage):
    TASK_TITLE = "New Task"
    ASSIGNEE = "emily@example.com"
    STATUS = "To Be Fixed"
    tasks_page.open_create_element_form()
    tasks_page.fill_task(
        ASSIGNEE, TASK_TITLE, f"Description of task {TASK_TITLE}", STATUS
    )
    tasks_page.save_form("created")
    tasks_page.switch_to_page("tasks")
    tasks_page.header_loaded("Tasks")
    assert tasks_page.find_task_by_title(TASK_TITLE)
    goal_column = tasks_page.find_column_by_name(STATUS)
    assert tasks_page.find_task_in_column(TASK_TITLE, goal_column)


@pytest.mark.smoke
@pytest.mark.tasks
def test_visibility_of_statuses(tasks_page: TasksPage):
    TASK_STATUSES = ["Draft", "To Review", "To Be Fixed", "To Publish", "Published"]
    for status in TASK_STATUSES:
        assert tasks_page.is_visible((By.XPATH, f"//h6[text()='{status}']"))


@pytest.mark.smoke
@pytest.mark.tasks
def test_cards_title_and_slug(tasks_page: TasksPage):

    for i in range(1, 16):
        assert tasks_page.is_visible(
            (By.XPATH, f"//div[@role='button']//div[text()='Task {i}']")
        )
        assert tasks_page.is_visible(
            (By.XPATH, f"//div[@role='button']//p[text()='Description of task {i}']")
        )


@pytest.mark.tasks
def test_cards_filters(tasks_page: TasksPage):
    tasks_page.filter_by("assignee", "john@google.com")
    assert tasks_page.count_cards() == 5
    tasks_page.clear_filter("assignee")
    tasks_page.filter_by("status", "To Be Fixed")
    assert tasks_page.count_cards() == 3
    tasks_page.clear_filter("status")
    tasks_page.filter_by("label", "bug")
    assert tasks_page.count_cards() == 2


@pytest.mark.tasks
def test_edit_task(tasks_page: TasksPage):
    OLD_TITLE = "Task 1"
    NEW_TITLE = "Task 1 edited"

    tasks_page.edit_task_title(OLD_TITLE, NEW_TITLE)
    assert tasks_page.find_task_by_title(NEW_TITLE)


@pytest.mark.tasks
def test_change_task_status(tasks_page: TasksPage):
    TASK_TITLE = "Task 5"
    COLUMN_NAME = "To Be Fixed"
    tasks_page.change_status(TASK_TITLE, COLUMN_NAME)
    assert tasks_page.is_task_in_column(TASK_TITLE, COLUMN_NAME)


@pytest.mark.tasks
def test_delete_task(tasks_page: TasksPage):
    TITLE = "Task 6"
    tasks_page.delete_task(TITLE)
    assert tasks_page.is_not_located(
        (By.XPATH, f"//div[@role='button']//div[text()='{TITLE}']")
    )
