import sqlite3


def connect_to_database():
    """Nawiązanie połączenia z bazą danych"""
    try:
        conn = sqlite3.connect('samochody_osoby.db')
        cursor = conn.cursor()
        return conn, cursor
    except sqlite3.Error as e:
        print(f"Błąd połączenia z bazą danych: {e}")
        return None, None


def zapytanie_o_kolor():
    """Interaktywne zapytanie o samochody określonego koloru"""
    conn, cursor = connect_to_database()
    if not conn:
        return
    
    # Pobierz dostępne kolory
    cursor.execute("SELECT DISTINCT kolor FROM samochod ORDER BY kolor")
    kolory = [row[0] for row in cursor.fetchall()]
    
    print("Dostępne kolory:")
    for i, kolor in enumerate(kolory, 1):
        print(f"{i}. {kolor}")
    
    try:
        wybor = int(input("\nWybierz numer koloru: ")) - 1
        if 0 <= wybor < len(kolory):
            wybrany_kolor = kolory[wybor]
            
            query = '''
                SELECT s.marka, s.model, s.rok_produkcji, s.cena, 
                       o.imie, o.nazwisko, os.data_zakupu
                FROM samochod s
                JOIN osoba_samochod os ON s.id = os.samochod_id
                JOIN osoba o ON os.osoba_id = o.id
                WHERE s.kolor = ?
                ORDER BY s.cena DESC
            '''
            cursor.execute(query, (wybrany_kolor,))
            results = cursor.fetchall()
            
            print(f"\n=== SAMOCHODY W KOLORZE {wybrany_kolor.upper()} ===")
            if results:
                for marka, model, rok, cena, imie, nazwisko, data in results:
                    print(f"{marka} {model} ({rok}) - {int(cena)} zł")
                    print(f"   └─ Właściciel: {imie} {nazwisko} (zakup: {data})")
            else:
                print("Brak samochodów w tym kolorze")
        else:
            print("Nieprawidłowy wybór")
    except ValueError:
        print("Proszę wprowadzić liczbę")
    finally:
        conn.close()


def zapytanie_o_przedzial_cenowy():
    """Interaktywne zapytanie o samochody w przedziale cenowym"""
    conn, cursor = connect_to_database()
    if not conn:
        return
    
    # Pokaż zakres cen
    cursor.execute("SELECT MIN(cena), MAX(cena) FROM samochod")
    min_cena, max_cena = cursor.fetchone()
    print(f"Dostępny zakres cen: {int(min_cena)} - {int(max_cena)} zł")
    
    try:
        cena_min = float(input("Podaj minimalną cenę: "))
        cena_max = float(input("Podaj maksymalną cenę: "))
        
        query = '''
            SELECT s.marka, s.model, s.kolor, s.rok_produkcji, s.cena,
                   COUNT(os.osoba_id) as liczba_wlascicieli,
                   GROUP_CONCAT(o.imie || ' ' || o.nazwisko, ', ') as wlasciciele
            FROM samochod s
            LEFT JOIN osoba_samochod os ON s.id = os.samochod_id
            LEFT JOIN osoba o ON os.osoba_id = o.id
            WHERE s.cena BETWEEN ? AND ?
            GROUP BY s.id, s.marka, s.model, s.kolor, s.rok_produkcji, s.cena
            ORDER BY s.cena DESC
        '''
        cursor.execute(query, (cena_min, cena_max))
        results = cursor.fetchall()
        
        print(f"\n=== SAMOCHODY W PRZEDZIALE {int(cena_min)} - {int(cena_max)} ZŁ ===")
        if results:
            for marka, model, kolor, rok, cena, liczba_wl, wlasciciele in results:
                print(f"{marka} {model} ({kolor}, {rok}) - {int(cena)} zł")
                if wlasciciele:
                    print(f"   └─ Właściciele ({liczba_wl}): {wlasciciele}")
                else:
                    print("   └─ Brak właścicieli")
        else:
            print("Brak samochodów w tym przedziale cenowym")
            
    except ValueError:
        print("Proszę wprowadzić prawidłowe liczby")
    finally:
        conn.close()


def zapytanie_o_wiek_wlasciciela():
    """Interaktywne zapytanie o właścicieli w określonym wieku"""
    conn, cursor = connect_to_database()
    if not conn:
        return
    
    cursor.execute("SELECT MIN(wiek), MAX(wiek) FROM osoba")
    min_wiek, max_wiek = cursor.fetchone()
    print(f"Dostępny zakres wieku: {min_wiek} - {max_wiek} lat")
    
    try:
        wiek_min = int(input("Podaj minimalny wiek: "))
        wiek_max = int(input("Podaj maksymalny wiek: "))
        
        query = '''
            SELECT o.imie, o.nazwisko, o.wiek,
                   COUNT(s.id) as liczba_aut,
                   ROUND(AVG(s.cena), 0) as srednia_wartosc,
                   SUM(s.cena) as suma_wartosci,
                   GROUP_CONCAT(s.marka || ' ' || s.model, ', ') as auta
            FROM osoba o
            LEFT JOIN osoba_samochod os ON o.id = os.osoba_id
            LEFT JOIN samochod s ON os.samochod_id = s.id
            WHERE o.wiek BETWEEN ? AND ?
            GROUP BY o.id, o.imie, o.nazwisko, o.wiek
            ORDER BY suma_wartosci DESC NULLS LAST
        '''
        cursor.execute(query, (wiek_min, wiek_max))
        results = cursor.fetchall()
        
        print(f"\n=== WŁAŚCICIELE W WIEKU {wiek_min} - {wiek_max} LAT ===")
        if results:
            for imie, nazwisko, wiek, liczba, srednia, suma, auta in results:
                print(f"{imie} {nazwisko} ({wiek} lat)")
                if suma:
                    print(f"   └─ {liczba} aut, wartość: {int(suma)} zł (śred. {int(srednia)} zł)")
                    print(f"   └─ Auta: {auta}")
                else:
                    print("   └─ Brak samochodów")
        else:
            print("Brak osób w tym przedziale wiekowym")
            
    except ValueError:
        print("Proszę wprowadzić prawidłowe liczby")
    finally:
        conn.close()


def top_n_zapytania():
    """Zapytania TOP N"""
    conn, cursor = connect_to_database()
    if not conn:
        return
    
    print("Dostępne opcje TOP N:")
    print("1. TOP najdroższych samochodów")
    print("2. TOP najbogatszych właścicieli")
    print("3. TOP najstarszych samochodów")
    print("4. TOP najnowszych samochodów")
    
    try:
        opcja = int(input("Wybierz opcję (1-4): "))
        n = int(input("Ile rekordów wyświetlić? "))
        
        if opcja == 1:
            query = '''
                SELECT s.marka, s.model, s.kolor, s.rok_produkcji, s.cena,
                       o.imie, o.nazwisko
                FROM samochod s
                LEFT JOIN osoba_samochod os ON s.id = os.samochod_id
                LEFT JOIN osoba o ON os.osoba_id = o.id
                ORDER BY s.cena DESC
                LIMIT ?
            '''
            cursor.execute(query, (n,))
            results = cursor.fetchall()
            print(f"\n=== TOP {n} NAJDROŻSZYCH SAMOCHODÓW ===")
            for i, (marka, model, kolor, rok, cena, imie, nazwisko) in enumerate(results, 1):
                print(f"{i}. {marka} {model} ({kolor}, {rok}) - {int(cena)} zł")
                if imie:
                    print(f"    └─ Właściciel: {imie} {nazwisko}")
                    
        elif opcja == 2:
            query = '''
                SELECT o.imie, o.nazwisko, o.wiek,
                       COUNT(s.id) as liczba_aut,
                       SUM(s.cena) as suma_wartosci
                FROM osoba o
                JOIN osoba_samochod os ON o.id = os.osoba_id
                JOIN samochod s ON os.samochod_id = s.id
                GROUP BY o.id, o.imie, o.nazwisko, o.wiek
                ORDER BY suma_wartosci DESC
                LIMIT ?
            '''
            cursor.execute(query, (n,))
            results = cursor.fetchall()
            print(f"\n=== TOP {n} NAJBOGATSZYCH WŁAŚCICIELI ===")
            for i, (imie, nazwisko, wiek, liczba, suma) in enumerate(results, 1):
                print(f"{i}. {imie} {nazwisko} ({wiek} lat) - {int(suma)} zł ({liczba} aut)")
                
        elif opcja == 3:
            query = '''
                SELECT s.marka, s.model, s.kolor, s.rok_produkcji, s.cena,
                       o.imie, o.nazwisko
                FROM samochod s
                LEFT JOIN osoba_samochod os ON s.id = os.samochod_id
                LEFT JOIN osoba o ON os.osoba_id = o.id
                ORDER BY s.rok_produkcji ASC
                LIMIT ?
            '''
            cursor.execute(query, (n,))
            results = cursor.fetchall()
            print(f"\n=== TOP {n} NAJSTARSZYCH SAMOCHODÓW ===")
            for i, (marka, model, kolor, rok, cena, imie, nazwisko) in enumerate(results, 1):
                print(f"{i}. {marka} {model} ({rok}, {kolor}) - {int(cena)} zł")
                if imie:
                    print(f"    └─ Właściciel: {imie} {nazwisko}")
                    
        elif opcja == 4:
            query = '''
                SELECT s.marka, s.model, s.kolor, s.rok_produkcji, s.cena,
                       o.imie, o.nazwisko
                FROM samochod s
                LEFT JOIN osoba_samochod os ON s.id = os.samochod_id
                LEFT JOIN osoba o ON os.osoba_id = o.id
                ORDER BY s.rok_produkcji DESC
                LIMIT ?
            '''
            cursor.execute(query, (n,))
            results = cursor.fetchall()
            print(f"\n=== TOP {n} NAJNOWSZYCH SAMOCHODÓW ===")
            for i, (marka, model, kolor, rok, cena, imie, nazwisko) in enumerate(results, 1):
                print(f"{i}. {marka} {model} ({rok}, {kolor}) - {int(cena)} zł")
                if imie:
                    print(f"    └─ Właściciel: {imie} {nazwisko}")
        else:
            print("Nieprawidłowa opcja")
            
    except ValueError:
        print("Proszę wprowadzić prawidłowe liczby")
    finally:
        conn.close()


def wlasne_zapytanie():
    """Możliwość wprowadzenia własnego zapytania SQL"""
    conn, cursor = connect_to_database()
    if not conn:
        return
    
    print("Dostępne tabele i kolumny:")
    print("osoba: id, imie, nazwisko, wiek, data_urodzenia")
    print("samochod: id, marka, model, kolor, rok_produkcji, cena")
    print("osoba_samochod: id, osoba_id, samochod_id, data_zakupu")
    print()
    print("Wprowadź swoje zapytanie SQL (tylko SELECT!):")
    
    query = input("SQL> ")
    
    if query.strip().upper().startswith('SELECT'):
        try:
            cursor.execute(query)
            results = cursor.fetchall()
            
            # Pobierz nazwy kolumn
            column_names = [description[0] for description in cursor.description]
            
            print("\n=== WYNIKI ZAPYTANIA ===")
            if results:
                # Wyświetl nagłówki
                header = " | ".join(f"{name:15}" for name in column_names)
                print(header)
                print("-" * len(header))
                
                # Wyświetl dane
                for row in results:
                    row_str = " | ".join(f"{str(value):15}" for value in row)
                    print(row_str)
                    
                print(f"\nZnaleziono {len(results)} rekord(ów)")
            else:
                print("Brak wyników")
                
        except sqlite3.Error as e:
            print(f"Błąd SQL: {e}")
    else:
        print("Dozwolone są tylko zapytania SELECT!")
        
    conn.close()


def demo_automatyczne():
    """Demonstracja automatyczna bez interakcji użytkownika"""
    print("\n" + "="*60)
    print("DEMONSTRACJA AUTOMATYCZNA - PRZYKŁADY ZAPYTAŃ")
    print("="*60)
    
    conn, cursor = connect_to_database()
    if not conn:
        return
    
    try:
        # Demo 1: Samochody czerwone
        print("\n1. SAMOCHODY CZERWONE:")
        query = '''
            SELECT s.marka, s.model, s.rok_produkcji, s.cena, 
                   o.imie, o.nazwisko
            FROM samochod s
            JOIN osoba_samochod os ON s.id = os.samochod_id
            JOIN osoba o ON os.osoba_id = o.id
            WHERE s.kolor = 'czerwony'
            ORDER BY s.cena DESC
        '''
        cursor.execute(query)
        results = cursor.fetchall()
        for marka, model, rok, cena, imie, nazwisko in results:
            print(f"   {marka} {model} ({rok}) - {int(cena)} zł -> {imie} {nazwisko}")
        
        # Demo 2: Samochody 100k-200k zł
        print("\n2. SAMOCHODY W PRZEDZIALE 100.000 - 200.000 ZŁ:")
        query = '''
            SELECT s.marka, s.model, s.kolor, s.rok_produkcji, s.cena,
                   o.imie, o.nazwisko
            FROM samochod s
            LEFT JOIN osoba_samochod os ON s.id = os.samochod_id
            LEFT JOIN osoba o ON os.osoba_id = o.id
            WHERE s.cena BETWEEN 100000 AND 200000
            ORDER BY s.cena DESC
        '''
        cursor.execute(query)
        results = cursor.fetchall()
        for marka, model, kolor, rok, cena, imie, nazwisko in results:
            print(f"   {marka} {model} ({kolor}, {rok}) - {int(cena)} zł")
            if imie:
                print(f"      └─ Właściciel: {imie} {nazwisko}")
        
        # Demo 3: TOP 3 najdroższe samochody
        print("\n3. TOP 3 NAJDROŻSZE SAMOCHODY:")
        query = '''
            SELECT s.marka, s.model, s.kolor, s.rok_produkcji, s.cena,
                   o.imie, o.nazwisko
            FROM samochod s
            LEFT JOIN osoba_samochod os ON s.id = os.samochod_id
            LEFT JOIN osoba o ON os.osoba_id = o.id
            ORDER BY s.cena DESC
            LIMIT 3
        '''
        cursor.execute(query)
        results = cursor.fetchall()
        for i, (marka, model, kolor, rok, cena, imie, nazwisko) in enumerate(results, 1):
            print(f"   {i}. {marka} {model} ({kolor}, {rok}) - {int(cena)} zł")
            if imie:
                print(f"      └─ Właściciel: {imie} {nazwisko}")
        
        # Demo 4: Właściciele 25-35 lat
        print("\n4. WŁAŚCICIELE W WIEKU 25-35 LAT:")
        query = '''
            SELECT o.imie, o.nazwisko, o.wiek,
                   COUNT(s.id) as liczba_aut,
                   SUM(s.cena) as suma_wartosci
            FROM osoba o
            LEFT JOIN osoba_samochod os ON o.id = os.osoba_id
            LEFT JOIN samochod s ON os.samochod_id = s.id
            WHERE o.wiek BETWEEN 25 AND 35
            GROUP BY o.id, o.imie, o.nazwisko, o.wiek
            ORDER BY suma_wartosci DESC NULLS LAST
        '''
        cursor.execute(query)
        results = cursor.fetchall()
        for imie, nazwisko, wiek, liczba, suma in results:
            print(f"   {imie} {nazwisko} ({wiek} lat)", end="")
            if suma:
                print(f" - {liczba} aut, wartość: {int(suma)} zł")
            else:
                print(" - brak samochodów")
        
    finally:
        conn.close()


def main():
    """Menu główne"""
    print("\n" + "="*50)
    print("INTERAKTYWNE ZAPYTANIA DO BAZY DANYCH")
    print("="*50)
    print("1. Znajdź samochody według koloru")
    print("2. Znajdź samochody w przedziale cenowym")
    print("3. Znajdź właścicieli według wieku")
    print("4. TOP N zapytania")
    print("5. Własne zapytanie SQL")
    print("9. Demonstracja automatyczna")
    print("0. Wyjście")
    
    while True:
        try:
            wybor = int(input("\nWybierz opcję (0-5, 9): "))
            
            if wybor == 1:
                zapytanie_o_kolor()
            elif wybor == 2:
                zapytanie_o_przedzial_cenowy()
            elif wybor == 3:
                zapytanie_o_wiek_wlasciciela()
            elif wybor == 4:
                top_n_zapytania()
            elif wybor == 5:
                wlasne_zapytanie()
            elif wybor == 9:
                demo_automatyczne()
            elif wybor == 0:
                print("Do widzenia!")
                break
            else:
                print("Nieprawidłowy wybór!")
                
        except ValueError:
            print("Proszę wprowadzić liczbę!")
        except (KeyboardInterrupt, EOFError):
            print("\n\nUruchamiam demonstrację automatyczną...")
            demo_automatyczne()
            print("\nDo widzenia!")
            break


if __name__ == "__main__":
    main()
