ukoly = []

def hlavni_menu():
    print("Správce úkolů - Hlavní menu\n"
        "1. Přidat nový úkol\n"
        "2. Zobrazit všechny úkoly\n"
        "3. Odstranit úkol\n"
        "4. Konec programu")

def pridat_ukol():
    while True:
        #Vytvoření dočasného listu pro uložení názvu i popisu úkolu jako jeden index v listu "ukoly".
        seznam = []
        nazev_ukolu = str(input("Zadejte název úkolu: "))
        popis_ukolu = str(input("Zadejte popis úkolu: "))

        #Kontrola platného vstupu
        if nazev_ukolu  == "": 
            print("Nezadali jste název úkolu, prosím zadejte vstup znovu.\n")
        elif popis_ukolu == "":
            print("Nezadali jste popis úkolu, prosím zadejte vstup znovu.\n")
        else:
            #Přidání názvu a popisu úkolu do listu "seznam" a následně přidání tohoto celku do listu "ukoly".
            seznam.append(nazev_ukolu)
            seznam.append(popis_ukolu)
            ukoly.append(seznam)
            print(f"\nÚkol '{nazev_ukolu}' byl přidán.\n")
            break

def zobrazit_ukoly():
    pocet = 1
    print("\nSeznam úkolů:")
    for poradi in range(0, len(ukoly)):
        print(f"{pocet}. {ukoly[poradi][0]} - {ukoly[poradi][1]}")
        pocet += 1
    print("")

def odstranit_ukol():
    while True:
        #Zobrazení seznamu úkolů
        zobrazit_ukoly()

        cislo_ukolu = int(input("\nZadejte číslo úkolu, který chcete odstranit: ")) -1

        #Kontrola platného vstupu
        if len(ukoly) == 1:
            if (cislo_ukolu + 1) == 1:
                nazev_smazaneho_ukolu = ukoly[cislo_ukolu][0]
                ukoly.pop(cislo_ukolu)
                print(f"Úkol {nazev_smazaneho_ukolu} byl odstraněn.\n")
                break
            else:
                print("Tento úkol není v seznamu.")
        elif (cislo_ukolu + 1) in range(0, (len(ukoly) + 1)):
            nazev_smazaneho_ukolu = ukoly[cislo_ukolu][0]
            ukoly.pop(cislo_ukolu)
            print(f"Úkol '{nazev_smazaneho_ukolu}' byl odstraněn.\n")
            break
        else:
            print("Tento úkol není v seznamu.")

while True:
    hlavni_menu()

    vyber = input("Vyberte možnost (1-4): ")

    if vyber == "1":
        pridat_ukol()
    elif vyber == "2":
        zobrazit_ukoly()
    elif vyber == "3":
        odstranit_ukol()
    elif vyber == "4":
        print("\nKonec programu.")
        break
    else:
        print("\nZadali jste neplatnou volbu.\n")
    
