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
    hasher = hashlib.sha256()
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

def get_total_size_of_files(file_list):
    total_size = 0
    for file in file_list:
        try:
            total_size += file.stat().st_size
        except IOError as e:
            logging.error(f"Kann Größe nicht lesen {file}: {e}")
    return total_size

def sync_directories(source, target, mode):
    source_dir = Path(source)
    target_dir = Path(target)

    source_files = list(source_dir.rglob('*'))
    target_files = list(target_dir.rglob('*'))

    logging.info("Hashing der Dateien im Quellverzeichnis...")
    source_hashes = hash_files([file for file in source_files if file.is_file()])
    logging.info("Hashing der Dateien im Zielverzeichnis...")
    target_hashes = set(hash_files([file for file in target_files if file.is_file()]).values())

    files_to_copy = [file for file, hash_val in source_hashes.items() if hash_val and hash_val not in target_hashes]
    total_size_needed = get_total_size_of_files(files_to_copy)

    logging.info(f"Benötigter Speicherplatz: {total_size_needed // (1024 * 1024)} MB")

    if mode == 'copy' or not os.stat(source_dir).st_dev == os.stat(target_dir).st_dev:
        if not disk_space_check(total_size_needed, target):
            return

    logging.info("Übertrage Dateien...")
    for file_path in tqdm(files_to_copy, desc="Dateien übertragen", unit="file"):
        target_path = target_dir / file_path.relative_to(source_dir)
        target_path.parent.mkdir(parents=True, exist_ok=True)
        if mode == 'copy':
            shutil.copy2(file_path, target_path)
        else:
            shutil.move(file_path, target_path)
    logging.info("Synchronisation abgeschlossen.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Synchronisiert Dateien zwischen zwei Verzeichnissen basierend auf SHA-256 Hashwerten.")
    parser.add_argument('source', help='Quellverzeichnis')
    parser.add_argument('target', help='Zielverzeichnis')
    parser.add_argument('--move', action='store_true', help='Verschiebt Dateien statt sie zu kopieren')
    args = parser.parse_args()

    if not Path(args.source).exists() or not Path(args.target).exists():
        logging.error("Eines der angegebenen Verzeichnisse existiert nicht.")
        sys.exit(1)

    operation_mode = 'move' if args.move else 'copy'
    sync_directories(args.source, args.target, operation_mode)
