import mysql.connector

def vytvoreni_test_tabulky():
    conn = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "1111",
        database = "taskmanager_test"
    )
    kurzor = conn.cursor()

    kurzor.execute("DROP TABLE IF EXISTS ukoly")

    kurzor.execute("""
            CREATE TABLE IF NOT EXISTS ukoly (
                UkolID INT PRIMARY KEY AUTO_INCREMENT,
                Nazev_ukolu VARCHAR(50) NOT NULL,
                Popis_ukolu VARCHAR(50) NOT NULL,
                Stav VARCHAR(10) DEFAULT "Nezahájeno",
                Datum_vytvoreni DATE
            )
            """)
    
    conn.commit()
    kurzor.close()
    conn.close()
    print("Testovací tabulky vytvořeny.")


if __name__ == "__main__":
    vytvoreni_test_tabulky()
