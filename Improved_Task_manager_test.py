import pytest
import mysql.connector
from test_init import vytvoreni_test_tabulky
from Improved_Task_manager import pridat_ukol, aktualizovat_ukol, odstranit_ukol

@pytest.fixture(scope="session", autouse=True)
def vytvoreni_test_db():
    vytvoreni_test_tabulky()

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
    pridat_ukol(pripojeni, "Test_nazev", "Test_popis")

    kurzor = pripojeni.cursor()
    kurzor.execute("SELECT * FROM ukoly WHERE Nazev_ukolu = %s", ("Test_nazev",))
    vysledek = kurzor.fetchone()

    kurzor.execute("DELETE FROM ukoly WHERE Nazev_ukolu = %s", ("Test_nazev",))
    pripojeni.commit()
    kurzor.close()
    
    assert vysledek is not None

def test_pridat_ukol_negativni(pripojeni):
    pridat_ukol(pripojeni, "", "Test_popis")

    kurzor = pripojeni.cursor()
    kurzor.execute("SELECT * FROM ukoly WHERE Nazev_ukolu = %s", ("Test_nazev",))
    vysledek = kurzor.fetchone()

    kurzor.execute("DELETE FROM ukoly WHERE Nazev_ukolu = %s", ("Test_nazev",))
    pripojeni.commit()
    kurzor.close()
    
    assert vysledek is None

def test_aktualizovat_ukol_pozitivni(pripojeni):
    pridat_ukol(pripojeni, "Test_nazev", "Test_popis")
    aktualizovat_ukol(pripojeni, 1, "Probíhá")

    kurzor = pripojeni.cursor()
    kurzor.execute("SELECT * FROM ukoly WHERE UkolID = %s", ("1",))
    vysledek = kurzor.fetchone()
    kurzor.execute("DELETE FROM ukoly WHERE Nazev_ukolu = 'Test_nazev'")
    pripojeni.commit()
    kurzor.close()

    assert vysledek[3] == "Probíhá"

def test_aktualizovat_ukol_negativni(pripojeni):
    pridat_ukol(pripojeni, "Test_nazev", "Test_popis")
    with pytest.raises(ValueError):
        aktualizovat_ukol(pripojeni, 5, "Probíhá") #Zadání neexistujícího ID

    kurzor = pripojeni.cursor()
    # kurzor.execute("SELECT * FROM ukoly WHERE UkolID = %s", ("5",))
    # vysledek = kurzor.fetchone()
    kurzor.execute("DELETE FROM ukoly WHERE Nazev_ukolu = 'Test_nazev'")
    pripojeni.commit()
    kurzor.close()

