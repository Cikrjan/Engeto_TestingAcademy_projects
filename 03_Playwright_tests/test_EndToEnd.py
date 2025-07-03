import pytest
from playwright.sync_api import expect, Page

#Přihlášení se do systému
def test_SignIn(new_page):

    new_page.goto("https://the-internet.herokuapp.com/")
    sign_in = new_page.locator("[href='/login']").click()
    user_name = new_page.locator("input#username").fill("tomsmith")
    password = new_page.locator("input#password").fill("SuperSecretPassword!")
    login_button = new_page.locator(".radius").click()
    assert new_page.url == "https://the-internet.herokuapp.com/secure"

#Výběr položky v dropdown
def test_Dropdown(new_page):
    new_page.goto("https://the-internet.herokuapp.com/")
    dropdown_new_page = new_page.locator("[href='/dropdown']").click()
    dropdown_click = new_page.locator("#dropdown")
    dropdown_click.select_option("1")
    choice = dropdown_click.locator("option[value='1']")
    expect(choice).to_have_attribute("selected", "selected") #Ověření, že byla vybrána první možnost
    expect(choice).to_have_text("Option 1")
    
#Zakliknutí checkboxu
def test_Checkbox(new_page):
    new_page.goto("https://the-internet.herokuapp.com/")
    checkbox_new_page = new_page.locator("[href='/checkboxes']").click()
    checkbox_menu = new_page.locator("#checkboxes")
    checkbox_1 = checkbox_menu.locator("input[type='checkbox']").nth(0)
    checkbox_2 = checkbox_menu.locator("input[type='checkbox']").nth(1)

    checkbox_1.click()
    checkbox_2.click()

    assert checkbox_1.is_checked()
    assert not checkbox_2.is_checked()
    