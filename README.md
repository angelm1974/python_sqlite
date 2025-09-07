# Baza danych SQLite - Samochody i Osoby

## Cel i przeznaczenie

To narzędzie zostało stworzone aby pokazać, jak szybko można stworzyć interfejs do bazy danych w języku Python. Projekt demonstruje różne sposoby pracy z bazą danych SQLite:

1. **Interfejs programistyczny** - gotowe funkcje Python do wykonywania zapytań
2. **Bezpośrednie zapytania SQL** - możliwość wykonywania własnych poleceń SQL
3. **Interaktywne menu** - przyjazny interfejs użytkownika
4. **Demonstracje** - gotowe przykłady różnych typów zapytań

Można pracować zarówno przez wygodne funkcje Python, jak i bezpośrednio pisać zapytania SQL - w zależności od potrzeb i poziomu zaawansowania.

## Struktura bazy danych

Baza danych składa się z trzech tabel powiązanych relacją wiele-do-wielu:

### Tabela `osoba`
- `id` - klucz główny (INTEGER, AUTOINCREMENT)
- `imie` - imię osoby (TEXT, NOT NULL)
- `nazwisko` - nazwisko osoby (TEXT, NOT NULL) 
- `wiek` - wiek w latach (INTEGER, NOT NULL)
- `data_urodzenia` - data urodzenia (DATE)

### Tabela `samochod`
- `id` - klucz główny (INTEGER, AUTOINCREMENT)
- `marka` - marka samochodu (TEXT, NOT NULL)
- `model` - model samochodu (TEXT, NOT NULL)
- `kolor` - kolor samochodu (TEXT, NOT NULL)
- `rok_produkcji` - rok produkcji (INTEGER, NOT NULL)
- `cena` - cena w złotych (REAL)

### Tabela `osoba_samochod` (relacja wiele-do-wielu)
- `id` - klucz główny (INTEGER, AUTOINCREMENT)
- `osoba_id` - klucz obcy do tabeli osoba (INTEGER, NOT NULL)
- `samochod_id` - klucz obcy do tabeli samochod (INTEGER, NOT NULL)
- `data_zakupu` - data zakupu samochodu (DATE)
- Ograniczenie UNIQUE(osoba_id, samochod_id) - zapobiega duplikatom

## Dane przykładowe

### Osoby (8 rekordów)
- Jan Kowalski (25 lat)
- Anna Nowak (30 lat)
- Piotr Wiśniewski (22 lata)
- Katarzyna Wójcik (28 lat)
- Tomasz Kowalczyk (35 lat)
- Magdalena Kamińska (19 lat)
- Andrzej Lewandowski (45 lat)
- Monika Dąbrowska (33 lata)

### Samochody (10 rekordów)
Różne marki: Toyota, BMW, Audi, Ford, Mercedes, Volkswagen, Skoda, Honda, Nissan, Opel
Różne kolory: czerwony, czarny, biały, niebieski, srebrny, szary, zielony
Ceny od 55.000 do 250.000 zł

### Relacje właściciel-samochód (11 rekordów)
Niektóre osoby posiadają więcej niż jeden samochód

## Pliki w projekcie
Można zacząć uruchamianie projektu od zapytania.py ponieważ baza już jest stworzona i w środku są dane.
Plik podstawowy.py pokazuje jak stworzyć baze i wgrać do niej dane w pythonie.
Można również wykonywać same zapytania SELECT w pliku zapytania.py.
### `podstawowy.py`
Główny plik zawierający:
- Funkcję `create_database()` - tworzenie struktury bazy danych
- Funkcję `insert_sample_data()` - wstawianie przykładowych danych
- Funkcję `main()` - uruchamianie całego procesu

### `zapytania.py`
Plik z zapytaniami SELECT zawierający funkcje:

### Podstawowe zapytania:
1. **ile_samochodow_maja_osoby()** - zlicza samochody dla każdej osoby
2. **wlasciciele_czerwonych_samochodow()** - pokazuje właścicieli czerwonych aut
3. **wlasciciele_ponizej_21_lat()** - właściciele młodsi niż 21 lat
4. **najdrozsze_samochody_i_wlasciciele()** - TOP 5 najdroższych aut
5. **samochody_wedlug_koloru()** - statystyki kolorów
6. **sredni_wiek_wlascicieli_wedlug_marki()** - średni wiek według marek
7. **osoby_bez_samochodu()** - osoby bez żadnego auta
8. **dostepne_kolory_samochodow()** - lista dostępnych kolorów
9. **wszystkie_samochody_z_wlascicielami()** - pełna lista z datami zakupu
10. **samochody_wyzsze_od_sredniej_ceny()** - auta droższe od średniej

### Zaawansowane zapytania z agregatami:
11. **statystyki_cenowe()** - MIN, MAX, AVG, SUM cen samochodów
12. **statystyki_wiekowe_osob()** - statystyki wiekowe z grupowaniem
13. **ranking_najdrozszych_marek()** - ranking marek według średniej ceny
14. **analiza_kolorow_z_cena()** - analiza kolorów z cenami i rokami
15. **najbogatsi_wlasciciele()** - właściciele według wartości posiadanych aut
16. **analiza_rocznikowa()** - analiza według roku produkcji z GROUP_CONCAT
17. **porownanie_wiek_wartosc_aut()** - porównanie grup wiekowych z CASE WHEN
18. **top_kombinacje_marka_kolor()** - kombinacje marka-kolor z HAVING
19. **analiza_dat_zakupu()** - analiza dat z funkcjami strftime()

### `interaktywne_zapytania.py`
Plik z interaktywnym menu zawierający:

1. **zapytanie_o_kolor()** - interaktywny wybór koloru samochodu
2. **zapytanie_o_przedzial_cenowy()** - wyszukiwanie w przedziale cen
3. **zapytanie_o_wiek_wlasciciela()** - wyszukiwanie właścicieli według wieku  
4. **top_n_zapytania()** - różne rankingi TOP N
5. **wlasne_zapytanie()** - możliwość wprowadzenia własnego SQL
6. **demo_automatyczne()** - demonstracja bez interakcji (opcja 9)
7. **main()** - menu główne z opcjami wyboru

### `demo.py`
Plik z szybką demonstracją zawierający:

1. **demo_szybkie()** - automatyczne uruchomienie najważniejszych zapytań:
   - Podstawowe statystyki (liczba rekordów)
   - TOP 3 najdroższe samochody
   - Popularność kolorów
   - Najbogatsi właściciele
   - Średni wiek właścicieli według marki
   - Właściciele czerwonych samochodów
   - Statystyki cenowe (MIN, MAX, AVG, SUM)

## Funkcje SQL wykorzystywane w zapytaniach

### Podstawowe agregaty:
- **COUNT()** - zliczanie rekordów
- **SUM()** - sumowanie wartości
- **AVG()** - średnia arytmetyczna
- **MIN()**, **MAX()** - wartości minimalne i maksymalne
- **ROUND()** - zaokrąglanie liczb

### Zaawansowane funkcje:
- **GROUP_CONCAT()** - łączenie wartości w grupach
- **CASE WHEN** - instrukcje warunkowe
- **strftime()** - formatowanie dat
- **HAVING** - filtrowanie grup
- **LEFT JOIN** - łączenia zewnętrzne
- **DISTINCT** - unikalne wartości
- **LIMIT** - ograniczanie liczby wyników
- **ORDER BY** - sortowanie

## Przykładowe zapytania SQL

### Zliczanie samochodów na osobę
```sql
SELECT o.imie, o.nazwisko, COUNT(os.samochod_id) as liczba_samochodow
FROM osoba o
LEFT JOIN osoba_samochod os ON o.id = os.osoba_id
GROUP BY o.id, o.imie, o.nazwisko
ORDER BY liczba_samochodow DESC
```

### Statystyki cenowe (agregaty)
```sql
SELECT 
    MIN(cena) as najnizsza_cena,
    MAX(cena) as najwyzsza_cena,
    ROUND(AVG(cena), 2) as srednia_cena,
    SUM(cena) as suma_wszystkich_cen,
    COUNT(*) as liczba_samochodow
FROM samochod
```

### Właściciele czerwonych samochodów
```sql
SELECT DISTINCT o.imie, o.nazwisko, s.marka, s.model
FROM osoba o
JOIN osoba_samochod os ON o.id = os.osoba_id
JOIN samochod s ON os.samochod_id = s.id
WHERE s.kolor = 'czerwony'
ORDER BY o.nazwisko, o.imie
```

### Ranking najdroższych marek
```sql
SELECT 
    marka,
    COUNT(*) as liczba_samochodow,
    ROUND(AVG(cena), 0) as srednia_cena,
    MIN(cena) as najtansza,
    MAX(cena) as najdrozsza
FROM samochod
GROUP BY marka
ORDER BY srednia_cena DESC
```

### Właściciele poniżej 21 lat
```sql
SELECT o.imie, o.nazwisko, o.wiek, s.marka, s.model, s.kolor, s.rok_produkcji
FROM osoba o
JOIN osoba_samochod os ON o.id = os.osoba_id
JOIN samochod s ON os.samochod_id = s.id
WHERE o.wiek < 21
ORDER BY o.wiek, o.nazwisko
```

### Średni wiek właścicieli według marki
```sql
SELECT s.marka, ROUND(AVG(o.wiek), 1) as sredni_wiek, COUNT(*) as liczba_wlascicieli
FROM samochod s
JOIN osoba_samochod os ON s.id = os.samochod_id
JOIN osoba o ON os.osoba_id = o.id
GROUP BY s.marka
ORDER BY sredni_wiek DESC
```

## Uruchamianie

1. **Tworzenie bazy danych i danych przykładowych:**
```bash
python podstawowy.py
```

2. **Szybka demonstracja (bez interakcji):**
```bash
python demo.py
```

3. **Wykonywanie wszystkich zapytań:**
```bash
python zapytania.py
```

4. **Interaktywne zapytania z menu:**
```bash
python interaktywne_zapytania.py
```

## Jak wybrać sposób pracy z bazą danych?

### Dla początkujących - gotowe funkcje Python:
```python
# Uruchom demonstrację automatyczną
python demo.py

# Albo wszystkie gotowe zapytania
python zapytania.py
```

### Dla zaawansowanych - własne zapytania SQL:
```python
# Opcja 1: Interaktywne menu z opcją własnego SQL
python interaktywne_zapytania.py
# Wybierz opcję 5 - "Własne zapytanie SQL"

# Opcja 2: Bezpośrednio w kodzie Python
import sqlite3
conn = sqlite3.connect('samochody_osoby.db')
cursor = conn.cursor()

# Twoje zapytanie SQL
cursor.execute("SELECT * FROM osoba WHERE wiek > 30")
results = cursor.fetchall()
for row in results:
    print(row)

conn.close()
```

### Dla eksploracji danych:
- **`demo.py`** - szybki przegląd najważniejszych informacji
- **`interaktywne_zapytania.py`** - filtrowanie według własnych kryteriów
- **Opcja 5 w menu** - pełna swoboda pisania zapytań SQL

## Przykłady użycia funkcji agregatów

Program demonstruje wykorzystanie różnych funkcji SQL:

### Podstawowe agregaty:
- **COUNT()** - liczenie rekordów w grupach
- **SUM()** - sumowanie wartości (np. cen samochodów)  
- **AVG()** - obliczanie średnich (wiek, cena)
- **MIN()/MAX()** - znajdowanie wartości skrajnych

### Zaawansowane funkcje:
- **GROUP_CONCAT()** - łączenie tekstów w grupach
- **CASE WHEN** - logika warunkowa w zapytaniach
- **HAVING** - filtrowanie wyników po grupowaniu
- **strftime()** - operacje na datach

### Przykłady zastosowań agregatów:
1. Statystyki cenowe wszystkich samochodów
2. Grupowanie właścicieli według przedziałów wiekowych
3. Ranking marek według średniej ceny
4. Analiza kombinacji marka-kolor
5. Porównania wartości aut między grupami wiekowymi

## Wymagania

1. **Tworzenie bazy danych i danych przykładowych:**
```bash
python podstawowy.py
```

2. **Wykonywanie zapytań:**
```bash
python zapytania.py
```

## Wymagania
- Python 3.x
- Moduł sqlite3 (wbudowany w Python)

Baza danych zostanie utworzona jako plik `samochody_osoby.db` w bieżącym katalogu.

## Praktyczne przykłady użycia

### Scenario 1: "Chcę szybko zobaczyć, co jest w bazie"
```bash
python demo.py
```

### Scenario 2: "Interesuje mnie konkretny kolor samochodu"
```bash
python interaktywne_zapytania.py
# Wybierz opcję 1, potem wybierz kolor z listy
```

### Scenario 3: "Chcę napisać własne zapytanie SQL"
```bash
python interaktywne_zapytania.py
# Wybierz opcję 5, potem wpisz swoje zapytanie, np.:
# SELECT COUNT(*) FROM osoba WHERE wiek BETWEEN 25 AND 35
```

### Scenario 4: "Chcę zobaczyć wszystkie możliwe analizy"
```bash
python zapytania.py
```

### Scenario 5: "Chcę pracować bezpośrednio w kodzie Python"
```python
import sqlite3

conn = sqlite3.connect('samochody_osoby.db')
cursor = conn.cursor()

# Przykład: Znajdź wszystkie samochody droższe niż 100k
cursor.execute("SELECT marka, model, cena FROM samochod WHERE cena > 100000")
for marka, model, cena in cursor.fetchall():
    print(f"{marka} {model}: {int(cena)} zł")

conn.close()
```

**Narzędzie pokazuje, że Python + SQLite = szybki sposób na stworzenie funkcjonalnego interfejsu do bazy danych!**
