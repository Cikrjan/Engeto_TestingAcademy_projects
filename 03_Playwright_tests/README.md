test_EndToEnd.py
Testovací případ test_EndToEnd.py jsem pojal jako imitaci reálné webové stránky, kdy jsem otestoval uživatelskou journey jen v bezpečném testovacím prostředí stránky https://the-internet.herokuapp.com. To je důvod, proč jsou všechny testy v jedné funkci. Test prochází přihlášením uživatele, vybráním možnosti v dropdown až po výběr v checkboxu imitující například nastavení filtrace.

test_FAQ.py
Testovací případ jsem nechtěl pojmout jen jako proklikávání se stránkou, proto jsem do scriptu zakomponoval podmínku, která ověřuje, že po najetí na téma v rámci FAQ stránky, se změní barva pozadí. Vyzkoušel jsem si zde možnost, jak by mohlo vypadat testování vizuální stránky webu.

test_SignIn.py
Testovací případ je z z těchto tří testů nejjednodušší, ale chtěl jsem zde vyzkoušet, jak se testuje negativní testovací případ. 

U všech tří testovacích souborů využívám pomocný soubor conftest.py, ve kterém je fixture pro vytvoření prohlížeče a nového okna prohlížeče. Navíc jsem se naučil způsob, jak otestovat všechny tři varianty prohlížečů díky nepřímé parametrizaci.
V souborech test_EndToEnd.py a test_FAQ.py používám syntaxe z JavaScriptu, které mi napomohly k požadovanému výsledku testu.
