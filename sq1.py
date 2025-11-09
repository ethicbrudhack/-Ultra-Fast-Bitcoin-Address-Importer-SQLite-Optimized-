import os
import time
import threading
import multiprocessing
import sqlite3

def print_counter(counter, total_guess):
    while True:
        with counter.get_lock():
            current = counter.value
        percent = (current / total_guess * 100) if total_guess > 0 else 0
        print(f"📊 POSTĘP: {current} / ~{total_guess} adresów ({percent:.2f}%)", end='\r')
        if total_guess > 0 and current >= total_guess:
            break
        time.sleep(1)
    print(f"\n✅ GOTOWE: {current} adresów załadowanych.")

def import_addresses_line_by_line(file_path, db_file='addresses11.db'):
    if not os.path.exists(file_path):
        print(f"🚫 Plik '{file_path}' nie istnieje!")
        return

    # Szacujemy ilość adresów na podstawie rozmiaru pliku
    total_guess = os.path.getsize(file_path) // 64  # przyjmujemy ~64 bajty na linię
    print(f"🔍 Szacowana liczba adresów: ~{total_guess}")

    counter = multiprocessing.Value('i', 0)
    counter_thread = threading.Thread(target=print_counter, args=(counter, total_guess))
    counter_thread.start()

    # === Połączenie z SQLite z PRAGMA dla maksymalnej szybkości ===
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    conn.execute('PRAGMA synchronous = OFF')
    conn.execute('PRAGMA journal_mode = OFF')  # 🚀 szybciej niż MEMORY
    conn.execute('PRAGMA locking_mode = EXCLUSIVE')
    conn.execute('PRAGMA temp_store = MEMORY')
    conn.execute('PRAGMA cache_size = 1000000')
    c.execute('CREATE TABLE IF NOT EXISTS addresses (address TEXT PRIMARY KEY)')

    # === Jedna transakcja na całość ===
    conn.execute('BEGIN TRANSACTION;')

    batch = []
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            address = line.strip().split()[0]
            if address and address[0] in ("1", "3", "b"):  # tylko adresy BTC
                batch.append((address,))

                with counter.get_lock():
                    counter.value += 1

                if len(batch) >= 10_000_000:
                    c.executemany('INSERT OR IGNORE INTO addresses (address) VALUES (?)', batch)
                    batch = []

    # ostatnia partia
    if batch:
        c.executemany('INSERT OR IGNORE INTO addresses (address) VALUES (?)', batch)

    conn.commit()  # ✅ tylko jeden commit
    conn.close()
    counter_thread.join()
    print("✅ Import zakończony.")

# === Wykonanie ===
if __name__ == "__main__":
    import_addresses_line_by_line("adresy21.txt")
