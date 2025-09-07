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


def demo_szybkie():
    """Szybka demonstracja najważniejszych zapytań"""
    print("="*60)
    print("SZYBKA DEMONSTRACJA ZAPYTAŃ SQL")
    print("="*60)
    
    conn, cursor = connect_to_database()
    if not conn:
        print("Brak połączenia z bazą danych!")
        return
    
    try:
        # 1. Podstawowe statystyki
        print("\n1. PODSTAWOWE STATYSTYKI:")
        cursor.execute("SELECT COUNT(*) FROM osoba")
        liczba_osob = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM samochod")
        liczba_aut = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM osoba_samochod")
        liczba_relacji = cursor.fetchone()[0]
        
        print(f"   Osób w bazie: {liczba_osob}")
        print(f"   Samochodów w bazie: {liczba_aut}")
        print(f"   Relacji właściciel-samochód: {liczba_relacji}")
        
        # 2. Najdroższe samochody
        print("\n2. TOP 3 NAJDROŻSZE SAMOCHODY:")
        cursor.execute('''
            SELECT s.marka, s.model, s.cena, o.imie, o.nazwisko
            FROM samochod s
            LEFT JOIN osoba_samochod os ON s.id = os.samochod_id
            LEFT JOIN osoba o ON os.osoba_id = o.id
            ORDER BY s.cena DESC
            LIMIT 3
        ''')
        for i, (marka, model, cena, imie, nazwisko) in enumerate(cursor.fetchall(), 1):
            wlasciciel = f"({imie} {nazwisko})" if imie else "(brak właściciela)"
            print(f"   {i}. {marka} {model} - {int(cena)} zł {wlasciciel}")
        
        # 3. Statystyki kolorów
        print("\n3. POPULARNOŚĆ KOLORÓW:")
        cursor.execute('''
            SELECT kolor, COUNT(*) as liczba
            FROM samochod
            GROUP BY kolor
            ORDER BY liczba DESC, kolor
        ''')
        for kolor, liczba in cursor.fetchall():
            print(f"   {kolor.capitalize()}: {liczba} samochód(ów)")
        
        # 4. Najbogatsi właściciele
        print("\n4. NAJBOGATSI WŁAŚCICIELE:")
        cursor.execute('''
            SELECT o.imie, o.nazwisko, SUM(s.cena) as wartosc
            FROM osoba o
            JOIN osoba_samochod os ON o.id = os.osoba_id
            JOIN samochod s ON os.samochod_id = s.id
            GROUP BY o.id, o.imie, o.nazwisko
            ORDER BY wartosc DESC
        ''')
        for imie, nazwisko, wartosc in cursor.fetchall():
            print(f"   {imie} {nazwisko}: {int(wartosc)} zł")
        
        # 5. Średni wiek według marki
        print("\n5. ŚREDNI WIEK WŁAŚCICIELI WEDŁUG MARKI:")
        cursor.execute('''
            SELECT s.marka, ROUND(AVG(o.wiek), 1) as sredni_wiek
            FROM samochod s
            JOIN osoba_samochod os ON s.id = os.samochod_id
            JOIN osoba o ON os.osoba_id = o.id
            GROUP BY s.marka
            ORDER BY sredni_wiek DESC
        ''')
        for marka, wiek in cursor.fetchall():
            print(f"   {marka}: {wiek} lat")
        
        # 6. Samochody czerwone
        print("\n6. WŁAŚCICIELE CZERWONYCH SAMOCHODÓW:")
        cursor.execute('''
            SELECT o.imie, o.nazwisko, s.marka, s.model
            FROM osoba o
            JOIN osoba_samochod os ON o.id = os.osoba_id
            JOIN samochod s ON os.samochod_id = s.id
            WHERE s.kolor = 'czerwony'
            ORDER BY o.nazwisko
        ''')
        for imie, nazwisko, marka, model in cursor.fetchall():
            print(f"   {imie} {nazwisko} -> {marka} {model}")
        
        # 7. Agregaty cenowe
        print("\n7. STATYSTYKI CENOWE:")
        cursor.execute('''
            SELECT 
                MIN(cena) as min_cena,
                MAX(cena) as max_cena,
                ROUND(AVG(cena), 0) as avg_cena,
                SUM(cena) as suma_cen
            FROM samochod
        ''')
        min_c, max_c, avg_c, suma_c = cursor.fetchone()
        print(f"   Najtańszy samochód: {int(min_c)} zł")
        print(f"   Najdroższy samochód: {int(max_c)} zł")
        print(f"   Średnia cena: {int(avg_c)} zł")
        print(f"   Suma wartości wszystkich aut: {int(suma_c)} zł")
        
        print(f"\n{'='*60}")
        print("Demonstracja zakończona!")
        print("Aby uruchomić interaktywne zapytania: python interaktywne_zapytania.py")
        print("Aby zobaczyć wszystkie zapytania: python zapytania.py")
        
    except sqlite3.Error as e:
        print(f"Błąd SQL: {e}")
    finally:
        conn.close()


def main():
    """Główna funkcja"""
    demo_szybkie()


if __name__ == "__main__":
    main()
