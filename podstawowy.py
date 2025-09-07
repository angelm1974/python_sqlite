import sqlite3
from datetime import datetime, date

# Utworzenie połączenia z bazą danych SQLite


def create_database():
    conn = sqlite3.connect('samochody_osoby.db')
    cursor = conn.cursor()

    # Usunięcie tabel jeśli istnieją (dla czystego startu)
    cursor.execute('DROP TABLE IF EXISTS osoba_samochod')
    cursor.execute('DROP TABLE IF EXISTS samochod')
    cursor.execute('DROP TABLE IF EXISTS osoba')

    # Tworzenie tabeli osoba
    cursor.execute('''
        CREATE TABLE osoba (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            imie TEXT NOT NULL,
            nazwisko TEXT NOT NULL,
            wiek INTEGER NOT NULL,
            data_urodzenia DATE
        )
    ''')

    # Tworzenie tabeli samochod
    cursor.execute('''
        CREATE TABLE samochod (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            marka TEXT NOT NULL,
            model TEXT NOT NULL,
            kolor TEXT NOT NULL,
            rok_produkcji INTEGER NOT NULL,
            cena REAL
        )
    ''')

    # Tworzenie tabeli łączącej (relacja wiele-do-wielu)
    cursor.execute('''
        CREATE TABLE osoba_samochod (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            osoba_id INTEGER NOT NULL,
            samochod_id INTEGER NOT NULL,
            data_zakupu DATE,
            FOREIGN KEY (osoba_id) REFERENCES osoba(id),
            FOREIGN KEY (samochod_id) REFERENCES samochod(id),
            UNIQUE(osoba_id, samochod_id)
        )
    ''')

    return conn, cursor

# Wstawienie przykładowych danych


def insert_sample_data(cursor):
    # Dodawanie osób
    osoby = [
        ('Jan', 'Kowalski', 25, '1999-03-15'),
        ('Anna', 'Nowak', 30, '1994-07-22'),
        ('Piotr', 'Wiśniewski', 22, '2002-11-08'),
        ('Katarzyna', 'Wójcik', 28, '1996-05-13'),
        ('Tomasz', 'Kowalczyk', 35, '1989-09-30'),
        ('Magdalena', 'Kamińska', 19, '2005-12-18'),
        ('Andrzej', 'Lewandowski', 45, '1979-04-03'),
        ('Monika', 'Dąbrowska', 33, '1991-08-14')
    ]

    cursor.executemany('''
        INSERT INTO osoba (imie, nazwisko, wiek, data_urodzenia) 
        VALUES (?, ?, ?, ?)
    ''', osoby)

    # Dodawanie samochodów
    samochody = [
        ('Toyota', 'Corolla', 'czerwony', 2020, 85000),
        ('BMW', 'X5', 'czarny', 2019, 250000),
        ('Audi', 'A4', 'biały', 2021, 180000),
        ('Ford', 'Focus', 'czerwony', 2018, 65000),
        ('Mercedes', 'C-Class', 'srebrny', 2022, 220000),
        ('Volkswagen', 'Golf', 'niebieski', 2020, 95000),
        ('Skoda', 'Octavia', 'zielony', 2019, 75000),
        ('Honda', 'Civic', 'czerwony', 2021, 90000),
        ('Nissan', 'Qashqai', 'szary', 2020, 110000),
        ('Opel', 'Astra', 'biały', 2017, 55000)
    ]

    cursor.executemany('''
        INSERT INTO samochod (marka, model, kolor, rok_produkcji, cena) 
        VALUES (?, ?, ?, ?, ?)
    ''', samochody)

    # Dodawanie relacji osoba-samochód (właściciele)
    relacje = [
        (1, 1, '2023-01-15'),  # Jan Kowalski -> Toyota Corolla
        (1, 4, '2023-06-20'),  # Jan Kowalski -> Ford Focus (czerwony)
        (2, 2, '2022-11-10'),  # Anna Nowak -> BMW X5
        (2, 5, '2024-03-05'),  # Anna Nowak -> Mercedes C-Class
        (3, 6, '2023-09-12'),  # Piotr Wiśniewski -> Volkswagen Golf
        (4, 3, '2023-04-18'),  # Katarzyna Wójcik -> Audi A4
        (4, 8, '2024-01-25'),  # Katarzyna Wójcik -> Honda Civic (czerwony)
        (5, 7, '2022-08-30'),  # Tomasz Kowalczyk -> Skoda Octavia
        (6, 9, '2024-02-14'),  # Magdalena Kamińska -> Nissan Qashqai
        (7, 10, '2021-12-08'),  # Andrzej Lewandowski -> Opel Astra
        (8, 1, '2024-05-22'),  # Monika Dąbrowska -> Toyota Corolla (też czerwona)
    ]

    cursor.executemany('''
        INSERT INTO osoba_samochod (osoba_id, samochod_id, data_zakupu) 
        VALUES (?, ?, ?)
    ''', relacje)


def main():
    # Tworzenie bazy danych i tabel
    conn, cursor = create_database()

    print("Tworzenie bazy danych i wstawianie przykładowych danych...")
    insert_sample_data(cursor)
    conn.commit()
    print("Baza danych utworzona pomyślnie!")

    # Zamknięcie połączenia
    conn.close()
    print("Baza danych zamknięta.")
    print("\nAby wykonać zapytania SELECT, uruchom plik zapytania.py")


if __name__ == "__main__":
    main()
