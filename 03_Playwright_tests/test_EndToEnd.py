import pytest
from playwright.sync_api import sync_playwright, Page

@pytest.fixture(scope='function', autouse=True)
def new_page(request):
    browser_name = request.param
    with sync_playwright() as p:
        browser_type = getattr(p, browser_name)
        browser = browser_type.launch(headless=False, slow_mo=500)
        page = browser.new_page()
        yield page
        page.close()

@pytest.mark.parametrize("new_page", ["chromium", "firefox", "webkit"], indirect=True)
def test_MultipleTests(new_page: new_page):
    new_page.goto("https://the-internet.herokuapp.com/")

    #Přihlášení se do systému
    sign_in = new_page.locator("[href='/login']").click()
    user_name = new_page.locator("input#username").fill("tomsmith")
    password = new_page.locator("input#password").fill("SuperSecretPassword!")
    login_button = new_page.locator(".radius").click()
    assert new_page.url == "https://the-internet.herokuapp.com/secure"

    new_page.wait_for_timeout(500)

    #Výběr položky v dropdown
    new_page.goto("https://the-internet.herokuapp.com/")
    dropdown_new_page = new_page.locator("[href='/dropdown']").click()
    dropdown_click = new_page.locator("#dropdown")
    dropdown_click.select_option("1")
    choice = dropdown_click.locator("option[value='1']")
    assert choice.evaluate("el => el.selected") is True
    assert choice.inner_text() == "Option 1"

    new_page.wait_for_timeout(500)

    #Zakliknutí checkboxu - imitace výběru položek ve filtru
    new_page.goto("https://the-internet.herokuapp.com/")
    checkbox_new_page = new_page.locator("[href='/checkboxes']").click()
    checkbox_menu = new_page.locator("#checkboxes")
    checkbox_1 = checkbox_menu.locator("input[type='checkbox']").nth(0)
    checkbox_2 = checkbox_menu.locator("input[type='checkbox']").nth(1)

    checkbox_1.click()
    checkbox_2.click()

    assert checkbox_1.is_checked()
    assert not checkbox_2.is_checked()

#



    