import mysql.connector

def pripojeni_db():
    return mysql.connector.connect(
        host = "localhost", 
        user = "root", 
        password = "1111", 
        database = "TaskManager"
    )

def vytvoreni_tabulky():
    #Připojení databáze
    conn = pripojeni_db()
    kurzor = conn.cursor() 

    #Vytvoření tabulky pokud ještě neexistuje
    kurzor.execute("""
    CREATE TABLE IF NOT EXISTS Ukoly (
	    UkolID INT PRIMARY KEY AUTO_INCREMENT,
        Nazev_ukolu VARCHAR(50) NOT NULL,
        Popis_ukolu VARCHAR(50) NOT NULL,
        Stav VARCHAR(10) DEFAULT "Nezahájeno"
    )
    """)

    conn.commit()
    kurzor.close()
    conn.close()
    print("Tabulka vytvořena")

def pridat_ukol():
    Nazev_ukolu = input("Název úkolu: ")
    Popis_ukolu = input("Popis úkolu: ")
    conn = pripojeni_db()
    kurzor = conn.cursor()
    kurzor.execute("INSERT INTO Ukoly (Nazev_ukolu, Popis_ukolu) Values (%s, %s)", (Nazev_ukolu, Popis_ukolu))
    conn.commit()
    kurzor.close()
    conn.close()
    print("Úkol přidán")

def zobrazit_ukoly():
    conn = pripojeni_db()
    kurzor = conn.cursor()
    kurzor.execute("SELECT UkolID, Nazev_ukolu, Popis_ukolu, Stav " \
                    "FROM Ukoly" \
                    "WHERE Stav = 'Nezahájeno' OR 'Probíhá'")
    print("\n Seznam úkolů: ")
    for row in kurzor.fetchall():
        stav = "Nezahájeno" if row[3] else "Probíhá"
        print(f"{row[0]} : {row[1]} - {row[2]} ({stav})")
    kurzor.close()
    conn.close()

def aktualizovat_ukol():
    ukolID = int(input("ID úkolu: "))
    stav = input("Nový stav úkolu (Probíhá, Hotovo): ")
    conn = pripojeni_db()
    kurzor = conn.cursor()
    kurzor.execute("UPDATE Ukoly SET Stav = %s WHERE UkolID = %s", (stav, ukolID))
    kurzor.close()
    conn.close()


def hlavni_menu():
    while True:
        print("Vylepšený správce úkolů - Hlavní menu\n"
        "1. Přidat úkol\n"
        "2. Zobrazit úkoly\n"
        "3. Aktualizovat úkol\n"
        "4. Odstranit úkol\n"
        "5. Ukončit program")

        vyber = input("Vyberte možnost (1-5): ")

        if vyber == "1":
            pridat_ukol()
        elif vyber == "2":
            zobrazit_ukoly()
        elif vyber == "3":
            aktualizovat_ukol()
        elif vyber == "4":
            odstranit_ukol()
        elif vyber == "5":
            print("\nProgram ukončen.")
            break
        else:
            print("\nZadali jste neplatnou volbu.\n")



if __name__ == "__main__":
    vytvoreni_tabulky()
    hlavni_menu()