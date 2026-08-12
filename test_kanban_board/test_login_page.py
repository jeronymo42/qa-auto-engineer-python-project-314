import pytest

from pages.login_page import LoginPage


@pytest.mark.smoke
def test_base_functionality(driver):
    login_page = LoginPage(driver)
    assert "Task manager" in driver.title
    assert login_page.is_visible(login_page.LOGIN_BUTTON)
    assert login_page.is_visible(login_page.USERNAME_INPUT)
    assert login_page.is_visible(login_page.PASSWORD_INPUT)


@pytest.mark.smoke
def test_login(driver):
    login_page = LoginPage(driver)
    login_page.login("test", "test")
    assert login_page.is_visible(login_page.PROFILE_BUTTON)
    assert login_page.is_visible(login_page.HEADER)


@pytest.mark.smoke
def test_logout(main_page: LoginPage):
    main_page.logout()
    assert main_page.is_visible(main_page.LOGIN_BUTTON)
    assert main_page.is_visible(main_page.USERNAME_INPUT)
    assert main_page.is_visible(main_page.PASSWORD_INPUT)
