import hashlib
import shutil
import logging
from pathlib import Path
import argparse
import sys
from tqdm import tqdm
import os
from multiprocessing import Pool, cpu_count

# Konfiguration des Loggings mit Zeitstempel, Schweregrad der Meldung und Meldungstext
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def file_hash(filepath):
    hasher = hashlib.sha3_256()  # Verwendung von SHA-3 256
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return filepath, hasher.hexdigest()
    except IOError as e:
        logging.error(f"Kann Datei nicht lesen {filepath}: {e}")
        return filepath, None

def hash_files(file_paths):
    with Pool(processes=cpu_count()) as pool:
        results = list(tqdm(pool.imap(file_hash, file_paths), total=len(file_paths), desc="Hashing Dateien", unit="file"))
    return dict(results)

def sync_directories(source, target, mode, compare_only=False):
    source_dir = Path(source)
    target_dir = Path(target)
    transferred_files = 0
    skipped_files = 0
    remaining_files = 0

    logging.info("Hashing der Dateien im Quellverzeichnis mit SHA-3...")
    source_hashes = hash_files([file for file in source_dir.rglob('*') if file.is_file()])
    logging.info("Hashing der Dateien im Zielverzeichnis mit SHA-3...")
    target_hashes = set(hash_files([file for file in target_dir.rglob('*') if file.is_file()]).values())

    if compare_only:
        duplicates = [file for file, hash_val in source_hashes.items() if hash_val in target_hashes]
        logging.info(f"Anzahl der Duplikate: {len(duplicates)}")
        for dup in duplicates:
            logging.info(f"Duplikat gefunden: {dup}")
        return

    files_to_copy = [file for file, hash_val in source_hashes.items() if hash_val and hash_val not in target_hashes]
    skipped_files = len(source_hashes) - len(files_to_copy)

    if not files_to_copy:
        logging.info("Keine Dateien zu übertragen.")
    else:
        logging.info("Übertrage Dateien...")
        for file_path in tqdm(files_to_copy, desc="Dateien übertragen", unit="file"):
            target_path = target_dir / file_path.relative_to(source_dir)
            target_path.parent.mkdir(parents=True, exist_ok=True)
            if mode == 'copy':
                shutil.copy2(file_path, target_path)
                transferred_files += 1
            else:
                shutil.move(file_path, target_path)
                transferred_files += 1

    # Zähle verbleibende Dateien im Quellverzeichnis
    remaining_files = len(list(source_dir.rglob('*')))
    logging.info("Synchronisation abgeschlossen.")
    logging.info(f"{transferred_files} Datei(en) {mode}iert.")
    logging.info(f"{skipped_files} Datei(en) übersprungen.")
    logging.info(f"{remaining_files} Datei(en) verbleiben im Quellverzeichnis.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Synchronisiert Dateien zwischen zwei Verzeichnissen basierend auf SHA-3 Hashwerten.")
    parser.add_argument('source', help='Quellverzeichnis', nargs='?')
    parser.add_argument('target', help='Zielverzeichnis', nargs='?')
    parser.add_argument('--move', action='store_true', help='Verschiebt Dateien statt sie zu kopieren')
    parser.add_argument('--copy', action='store_true', help='Kopiert Dateien')
    parser.add_argument('--compare', action='store_true', help='Vergleicht Dateien zwischen den Verzeichnissen auf Duplikate')
    args = parser.parse_args()

    if args.move or args.copy or args.compare:
        if not args.source or not args.target:
            logging.error("Quell- und Zielverzeichnis müssen angegeben werden.")
            sys.exit(1)
        if args.compare:
            sync_directories(args.source, args.target, None, compare_only=True)
        else:
            mode = 'move' if args.move else 'copy'
            sync_directories(args.source, args.target, mode)
    else:
        parser.print_help()
