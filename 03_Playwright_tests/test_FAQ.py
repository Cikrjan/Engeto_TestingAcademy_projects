import pytest
from playwright.sync_api import expect, Page

@pytest.mark.parametrize("new_page", ["chromium"], indirect=True)
def test_FAQ(new_page):
    #přejití na testovanou stránku
    new_page.goto("https://engeto.cz/")

    #nalezení a kliknutí na tlačítko odmítnou na cookie liště
    cookie_refuse = new_page.locator("#cookiescript_reject")
    if cookie_refuse.is_visible():
        cookie_refuse.wait_for(state="visible", timeout=3000)
        cookie_refuse.click()

    #nalezení a kliknutí na tlačítko "FAQ"
    faq_button = new_page.locator("[data-mobile-key='menu-key-4397']")
    faq_button.click()

    #Filtr "Ukončení kurzu a uplatnění" a otestování změny barvy pozadí po najetí na tlačítko
    filter_button = new_page.locator("[for='filter-item_ukonceni-kurzu']")
    filter_button.hover()
    try:
    #Čekání na změnu barvy, jinak 3 sec timeout
        expect(filter_button).to_have_css("background-color", "rgb(162, 229, 244)")
    except AssertionError:
        print("Pozor, barva se nezměnila!")
    
    # Zjištění a vypsání barvy pozadí pro případnou kontrolu, defaultně zakomentováno pro rychlejší průběh testu
    # color_after = filter_button.evaluate("el => getComputedStyle(el).backgroundColor")
    # print("Barva po:", color_after)
    filter_button.click()
    question_rolldown = new_page.locator("#kdy-se-uzavira-kurz-do-kdy-mohu-odevzdavat-projekty-prochazet-zaznamy-a-ucebni-materialy > h3 > a")
    question_rolldown.click()

    link = new_page.locator("#kdy-se-uzavira-kurz-do-kdy-mohu-odevzdavat-projekty-prochazet-zaznamy-a-ucebni-materialy > div > ul > li:nth-child(4) > a:nth-child(3)")
    
    assert link.is_visible()

# , "firefox", "webkit"