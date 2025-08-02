import pytest
import mysql.connector
from test_init import vytvoreni_test_tabulky
from Improved_Task_manager import pridat_ukol, aktualizovat_ukol, odstranit_ukol

#scope dávám "session", protože chci, aby tato fixture fungovala po celou délku testování
@pytest.fixture(scope="session", autouse=True) 
def vytvoreni_test_db():
    vytvoreni_test_tabulky()

#tady chci scope jen "module" tak, aby se fixture používala jen v daném souboru
@pytest.fixture(scope="module")
def pripojeni():
    conn = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "1111",
        database = "taskmanager_test"
    )
    yield conn
    conn.close()

def test_pridat_ukol_pozitivni(pripojeni):
    #přidám úkol do databáze skrze funkci z hlavního skriptu
    pridat_ukol(pripojeni, "Test_nazev", "Test_popis")

    #vyberu si v databázi záznam přidaného úkolu a uložím si ho do proměnné
    kurzor = pripojeni.cursor()
    kurzor.execute("SELECT * FROM ukoly WHERE Nazev_ukolu = %s AND Popis_ukolu = %s", ("Test_nazev", "Test_popis"))
    vysledek = kurzor.fetchone()

    #Úklid
    kurzor.execute("DELETE FROM ukoly WHERE UkolId = %s", (vysledek[0],))
    pripojeni.commit()
    kurzor.close()
    
    assert vysledek is not None

def test_pridat_ukol_negativni(pripojeni): #tato funkce testuje, zda je ošetřen vstup při zadání prázdného stringu.
    #přidám úkol do databáze skrze funkci z hlavního skriptu
    pridat_ukol(pripojeni, "", "Test_popis")

    #vyberu si v databázi záznam přidaného úkolu a uložím si ho do proměnné
    kurzor = pripojeni.cursor()
    kurzor.execute("SELECT * FROM ukoly WHERE Nazev_ukolu = '' AND Popis_ukolu = %s", ("Test_popis",))
    vysledek = kurzor.fetchone()

    #pokud se záznam do databáze přidal, vymažeme ho, aby tabulka zůstala prázdná pro další testy
    if vysledek:
        kurzor.execute("DELETE FROM ukoly WHERE UkolID = %s", (vysledek[0],))
        pripojeni.commit()

    kurzor.close()
    
    #očekávám, že test selže, protože se špatně uložený záznam našel
    assert vysledek is None

def test_aktualizovat_ukol_pozitivni(pripojeni):
    #přidám úkol do databáze skrze funkci z hlavního skriptu
    pridat_ukol(pripojeni, "Test_nazev", "Test_popis")

    #vyhledám si ID přidaného úkolu v databázi, protože nemůžu předpokládat, že ID bude vždy 1 (zvlášť když je tabulka nastavená na AUTOINCREMENT)
    kurzor = pripojeni.cursor()
    kurzor.execute("SELECT UkolID FROM ukoly WHERE Nazev_ukolu = %s AND Popis_ukolu = %s", ("Test_nazev", "Test_popis"))
    ukolID = kurzor.fetchone()[0]

    #aktualizuji záznam v databázi skrze funkci z hlavního skriptu
    aktualizovat_ukol(pripojeni, ukolID, "Probíhá")

    #uložím si záznam do proměnné
    kurzor.execute("SELECT * FROM ukoly WHERE UkolID = %s", (ukolID,))
    vysledek = kurzor.fetchone()

    #Úklid
    kurzor.execute("DELETE FROM ukoly WHERE UkolID = %s", (ukolID,))
    pripojeni.commit()
    kurzor.close()

    assert vysledek[3] == "Probíhá"

def test_aktualizovat_ukol_negativni(pripojeni):
    #přidám úkol do databáze skrze funkci z hlavního skriptu
    pridat_ukol(pripojeni, "Test_nazev", "Test_popis")

    #očekávám, že v případě zadání neexistujícího ID vyskočí ValueError
    with pytest.raises(ValueError):
        aktualizovat_ukol(pripojeni, 5, "Probíhá")

    #Úklid
    kurzor = pripojeni.cursor()
    kurzor.execute("DELETE FROM ukoly WHERE Nazev_ukolu = 'Test_nazev'")
    pripojeni.commit()
    kurzor.close()

def test_odstranit_ukol_pozitivni(pripojeni):
    #přidám úkol do databáze skrze funkci z hlavního skriptu
    pridat_ukol(pripojeni, "Test_nazev", "Test_popis")

    #vyhledám si ID přidaného úkolu v databázi
    kurzor = pripojeni.cursor()
    kurzor.execute("SELECT UkolID FROM ukoly WHERE Nazev_ukolu = %s AND Popis_ukolu = %s", ("Test_nazev", "Test_popis"))
    ukolID = kurzor.fetchone()[0]

    #odstraním úkol skrze funkci z hlavního skriptu
    odstranit_ukol(pripojeni, ukolID,)

    #vyhledám si záznam v databázi přidaného (a následně smazaného) úkolu, očekávám, že záznam neexistuje
    kurzor.execute("SELECT * FROM ukoly WHERE UkolId = %s", (ukolID,))
    vysledek = kurzor.fetchone()
    pripojeni.commit()
    kurzor.close()

    assert vysledek is None

def test_odstranit_ukol_negativni(pripojeni):
    #přidám úkol do databáze skrze funkci z hlavního skriptu
    pridat_ukol(pripojeni, "Test_nazev", "Test_popis")

    #očekávám, že funkce vyhodí chybu při zadání stringu místo čísla
    with pytest.raises((TypeError, ValueError)):
        odstranit_ukol(pripojeni, "abc")

    #Úklid
    kurzor = pripojeni.cursor()
    kurzor.execute("DELETE FROM ukoly WHERE Nazev_ukolu = 'Test_nazev'")
    pripojeni.commit()
    kurzor.close()