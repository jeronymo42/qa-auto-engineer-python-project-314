import pytest
from selenium.webdriver.common.by import By

from pages.login_page import LoginPage
from pages.users_page import UsersPage
from pages.status_page import StatusPage
from pages.tasks_page import TasksPage
from pages.labels_page import LabelsPage


@pytest.mark.smoke
def test_base_functionality(driver):
    login_page = LoginPage(driver)
    assert "Task manager" in driver.title
    login_page.is_visible(login_page.LOGIN_BUTTON)
    login_page.is_visible(login_page.USERNAME_INPUT)
    login_page.is_visible(login_page.PASSWORD_INPUT)


@pytest.mark.smoke
def test_login(driver):
    login_page = LoginPage(driver)
    login_page.login("test", "test")
    assert login_page.is_visible(login_page.PROFILE_BUTTON)
    assert login_page.is_visible(login_page.HEADER)


@pytest.mark.smoke
def test_logout(main_page):
    main_page.logout()
    assert main_page.is_visible(main_page.LOGIN_BUTTON)
    assert main_page.is_visible(main_page.USERNAME_INPUT)
    assert main_page.is_visible(main_page.PASSWORD_INPUT)


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

    user_page.create_user(TEST_USER_EMAIL, TEST_USER_FIRST_NAME, TEST_USER_LAST_NAME)

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

    assert user_page.is_invisible((By.XPATH, f"//td/span[text()='{user_email}']/../.."))
    assert user_page.is_invisible((By.XPATH, f"//td[text()='{user_first_name}']/../.."))
    assert user_page.is_invisible((By.XPATH, f"//td[text()='{user_last_name}']/../.."))


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
        assert user_page.is_invisible((By.XPATH, f"//td[text()='{user}']/../.."))


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
