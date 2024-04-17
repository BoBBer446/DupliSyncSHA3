# Datei-Synchronisierer

Dieses Skript ermöglicht es, Dateien zwischen zwei Verzeichnissen zu synchronisieren, indem es SHA-3 Hashwerte verwendet, um Duplikate zu erkennen und nur neue oder geänderte Dateien zu kopieren oder zu verschieben.

## Funktionsweise

Das Skript durchläuft die folgenden Schritte:

1. **Hash-Berechnung**: Für jede Datei im Quellverzeichnis wird ein SHA-3 Hash berechnet. Dieser Hash dient als eindeutiger Identifikator für den Inhalt jeder Datei.

2. **Vergleich der Verzeichnisse**: Es wird geprüft, ob der Hash einer Datei im Zielverzeichnis vorhanden ist. Falls nicht, wird die Datei als "zu kopieren" oder "zu verschieben" markiert.

3. **Speicherplatzprüfung**: Bevor Dateien verschoben oder kopiert werden, prüft das Skript, ob ausreichend Speicherplatz im Zielverzeichnis vorhanden ist.

4. **Dateiübertragung**: Dateien, die im Zielverzeichnis nicht vorhanden sind, werden je nach Modus kopiert oder verschoben.

5. **Logging**: Das Skript protokolliert wichtige Informationen und Fehler während des Ausführungsprozesses, um die Nachverfolgung zu erleichtern.

6. **Duplikatprüfung**: Optional kann das Skript auch verwendet werden, um zu prüfen, ob Dateien im Quellverzeichnis bereits im Zielverzeichnis existieren.

## Warum dieses Skript?

Die Verwendung von SHA-3 Hashwerten zur Identifikation von Dateien vermeidet unnötige Übertragungen von Duplikaten und sorgt dafür, dass nur tatsächlich neue oder geänderte Dateien behandelt werden. Dies spart Zeit und Speicherplatz.

## Anforderungen

- Python 3.6 oder höher
- Die Module `hashlib`, `shutil`, `pathlib`, `argparse`, `logging`, `sys`, `tqdm`, `os`, `multiprocessing`

## Installation und Nutzung

Klonen Sie das Repository und navigieren Sie in das Verzeichnis des Skripts:

```bash
git clone https://github.com/BoBBer446/python_copy2_image_duplicate_copy
cd python_copy2_image_duplicate_copy
```

### Verwendung des Scripts

Um Dateien zwischen Verzeichnissen zu synchronisieren:

```bash
# Für das Verschieben von Dateien
python sync_files.py <Quellverzeichnis> <Zielverzeichnis> --move

# Für das Kopieren von Dateien
python sync_files.py <Quellverzeichnis> <Zielverzeichnis> --copy

# Um zu prüfen, ob Duplikate im Zielverzeichnis vorhanden sind
python sync_files.py <Quellverzeichnis> <Zielverzeichnis> --compare
```

## Lizenz

Dieses Projekt ist unter der MIT Lizenz lizenziert. Sie können das Skript frei verwenden, modifizieren und verteilen. Weitere Informationen finden Sie in der `LICENSE` Datei.
