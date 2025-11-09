# 💾 Ultra-Fast Bitcoin Address Importer (SQLite Optimized)

> ⚙️ **High-performance tool for bulk importing Bitcoin addresses into SQLite**  
> This script is designed to efficiently **load millions of addresses** line-by-line  
> into a local SQLite database with **maximum speed**, **progress tracking**,  
> and **real-time counters**.

---

## 🚀 Overview

This tool imports a huge list of Bitcoin addresses (e.g., from a text file)  
into an SQLite database (`addresses11.db`).  

It’s optimized for speed using:
- 🚀 PRAGMA optimizations  
- 🧮 Batched inserts  
- 🔁 Real-time progress updates via multiprocessing  
- 💾 Single-transaction commit (massively faster than per-line commits)

The importer is ideal for creating or populating large **address lookup databases**  
for later blockchain analysis or seed-checking tools.

---

## ✨ Features

| Feature | Description |
|----------|--------------|
| ⚙️ **SQLite PRAGMA optimization** | Turns off journaling & sync for raw speed |
| 📊 **Live progress indicator** | Displays import progress with dynamic updates |
| 💾 **Single-transaction bulk insert** | Commits once at the end for maximum efficiency |
| 🧮 **Address filtering** | Imports only Bitcoin-style addresses (1, 3, bc1) |
| 🧠 **Automatic total estimation** | Estimates total records from file size |
| 🧵 **Threaded UI counter** | Updates status in real time during import |
| 🧰 **Safe deduplication** | Uses `INSERT OR IGNORE` to skip duplicates automatically |

---

## 📂 File Structure

| File | Description |
|------|-------------|
| `import_addresses.py` | Main script |
| `adresy21.txt` | Input text file containing addresses (one per line) |
| `addresses11.db` | Output SQLite database |
| `README.md` | This documentation |

---

## ⚙️ Configuration

| Variable | Description |
|-----------|-------------|
| `file_path` | Path to input address file (default: `adresy21.txt`) |
| `db_file` | SQLite database file name (default: `addresses11.db`) |
| `batch` | Number of addresses inserted per batch (10 million) |
| `total_guess` | Estimated total addresses (based on file size / 64 bytes) |

**Dependencies**

No external libraries required.  
Python standard libraries: `os`, `time`, `threading`, `multiprocessing`, `sqlite3`.

---

## 🧠 How It Works

### 1️⃣ Estimate Total  
Before import, the script estimates total records by dividing the file size by ~64 bytes per line.

```python
total_guess = os.path.getsize(file_path) // 64
2️⃣ Initialize Progress Thread

A live progress display runs in a separate thread, updating every second:

print(f"📊 POSTĘP: {current} / ~{total_guess} adresów ({percent:.2f}%)", end='\r')

3️⃣ SQLite Optimization

The script sets fast-write PRAGMA options for high-speed importing:

conn.execute('PRAGMA synchronous = OFF')
conn.execute('PRAGMA journal_mode = OFF')
conn.execute('PRAGMA locking_mode = EXCLUSIVE')
conn.execute('PRAGMA temp_store = MEMORY')
conn.execute('PRAGMA cache_size = 1000000')


This drastically improves bulk performance (10×–100× faster).

4️⃣ Address Filtering

Only valid Bitcoin-style addresses are inserted (those starting with 1, 3, or b):

if address and address[0] in ("1", "3", "b"):
    batch.append((address,))

5️⃣ Batched Insert + Final Commit

Addresses are inserted in batches (10 million rows per block).
One single commit at the end avoids slow disk I/O loops.

c.executemany('INSERT OR IGNORE INTO addresses (address) VALUES (?)', batch)
conn.commit()

🧾 Example Output
🔍 Szacowana liczba adresów: ~31500000
📊 POSTĘP: 14560000 / ~31500000 adresów (46.22%) 
✅ GOTOWE: 31500420 adresów załadowanych.
✅ Import zakończony.

🧩 Core Functions
Function	Description
print_counter()	Displays real-time progress and completion percentage
import_addresses_line_by_line()	Imports all addresses from file into SQLite with batch commits
main()	Entry point, calls import function with defaults
⚡ Performance Tips

💾 Use SSD storage for huge databases — improves insert speed drastically.

🚀 Increase batch size if you have enough RAM (default 10M).

🔧 Keep PRAGMA settings as-is for fastest performance.

🧮 Avoid running concurrent imports on the same DB file.

🔄 Use .VACUUM after import to optimize database size if needed.

🔒 Ethical & Legal Notice

This script is a data management utility, intended for research, analysis,
and database preparation only. It does not interact with private keys or wallets.

You may:

Import and analyze address datasets you own.

Build offline lookup databases for auditing or research.

Use for blockchain statistics or seed-check tools.

You must not:

Combine this tool with unauthorized data or illegal scraping.

Use it for private or confidential address lists without consent.

Always ensure compliance with local laws and ethical guidelines.

🧰 Suggested Improvements

📈 Add progress logging to file.

💾 Include support for .gz or .zip compressed lists.

🧮 Add multiprocessing import for multi-core performance.

⚙️ Support multiple database shards for parallel writes.

🧩 Add resume/restart support for partial imports.

🪪 License

MIT License
© 2025 — Author: [Ethicbrudhack]

💡 Summary

This importer is a lightning-fast, memory-efficient solution
for converting huge address text files into structured SQLite databases.

⚡ Built for speed, designed for reliability, crafted for researchers.

BTC donation address: bc1q4nyq7kr4nwq6zw35pg0zl0k9jmdmtmadlfvqhr
