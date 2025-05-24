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
    kurzor = pripojeni.cursor()
    pridat_ukol(pripojeni, "Test_nazev", "Test_popis")
    kurzor.execute("SELECT * FROM ukoly WHERE Nazev_ukolu = 'Test_nazev'")
    vysledek = kurzor.fetchone()
    kurzor.execute("DELETE FROM ukoly WHERE Nazev_ukolu = 'Test_nazev'")
    pripojeni.commit()
    kurzor.close()
    
    assert vysledek is not None

def test_pridat_ukol_negativni(pripojeni):
    kurzor = pripojeni.cursor()
    kurzor.execute("INSERT INTO ukoly (Nazev_ukolu, Popis_ukolu, Datum_vytvoreni) VALUES ('', 'Test_popis', NOW())")
    pripojeni.commit()
    kurzor.execute("SELECT * FROM ukoly WHERE Nazev_ukolu = 'Test_nazev'")
    vysledek = kurzor.fetchone()
    kurzor.execute("DELETE FROM ukoly WHERE Nazev_ukolu = 'Test_nazev'")
    pripojeni.commit()
    kurzor.close()
    
    assert vysledek is None

def test_aktualizace_ukolu_pozitivni(pripojeni):
    kurzor = pripojeni.cursor()
    #Přidání testovacího úkolu
    kurzor.execute("INSERT INTO ukoly (Nazev_ukolu, Popis_ukolu, Datum_vytvoreni) VALUES ('Test_nazev', 'Test_popis', NOW())")
    pripojeni.commit()
    #změna stavu úkolu
    kurzor.execute("UPDATE ukoly SET Stav = 'Probíhá' WHERE UkolID = 1")
    pripojeni.commit()
    #výběr testovacího úkolu
    kurzor.execute("SELECT Stav FROM ukoly WHERE UkolID = 1")
    vysledek = kurzor.fetchone()[0]
    kurzor.execute("DELETE FROM ukoly WHERE Nazev_ukolu = 'Test_nazev'")
    pripojeni.commit()
    kurzor.close()

    assert vysledek == "Probíhá"

