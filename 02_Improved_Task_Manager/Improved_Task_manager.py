import mysql.connector
from mysql.connector import Error

def pripojeni_db():
    try:
        return mysql.connector.connect(
            host = "localhost", 
            user = "root", 
            password = "1111", 
            database = "taskmanager"
        )
    except Error as e:
        return None

def vytvoreni_tabulky(pripojeni):
    #Připojení databáze
    if pripojeni == None:
        print("Databáze není připojená.")
        exit()
    else:
        kurzor = pripojeni.cursor() 

        #Ověření existence tabulky
        nazev_tabulky = "ukoly"
        kurzor.execute("""
            SELECT COUNT(*) FROM information_schema.tables 
            WHERE table_schema = %s AND table_name = %s """, ("taskmanager", nazev_tabulky))

        exists = kurzor.fetchone()[0]

        if exists:
            print(f"Tabulka '{nazev_tabulky}' už existuje.")       
        else:
            #Vytvoření tabulky pokud ještě neexistuje
            kurzor.execute("""
            CREATE TABLE IF NOT EXISTS ukoly (
                UkolID INT PRIMARY KEY AUTO_INCREMENT,
                Nazev_ukolu VARCHAR(50) NOT NULL,
                Popis_ukolu VARCHAR(50) NOT NULL,
                Stav VARCHAR(10) DEFAULT "Nezahájeno",
                Datum_vytvoreni DATE
            )
            """)

            pripojeni.commit()
            kurzor.close()
            print("Tabulka vytvořena")

def pridat_ukol_vstupy(pripojeni):
    while True:
        Nazev_ukolu = input("Název úkolu: ").strip()
        Popis_ukolu = input("Popis úkolu: ").strip()
        #Ověření zadání obou vstupů
        if not Nazev_ukolu: 
            print("Nezadali jste název úkolu, prosím zadejte vstup znovu.\n")
        elif not Popis_ukolu:
            print("Nezadali jste popis úkolu, prosím zadejte vstup znovu.\n")
        else:
            pridat_ukol(pripojeni, Nazev_ukolu, Popis_ukolu)
            break

def pridat_ukol(pripojeni, Nazev_ukolu, Popis_ukolu):
    kurzor = pripojeni.cursor()
    kurzor.execute("INSERT INTO ukoly (Nazev_ukolu, Popis_ukolu, Datum_vytvoreni) Values (%s, %s, NOW())", (Nazev_ukolu, Popis_ukolu))
    pripojeni.commit()
    kurzor.close()
    print("Úkol přidán.\n")

def zobrazit_ukoly(pripojeni):
    kurzor = pripojeni.cursor()
    kurzor.execute("""
    SELECT UkolID, Nazev_ukolu, Popis_ukolu, Stav 
    FROM ukoly
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
    print("")
    kurzor.close()

def zobrazit_vsechny_ukoly(pripojeni): #pomocná funkce pro zobrazení všech úkolů ve funkcích aktualizovat_ukol() a odstranit_ukol()
    kurzor = pripojeni.cursor()
    kurzor.execute("""
    SELECT UkolID, Nazev_ukolu, Stav 
    FROM ukoly
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

def aktualizovat_ukol_vstupy(pripojeni):
    while True:
        if zobrazit_vsechny_ukoly(pripojeni) == "Seznam je prázdný": #Ošetření v případě prázdného seznamu
            print("Seznam je prázdný.\n")
            break
        else:
            try:
                ukolID = int(input("ID úkolu: ").strip())
                stav = input("Nový stav úkolu (Probíhá, Hotovo): ").strip()
                #SQL dotaz pro účely ověření zadání platného ID
                kurzor = pripojeni.cursor()
                kurzor.execute("SELECT * FROM ukoly WHERE UkolID = %s", (ukolID,))
                platneID = kurzor.fetchone()
                if platneID:
                    aktualizovat_ukol(pripojeni, ukolID, stav)
                    break
                else:
                    print("ID neexistuje, zadejte ho prosím znovu.\n")
            except ValueError as e:
                print("\nZadali jste neplatnou volbu.")

def aktualizovat_ukol(pripojeni, ukolID, stav):
    kurzor = pripojeni.cursor()
    kurzor.execute("SELECT * FROM ukoly WHERE UkolID = %s", (ukolID,))
    if not kurzor.fetchone():
        kurzor.close()
        raise ValueError("ID neexistuje.")
    
    kurzor.execute("UPDATE ukoly SET Stav = %s WHERE UkolID = %s", (stav, ukolID))
    pripojeni.commit()
    kurzor.close()
    print("Úkol aktualizován.\n")

def odstranit_ukol_vstupy(pripojeni):
    while True:
        if zobrazit_vsechny_ukoly(pripojeni) == "Seznam je prázdný": #Ošetření v případě prázdného seznamu
            print("Seznam je prázdný.\n")
            break
        else:
            try:
                ukolID = int(input("Zadej ID úkolu, který chcete smazat: ").strip())
                kurzor = pripojeni.cursor()
                kurzor.execute("SELECT * FROM ukoly WHERE UkolID = %s", (ukolID,))
                platneID = kurzor.fetchone()
                if platneID:
                    odstranit_ukol(pripojeni, ukolID)
                    break
                else:
                    print("ID neexistuje, zadejte ho prosím znovu.\n")
            except ValueError as e:
                print("\nZadali jste neplatnou volbu.")

def odstranit_ukol(pripojeni, ukolID):
    kurzor = pripojeni.cursor()
    kurzor.execute("SELECT * FROM ukoly WHERE UkolID = %s", (ukolID,))
    if not kurzor.fetchone():
        kurzor.close()
        raise ValueError("ID neexistuje.")
    
    kurzor.execute("DELETE FROM ukoly WHERE UkolID = %s", (ukolID,))
    pripojeni.commit()
    kurzor.close()
    print("Úkol odstraněn.\n")

def ukoncit_program(pripojeni):
    kurzor = pripojeni.cursor()
    kurzor.execute("DROP TABLE ukoly")
    pripojeni.commit()
    kurzor.close()
    pripojeni.close()
    print("\nProgram ukončen.")

def hlavni_menu(pripojeni):
    while True:
        print("Vylepšený správce úkolů - Hlavní menu\n"
        "1. Přidat úkol\n"
        "2. Zobrazit úkoly\n"
        "3. Aktualizovat úkol\n"
        "4. Odstranit úkol\n"
        "5. Ukončit program")

        try:
            vyber = int(input("Vyberte možnost (1-5): ").strip())

            if vyber == 1:
                pridat_ukol_vstupy(pripojeni)
            elif vyber == 2:
                zobrazit_ukoly(pripojeni)
            elif vyber == 3:
                aktualizovat_ukol_vstupy(pripojeni)
            elif vyber == 4:
                odstranit_ukol_vstupy(pripojeni)
            elif vyber == 5:
                ukoncit_program(pripojeni)
                break
            else:
                print("\nZadejte číslo 1-5.\n")
        except ValueError as e:
                print("\nZadali jste neplatnou volbu.\n")



if __name__ == "__main__":
    pripojeni = pripojeni_db()
    vytvoreni_tabulky(pripojeni)
    hlavni_menu(pripojeni)