import hashlib
import shutil
import logging
from pathlib import Path
import argparse
import sys
from tqdm import tqdm
import os
from multiprocessing import Pool, cpu_count
from datetime import datetime
import zipfile

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
    source_hashes = hash_files([file for file in source_dir.rglob('*') if file.is_file()])
    target_hashes = set(hash_files([file for file in target_dir.rglob('*') if file.is_file()]).values())

    if compare_only:
        duplicates = [file for file, hash_val in source_hashes.items() if hash_val in target_hashes]
        logging.info(f"Verglichen: Quelle: {source_dir}, Ziel: {target_dir}")
        logging.info(f"Davon Duplikate: {len(duplicates)} / {len(source_hashes)} ({len(duplicates)/len(source_hashes)*100:.2f}%)")
        create_duplicate_report(duplicates)
        ask_to_archive(duplicates, source_dir)
        return

def create_duplicate_report(duplicates):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"duplikate_{timestamp}.txt"
    with open(filename, 'w') as file:
        for item in duplicates:
            file.write(f"{item}\n")
    logging.info(f"Duplikat-Report erstellt: {filename}")

def ask_to_archive(duplicates, directory):
    response = input("Möchtest du die zurückgebliebenen Duplikate in ein Archiv komprimieren? (y/n): ")
    if response.lower() == 'y':
        archive_name = f"duplikate_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for dup in tqdm(duplicates, desc="Archivierung der Duplikate", unit="file"):
                zipf.write(dup, arcname=os.path.basename(dup))
        logging.info(f"Duplikate archiviert: {archive_name} in {directory}")

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
