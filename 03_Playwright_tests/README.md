test_EndToEnd.py

Testovací případ test_EndToEnd.py jsem pojal jako imitaci reálné webové stránky, kdy jsem otestoval uživatelskou journey jen v bezpečném testovacím prostředí stránky https://the-internet.herokuapp.com.Testy jsou po úpravě rozděleny do třech samostatných testů, aby byly jednodušší na údržbu a debugging. Test prochází přihlášením uživatele, vybráním možnosti v dropdown až po výběr v checkboxu imitující například nastavení filtrace.

test_FAQ.py

Testovací případ jsem nechtěl pojmout jen jako proklikávání se stránkou, proto jsem do scriptu zakomponoval podmínku, která ověřuje, že po najetí na téma v rámci FAQ stránky, se změní barva pozadí. Vyzkoušel jsem si zde možnost, jak by mohlo vypadat testování vizuální stránky webu.

test_SignIn.py

Testovací případ je z z těchto tří testů nejjednodušší, ale chtěl jsem zde vyzkoušet, jak se testuje negativní testovací případ. 

U všech tří testovacích souborů využívám pomocný soubor conftest.py, ve kterém je fixture pro vytvoření prohlížeče a nového okna prohlížeče. Navíc jsem se naučil způsob, jak otestovat všechny tři varianty prohlížečů díky nepřímé parametrizaci. Také jsem se díky tomu naučil pracovat s variantou hook, která automaticky doplňuje parametry do každé spuštěné funkce v rámci složky. Díky tomu nemusí být u každého testu parametrizace.
