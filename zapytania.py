import sqlite3


def connect_to_database():
    """Nawiązanie połączenia z bazą danych"""
    conn = sqlite3.connect('samochody_osoby.db')
    cursor = conn.cursor()
    return conn, cursor


def ile_samochodow_maja_osoby(cursor):
    """Zapytanie: Ile samochodów mają poszczególne osoby"""
    print("=== ILE SAMOCHODÓW MAJĄ POSZCZEGÓLNE OSOBY ===")
    query = '''
        SELECT o.imie, o.nazwisko, COUNT(os.samochod_id) as liczba_samochodow
        FROM osoba o
        LEFT JOIN osoba_samochod os ON o.id = os.osoba_id
        GROUP BY o.id, o.imie, o.nazwisko
        ORDER BY liczba_samochodow DESC
    '''
    cursor.execute(query)
    results = cursor.fetchall()

    for imie, nazwisko, liczba in results:
        print(f"{imie} {nazwisko}: {liczba} samochód(ów)")
    print()


def wlasciciele_czerwonych_samochodow(cursor):
    """Zapytanie: Właściciele czerwonych samochodów"""
    print("=== WŁAŚCICIELE CZERWONYCH SAMOCHODÓW ===")
    query = '''
        SELECT DISTINCT o.imie, o.nazwisko, s.marka, s.model
        FROM osoba o
        JOIN osoba_samochod os ON o.id = os.osoba_id
        JOIN samochod s ON os.samochod_id = s.id
        WHERE s.kolor = 'czerwony'
        ORDER BY o.nazwisko, o.imie
    '''
    cursor.execute(query)
    results = cursor.fetchall()

    for imie, nazwisko, marka, model in results:
        print(f"{imie} {nazwisko} -> {marka} {model}")
    print()


def wlasciciele_ponizej_21_lat(cursor):
    """Zapytanie: Właściciele poniżej 21 lat i ich samochody"""
    print("=== WŁAŚCICIELE PONIŻEJ 21 LAT I ICH SAMOCHODY ===")
    query = '''
        SELECT o.imie, o.nazwisko, o.wiek, s.marka, s.model, s.kolor, s.rok_produkcji
        FROM osoba o
        JOIN osoba_samochod os ON o.id = os.osoba_id
        JOIN samochod s ON os.samochod_id = s.id
        WHERE o.wiek < 21
        ORDER BY o.wiek, o.nazwisko
    '''
    cursor.execute(query)
    results = cursor.fetchall()

    if results:
        for imie, nazwisko, wiek, marka, model, kolor, rok in results:
            print(
                f"{imie} {nazwisko} ({wiek} lat) -> {marka} {model} ({kolor}, {rok})")
    else:
        print("Brak właścicieli poniżej 21 lat")
    print()


def najdrozsze_samochody_i_wlasciciele(cursor):
    """Zapytanie: Najdroższe samochody i ich właściciele"""
    print("=== NAJDROŻSZE SAMOCHODY I ICH WŁAŚCICIELE ===")
    query = '''
        SELECT s.marka, s.model, s.cena, o.imie, o.nazwisko
        FROM samochod s
        JOIN osoba_samochod os ON s.id = os.samochod_id
        JOIN osoba o ON os.osoba_id = o.id
        ORDER BY s.cena DESC
        LIMIT 5
    '''
    cursor.execute(query)
    results = cursor.fetchall()

    for marka, model, cena, imie, nazwisko in results:
        print(f"{marka} {model} ({cena} zł) -> {imie} {nazwisko}")
    print()


def samochody_wedlug_koloru(cursor):
    """Zapytanie: Liczba samochodów według koloru"""
    print("=== LICZBA SAMOCHODÓW WEDŁUG KOLORU ===")
    query = '''
        SELECT s.kolor, COUNT(*) as liczba
        FROM samochod s
        GROUP BY s.kolor
        ORDER BY liczba DESC
    '''
    cursor.execute(query)
    results = cursor.fetchall()

    for kolor, liczba in results:
        print(f"{kolor.capitalize()}: {liczba} samochód(ów)")
    print()


def sredni_wiek_wlascicieli_wedlug_marki(cursor):
    """Zapytanie: Średni wiek właścicieli według marki samochodu"""
    print("=== ŚREDNI WIEK WŁAŚCICIELI WEDŁUG MARKI SAMOCHODU ===")
    query = '''
        SELECT s.marka, ROUND(AVG(o.wiek), 1) as sredni_wiek, COUNT(*) as liczba_wlascicieli
        FROM samochod s
        JOIN osoba_samochod os ON s.id = os.samochod_id
        JOIN osoba o ON os.osoba_id = o.id
        GROUP BY s.marka
        ORDER BY sredni_wiek DESC
    '''
    cursor.execute(query)
    results = cursor.fetchall()

    for marka, sredni_wiek, liczba in results:
        print(f"{marka}: średni wiek {sredni_wiek} lat ({liczba} właściciel(i))")
    print()


def osoby_bez_samochodu(cursor):
    """Zapytanie: Osoby bez samochodu"""
    print("=== OSOBY BEZ SAMOCHODU ===")
    query = '''
        SELECT o.imie, o.nazwisko, o.wiek
        FROM osoba o
        LEFT JOIN osoba_samochod os ON o.id = os.osoba_id
        WHERE os.osoba_id IS NULL
        ORDER BY o.nazwisko
    '''
    cursor.execute(query)
    results = cursor.fetchall()

    if results:
        for imie, nazwisko, wiek in results:
            print(f"{imie} {nazwisko} ({wiek} lat)")
    else:
        print("Wszyscy mają samochody")
    print()


def dostepne_kolory_samochodow(cursor):
    """Zapytanie: Dostępne kolory samochodów"""
    print("=== DOSTĘPNE KOLORY SAMOCHODÓW ===")
    cursor.execute("SELECT DISTINCT kolor FROM samochod ORDER BY kolor")
    kolory = cursor.fetchall()
    for kolor, in kolory:
        print(f"- {kolor}")
    print()


def wszystkie_samochody_z_wlascicielami(cursor):
    """Zapytanie: Wszystkie samochody z właścicielami"""
    print("=== WSZYSTKIE SAMOCHODY Z WŁAŚCICIELAMI ===")
    query = '''
        SELECT s.marka, s.model, s.kolor, s.rok_produkcji, s.cena, 
               o.imie, o.nazwisko, os.data_zakupu
        FROM samochod s
        JOIN osoba_samochod os ON s.id = os.samochod_id
        JOIN osoba o ON os.osoba_id = o.id
        ORDER BY s.marka, s.model
    '''
    cursor.execute(query)
    results = cursor.fetchall()

    for marka, model, kolor, rok, cena, imie, nazwisko, data_zakupu in results:
        print(
            f"{marka} {model} ({kolor}, {rok}, {cena} zł) -> {imie} {nazwisko} (zakup: {data_zakupu})")
    print()


def samochody_wyzsze_od_sredniej_ceny(cursor):
    """Zapytanie: Samochody droższe od średniej ceny"""
    print("=== SAMOCHODY DROŻSZE OD ŚREDNIEJ CENY ===")
    query = '''
        SELECT s.marka, s.model, s.cena, o.imie, o.nazwisko
        FROM samochod s
        JOIN osoba_samochod os ON s.id = os.samochod_id
        JOIN osoba o ON os.osoba_id = o.id
        WHERE s.cena > (SELECT AVG(cena) FROM samochod)
        ORDER BY s.cena DESC
    '''
    cursor.execute(query)
    results = cursor.fetchall()

    # Dodatkowo pokaż średnią cenę
    cursor.execute("SELECT ROUND(AVG(cena), 2) FROM samochod")
    srednia_cena = cursor.fetchone()[0]
    print(f"Średnia cena samochodów: {srednia_cena} zł")
    print()

    for marka, model, cena, imie, nazwisko in results:
        print(f"{marka} {model} ({cena} zł) -> {imie} {nazwisko}")
    print()


def statystyki_cenowe(cursor):
    """Zapytanie: Statystyki cenowe - MIN, MAX, AVG, SUM"""
    print("=== STATYSTYKI CENOWE SAMOCHODÓW ===")
    query = '''
        SELECT 
            MIN(cena) as najnizsza_cena,
            MAX(cena) as najwyzsza_cena,
            ROUND(AVG(cena), 2) as srednia_cena,
            SUM(cena) as suma_wszystkich_cen,
            COUNT(*) as liczba_samochodow,
            ROUND(AVG(rok_produkcji), 0) as sredni_rok_produkcji
        FROM samochod
    '''
    cursor.execute(query)
    result = cursor.fetchone()
    
    if result:
        min_cena, max_cena, avg_cena, suma_cen, liczba, avg_rok = result
        print(f"Najniższa cena: {min_cena} zł")
        print(f"Najwyższa cena: {max_cena} zł")
        print(f"Średnia cena: {avg_cena} zł")
        print(f"Suma wszystkich cen: {suma_cen} zł")
        print(f"Liczba samochodów: {liczba}")
        print(f"Średni rok produkcji: {int(avg_rok)}")
    print()


def statystyki_wiekowe_osob(cursor):
    """Zapytanie: Statystyki wiekowe osób"""
    print("=== STATYSTYKI WIEKOWE OSÓB ===")
    query = '''
        SELECT 
            MIN(wiek) as najmlodszy,
            MAX(wiek) as najstarszy,
            ROUND(AVG(wiek), 1) as sredni_wiek,
            COUNT(*) as liczba_osob,
            COUNT(CASE WHEN wiek < 25 THEN 1 END) as osob_ponizej_25,
            COUNT(CASE WHEN wiek >= 25 AND wiek < 35 THEN 1 END) as osob_25_35,
            COUNT(CASE WHEN wiek >= 35 THEN 1 END) as osob_powyzej_35
        FROM osoba
    '''
    cursor.execute(query)
    result = cursor.fetchone()
    
    if result:
        min_wiek, max_wiek, avg_wiek, liczba, do_25, od_25_35, powyzej_35 = result
        print(f"Najmłodszy właściciel: {min_wiek} lat")
        print(f"Najstarszy właściciel: {max_wiek} lat")
        print(f"Średni wiek: {avg_wiek} lat")
        print(f"Liczba osób: {liczba}")
        print(f"Poniżej 25 lat: {do_25} osób")
        print(f"25-35 lat: {od_25_35} osób")
        print(f"Powyżej 35 lat: {powyzej_35} osób")
    print()


def ranking_najdrozszych_marek(cursor):
    """Zapytanie: Ranking najdroższych marek (średnia cena)"""
    print("=== RANKING NAJDROŻSZYCH MAREK (ŚREDNIA CENA) ===")
    query = '''
        SELECT 
            marka,
            COUNT(*) as liczba_samochodow,
            ROUND(MIN(cena), 0) as najtansza,
            ROUND(MAX(cena), 0) as najdrozsza,
            ROUND(AVG(cena), 0) as srednia_cena,
            SUM(cena) as suma_wartosci
        FROM samochod
        GROUP BY marka
        ORDER BY srednia_cena DESC
    '''
    cursor.execute(query)
    results = cursor.fetchall()
    
    for marka, liczba, min_cena, max_cena, avg_cena, suma in results:
        print(f"{marka}: {int(avg_cena)} zł śred. ({liczba} aut, {int(min_cena)}-{int(max_cena)} zł, suma: {int(suma)} zł)")
    print()


def analiza_kolorow_z_cena(cursor):
    """Zapytanie: Analiza kolorów z cenami"""
    print("=== ANALIZA KOLORÓW Z CENAMI ===")
    query = '''
        SELECT 
            kolor,
            COUNT(*) as liczba_aut,
            ROUND(MIN(cena), 0) as najtansza,
            ROUND(MAX(cena), 0) as najdrozsza,
            ROUND(AVG(cena), 0) as srednia_cena,
            ROUND(AVG(rok_produkcji), 0) as sredni_rok
        FROM samochod
        GROUP BY kolor
        HAVING COUNT(*) >= 1
        ORDER BY srednia_cena DESC
    '''
    cursor.execute(query)
    results = cursor.fetchall()
    
    for kolor, liczba, min_cena, max_cena, avg_cena, avg_rok in results:
        print(f"{kolor.capitalize()}: {liczba} aut, śred. {int(avg_cena)} zł ({int(min_cena)}-{int(max_cena)} zł), śred. rok {int(avg_rok)}")
    print()


def najbogatsi_wlasciciele(cursor):
    """Zapytanie: Najbogatsi właściciele (według wartości posiadanych aut)"""
    print("=== NAJBOGATSI WŁAŚCICIELE (WEDŁUG WARTOŚCI AUT) ===")
    query = '''
        SELECT 
            o.imie,
            o.nazwisko,
            o.wiek,
            COUNT(s.id) as liczba_aut,
            SUM(s.cena) as calkowita_wartosc,
            ROUND(AVG(s.cena), 0) as srednia_wartosc_auta,
            MIN(s.cena) as najtansze_auto,
            MAX(s.cena) as najdrozsze_auto
        FROM osoba o
        JOIN osoba_samochod os ON o.id = os.osoba_id
        JOIN samochod s ON os.samochod_id = s.id
        GROUP BY o.id, o.imie, o.nazwisko, o.wiek
        ORDER BY calkowita_wartosc DESC
    '''
    cursor.execute(query)
    results = cursor.fetchall()
    
    for imie, nazwisko, wiek, liczba, wartosc, avg_wartosc, min_cena, max_cena in results:
        print(f"{imie} {nazwisko} ({wiek} lat): {int(wartosc)} zł ({liczba} aut, śred. {int(avg_wartosc)} zł)")
        if liczba > 1:
            print(f"   └─ Najdroższe: {int(max_cena)} zł, najtańsze: {int(min_cena)} zł")
    print()


def analiza_rocznikowa(cursor):
    """Zapytanie: Analiza według roku produkcji"""
    print("=== ANALIZA WEDŁUG ROKU PRODUKCJI ===")
    query = '''
        SELECT 
            rok_produkcji,
            COUNT(*) as liczba_aut,
            GROUP_CONCAT(marka || ' ' || model, ', ') as modele,
            ROUND(AVG(cena), 0) as srednia_cena,
            MIN(cena) as min_cena,
            MAX(cena) as max_cena
        FROM samochod
        GROUP BY rok_produkcji
        ORDER BY rok_produkcji DESC
    '''
    cursor.execute(query)
    results = cursor.fetchall()
    
    for rok, liczba, modele, avg_cena, min_cena, max_cena in results:
        print(f"Rok {rok}: {liczba} aut, śred. {int(avg_cena)} zł ({int(min_cena)}-{int(max_cena)} zł)")
        print(f"   └─ {modele}")
    print()


def porownanie_wiek_wartosc_aut(cursor):
    """Zapytanie: Porównanie wieku właścicieli z wartością ich aut"""
    print("=== PORÓWNANIE WIEKU WŁAŚCICIELI Z WARTOŚCIĄ AUT ===")
    query = '''
        SELECT 
            CASE 
                WHEN o.wiek < 25 THEN 'Poniżej 25 lat'
                WHEN o.wiek >= 25 AND o.wiek < 35 THEN '25-35 lat'
                WHEN o.wiek >= 35 AND o.wiek < 45 THEN '35-45 lat'
                ELSE 'Powyżej 45 lat'
            END as grupa_wiekowa,
            COUNT(DISTINCT o.id) as liczba_osob,
            COUNT(s.id) as liczba_aut,
            ROUND(AVG(s.cena), 0) as srednia_wartosc_auta,
            SUM(s.cena) as suma_wartosci,
            ROUND(AVG(s.rok_produkcji), 0) as sredni_rok_aut
        FROM osoba o
        JOIN osoba_samochod os ON o.id = os.osoba_id
        JOIN samochod s ON os.samochod_id = s.id
        GROUP BY 
            CASE 
                WHEN o.wiek < 25 THEN 'Poniżej 25 lat'
                WHEN o.wiek >= 25 AND o.wiek < 35 THEN '25-35 lat'
                WHEN o.wiek >= 35 AND o.wiek < 45 THEN '35-45 lat'
                ELSE 'Powyżej 45 lat'
            END
        ORDER BY srednia_wartosc_auta DESC
    '''
    cursor.execute(query)
    results = cursor.fetchall()
    
    for grupa, osob, aut, avg_wartosc, suma, avg_rok in results:
        print(f"{grupa}: {osob} osób, {aut} aut")
        print(f"   └─ Śred. wartość auta: {int(avg_wartosc)} zł, suma: {int(suma)} zł, śred. rok: {int(avg_rok)}")
    print()


def top_kombinacje_marka_kolor(cursor):
    """Zapytanie: TOP kombinacje marka-kolor"""
    print("=== TOP KOMBINACJE MARKA-KOLOR ===")
    query = '''
        SELECT 
            marka || ' ' || kolor as kombinacja,
            COUNT(*) as liczba,
            ROUND(AVG(cena), 0) as srednia_cena,
            GROUP_CONCAT(DISTINCT model) as modele
        FROM samochod
        GROUP BY marka, kolor
        HAVING COUNT(*) >= 1
        ORDER BY liczba DESC, srednia_cena DESC
    '''
    cursor.execute(query)
    results = cursor.fetchall()
    
    for kombinacja, liczba, avg_cena, modele in results:
        print(f"{kombinacja}: {liczba} aut, śred. {int(avg_cena)} zł ({modele})")
    print()


def analiza_dat_zakupu(cursor):
    """Zapytanie: Analiza dat zakupu samochodów"""
    print("=== ANALIZA DAT ZAKUPU SAMOCHODÓW ===")
    query = '''
        SELECT 
            strftime('%Y', data_zakupu) as rok_zakupu,
            COUNT(*) as liczba_zakupow,
            ROUND(AVG(s.cena), 0) as srednia_cena_zakupow,
            MIN(data_zakupu) as pierwszy_zakup,
            MAX(data_zakupu) as ostatni_zakup
        FROM osoba_samochod os
        JOIN samochod s ON os.samochod_id = s.id
        WHERE data_zakupu IS NOT NULL
        GROUP BY strftime('%Y', data_zakupu)
        ORDER BY rok_zakupu DESC
    '''
    cursor.execute(query)
    results = cursor.fetchall()
    
    for rok, liczba, avg_cena, pierwszy, ostatni in results:
        print(f"Rok {rok}: {liczba} zakupów, śred. cena {int(avg_cena)} zł (od {pierwszy} do {ostatni})")
    print()


def main():
    """Główna funkcja wykonująca wszystkie zapytania"""
    conn, cursor = connect_to_database()

    try:
        # Wykonywanie wszystkich zapytań SELECT
        ile_samochodow_maja_osoby(cursor)
        wlasciciele_czerwonych_samochodow(cursor)
        wlasciciele_ponizej_21_lat(cursor)
        najdrozsze_samochody_i_wlasciciele(cursor)
        samochody_wedlug_koloru(cursor)
        sredni_wiek_wlascicieli_wedlug_marki(cursor)
        osoby_bez_samochodu(cursor)
        dostepne_kolory_samochodow(cursor)
        wszystkie_samochody_z_wlascicielami(cursor)
        samochody_wyzsze_od_sredniej_ceny(cursor)
        
        # Nowe zapytania z agregatami
        print("\n" + "="*60)
        print("ZAAWANSOWANE ZAPYTANIA Z AGREGATAMI")
        print("="*60 + "\n")
        
        statystyki_cenowe(cursor)
        statystyki_wiekowe_osob(cursor)
        ranking_najdrozszych_marek(cursor)
        analiza_kolorow_z_cena(cursor)
        najbogatsi_wlasciciele(cursor)
        analiza_rocznikowa(cursor)
        porownanie_wiek_wartosc_aut(cursor)
        top_kombinacje_marka_kolor(cursor)
        analiza_dat_zakupu(cursor)

    finally:
        conn.close()
        print("Połączenie z bazą danych zamknięte.")


if __name__ == "__main__":
    main()
