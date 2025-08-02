import pytest

def test_SignIn_Positive(new_page):
    new_page.goto("https://the-internet.herokuapp.com/")

    #Přejití na stránku s přihlášením
    login_page = new_page.locator("[href='/login']")
    login_page.click()

    #Vyplnění správných přihlašovacích údajů
    user_name = new_page.locator("input#username").fill("tomsmith")
    password = new_page.locator("input#password").fill("SuperSecretPassword!")

    #Potvrzení přihlášení
    login_button = new_page.locator(".radius")
    login_button.click()

    assert new_page.url == "https://the-internet.herokuapp.com/secure"

def test_SignIn_Negative(new_page):
    new_page.goto("https://the-internet.herokuapp.com/")

    #Přejití na stránku s přihlášením
    login_page = new_page.locator("[href='/login']")
    login_page.click()

    #Vyplnění nesprávného přihlašovacího údaje
    user_name = new_page.locator("input#username").fill("tomsmith")
    password = new_page.locator("input#password").fill("IncorrectPassword")#správné heslo: SuperSecretPassword!

    #Potvrzení přihlášení
    login_button = new_page.locator(".radius")
    login_button.click()

    error_message = new_page.locator(".flash.error")
    assert error_message.is_visible()
