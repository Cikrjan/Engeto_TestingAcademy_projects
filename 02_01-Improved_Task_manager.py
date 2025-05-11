import mysql.connector

def pripojeni_db():
    return mysql.connector.connect(
        host = "localhost", 
        user = "root", 
        password = "1111", 
        database = "taskmanager"
    )

def vytvoreni_tabulky():
    #Připojení databáze
    conn = pripojeni_db()
    kurzor = conn.cursor() 

    #Ověření existence tabulky
    nazev_tabulky = "ukoly"
    kurzor.execute("""
        SELECT COUNT(*) FROM information_schema.tables 
        WHERE table_schema = %s AND table_name = %s """, ("taskmanager", nazev_tabulky))

    exists = kurzor.fetchone()[0]

    if exists:
        print(f"Tabulka '{nazev_tabulky}' už existuje.")       
    else:
        print(exists)
        #Vytvoření tabulky pokud ještě neexistuje
        kurzor.execute("""
        CREATE TABLE IF NOT EXISTS Ukoly (
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
        print("Tabulka vytvořena")

def pridat_ukol():
    while True:
        Nazev_ukolu = input("Název úkolu: ")
        Popis_ukolu = input("Popis úkolu: ")
        #Ověření zadání obou vstupů
        if Nazev_ukolu  == "": 
                print("Nezadali jste název úkolu, prosím zadejte vstup znovu.\n")
        elif Popis_ukolu == "":
            print("Nezadali jste popis úkolu, prosím zadejte vstup znovu.\n")
        else:
            conn = pripojeni_db()
            kurzor = conn.cursor()
            kurzor.execute("INSERT INTO Ukoly (Nazev_ukolu, Popis_ukolu, Datum_vytvoreni) Values (%s, %s, NOW())", (Nazev_ukolu, Popis_ukolu))
            conn.commit()
            kurzor.close()
            conn.close()
            print("Úkol přidán")
            break

def zobrazit_ukoly():
    conn = pripojeni_db()
    kurzor = conn.cursor()
    kurzor.execute("""
    SELECT UkolID, Nazev_ukolu, Popis_ukolu, Stav 
    FROM Ukoly
    WHERE Stav IN ('Nezahájeno', 'Probíhá')
    """)
    #Ověření, že seznam není prázdný
    seznam = kurzor.fetchall()
    if not seznam:
        print("Seznam je prázdný")
    else:
        print("\nSeznam úkolů: ")    
        for row in seznam:   
            if row[3] == "Hotovo":
                pass
            else:
                print(f"{row[0]} : {row[1]} - {row[2]} ({row[3]})")
    kurzor.close()
    conn.close()

def zobrazit_vsechny_ukoly(): #pomocná funkce pro zobrazení všech úkolů ve funkcích aktualizovat_ukol() a odstranit_ukol()
    conn = pripojeni_db()
    kurzor = conn.cursor()
    kurzor.execute("""
    SELECT UkolID, Nazev_ukolu, Stav 
    FROM Ukoly
    """)
    #Ověření, že seznam není prázdný
    seznam = kurzor.fetchall()
    if not seznam:
        return "Seznam je prázdný"
    else:
        print("\nSeznam úkolů: ")    
        for row in seznam:   
            print(f"{row[0]} : {row[1]} ({row[2]})")
    kurzor.close()
    conn.close()

def aktualizovat_ukol():
    while True:
        conn = pripojeni_db()
        kurzor = conn.cursor()
        if zobrazit_vsechny_ukoly() == "Seznam je prázdný":
            print("Seznam je prázdný.")
            break
        else:
            zobrazit_vsechny_ukoly()
            ukolID = int(input("ID úkolu: "))
            stav = input("Nový stav úkolu (Probíhá, Hotovo): ")
            #SQL dotaz pro účely ověření zadání platného ID
            kurzor.execute("SELECT * FROM ukoly WHERE UkolID = %s", (ukolID,))
            platneID = kurzor.fetchone()
            if platneID:
                    kurzor.execute("UPDATE Ukoly SET Stav = %s WHERE UkolID = %s", (stav, ukolID))
                    conn.commit()
                    kurzor.close()
                    conn.close()
                    break
            else:
                print("ID neexistuje, zadejte ho prosím znovu.")


def odstranit_ukol():
    while True:
        conn = pripojeni_db()
        kurzor = conn.cursor()
        if zobrazit_vsechny_ukoly() == "Seznam je prázdný":
            print("Seznam je prázdný.")
            break
        else:
            zobrazit_vsechny_ukoly()
            ukolID = int(input("Zadej ID úkolu, který chcete smazat: "))
            #SQL dotaz pro účely ověření zadání platného ID
            kurzor.execute("SELECT * FROM ukoly WHERE UkolID = %s", (ukolID,))
            platneID = kurzor.fetchone()
            if platneID:
                    kurzor.execute("DELETE FROM Ukoly WHERE UkolID = %s", (ukolID,))
                    conn.commit()
                    kurzor.close()
                    conn.close()
                    break
            else:
                print("ID neexistuje, zadejte ho prosím znovu.")

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