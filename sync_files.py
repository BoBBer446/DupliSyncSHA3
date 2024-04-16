import hashlib
import shutil
import logging
from pathlib import Path
import argparse
import sys

# Konfiguration des Loggings mit Zeitstempel, Schweregrad der Meldung und Meldungstext
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def file_hash(filepath):
    """
    Berechnet den SHA-256 Hash einer Datei.
    
    Args:
        filepath (Path): Der Pfad zur Datei, deren Hash berechnet werden soll.
        
    Returns:
        str: Hexadezimaler Hashwert der Datei, oder None bei Lesefehlern.
    """
    hasher = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    except IOError as e:
        logging.error(f"Kann Datei nicht lesen {filepath}: {e}")
        return None

def get_total_size_of_files(file_list):
    """
    Berechnet die Gesamtgröße einer Liste von Dateien.
    
    Args:
        file_list (list of Path): Liste von Dateipfaden, deren Größen addiert werden sollen.
        
    Returns:
        int: Gesamtgröße der Dateien in Bytes.
    """
    total_size = 0
    for file in file_list:
        try:
            total_size += file.stat().st_size
        except IOError as e:
            logging.error(f"Kann Größe nicht lesen {file}: {e}")
    return total_size

def disk_space_check(needed_space, target_directory):
    """
    Prüft, ob genügend Speicherplatz im Zielverzeichnis verfügbar ist.
    
    Args:
        needed_space (int): Benötigter Speicherplatz in Bytes.
        target_directory (Path): Zielverzeichnis.
        
    Returns:
        bool: True, wenn genügend Platz vorhanden ist, sonst False.
    """
    total, used, free = shutil.disk_usage(target_directory)
    logging.info(f"Verfügbarer Speicherplatz: {free // (1024 * 1024)} MB")
    if needed_space > free:
        logging.warning("Nicht genügend Speicherplatz verfügbar.")
        return False
    return True

def sync_directories(source, target, mode):
    """
    Synchronisiert zwei Verzeichnisse, indem Dateien basierend auf ihren Hashwerten kopiert oder verschoben werden.
    
    Args:
        source (str): Quellverzeichnis.
        target (str): Zielverzeichnis.
        mode (str): 'copy' für Kopieren, 'move' für Verschieben.
    """
    source_dir = Path(source)
    target_dir = Path(target)
    source_files = {file_hash(file): file for file in source_dir.rglob('*') if file.is_file()}
    target_files = {file_hash(file) for file in target_dir.rglob('*') if file.is_file()}
    skipped_files = []

    files_to_copy = []
    for hsh, src in source_files.items():
        if src and hsh not in target_files:
            files_to_copy.append(src)
        else:
            skipped_files.append(src)

    total_size_needed = get_total_size_of_files(files_to_copy)
    total_skipped_size = get_total_size_of_files(skipped_files)

    logging.info(f"Benötigter Speicherplatz: {total_size_needed // (1024 * 1024)} MB")
    logging.info(f"Übersprungene Dateien: {len(skipped_files)}, Gesamtgröße: {total_skipped_size // (1024 * 1024)} MB")

    if not disk_space_check(total_size_needed, target):
        return

    for file_path in files_to_copy:
        target_path = target_dir / file_path.relative_to(source_dir)
        target_path.parent.mkdir(parents=True, exist_ok=True)
        logging.info(f"Übertrage: {file_path} -> {target_path}")
        if mode == 'copy':
            shutil.copy2(file_path, target_path)
        else:
            shutil.move(file_path, target_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Synchronisiert Dateien zwischen zwei Verzeichnissen basierend auf SHA-256 Hashwerten.")
    parser.add_argument('source', help='Quellverzeichnis')
    parser.add_argument('target', help='Zielverzeichnis')
    parser.add_argument('--move', action='store_true', help='Verschiebt Dateien statt sie zu kopieren')
    args = parser.parse_args()

    if not Path(args.source).exists() or not Path(args.target).exists():
        logging.error("Eines der angegebenen Verzeichnisse existiert nicht.")
        sys.exit(1)

    try:
        operation_mode = 'move' if args.move else 'copy'
        sync_directories(args.source, args.target, operation_mode)
    except Exception as e:
        logging.error(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
        sys.exit(1)
