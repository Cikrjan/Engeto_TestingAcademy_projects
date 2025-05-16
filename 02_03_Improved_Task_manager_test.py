import pytest
import mysql.connector
from test_init import vytvoreni_test_tabulky

@pytest.fixture(scope="session", autouse=True)
def vytvoreni_test_db():
    vytvoreni_test_tabulky()

@pytest.fixture(scope="module")
def db_connection():
    conn = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "1111",
        database = "taskmanager_test"
    )
    yield conn
    conn.close()

def test_pridat_ukol_pozitivni(db_connection):
    kurzor = db_connection.cursor()
    kurzor.execute("INSERT INTO ukoly (Nazev_ukolu, Popis_ukolu, Datum_vytvoreni) VALUES ('Test_nazev', 'Test_popis', NOW())")
    db_connection.commit()
    kurzor.execute("SELECT * FROM ukoly WHERE Nazev_ukolu = 'Test_nazev'")
    vysledek = kurzor.fetchone()
    kurzor.execute("DELETE FROM ukoly WHERE Nazev_ukolu = 'Test_nazev'")
    db_connection.commit()
    kurzor.close()
    
    assert vysledek is not None

def test_pridat_ukol_negativni(db_connection):
    kurzor = db_connection.cursor()
    kurzor.execute("INSERT INTO ukoly (Nazev_ukolu, Popis_ukolu, Datum_vytvoreni) VALUES ('', 'Test_popis', NOW())")
    db_connection.commit()
    kurzor.execute("SELECT * FROM ukoly WHERE Nazev_ukolu = 'Test_nazev'")
    vysledek = kurzor.fetchone()
    kurzor.execute("DELETE FROM ukoly WHERE Nazev_ukolu = 'Test_nazev'")
    db_connection.commit()
    kurzor.close()
    
    assert vysledek is None

