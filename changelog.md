### Changelog

**Allgemeine Änderungen:**
- **Hashing-Algorithmus**: Geändert von SHA-256 zu SHA-3 (SHA3-256), um eine modernere und sicherere Hashing-Funktion zu verwenden.
- **Neues Argument `--compare`**: Hinzugefügt zur Unterstützung der Duplikatprüfung zwischen Quell- und Zielverzeichnissen, ohne Dateien zu kopieren oder zu verschieben.
- **Verbesserte Argument-Verarbeitung**: Erweitert, um sicherzustellen, dass das Skript nur ausgeführt wird, wenn `--move`, `--copy` oder `--compare` explizit angegeben werden. Ohne diese wird nur die Hilfe angezeigt.

**Technische Änderungen:**
- **SHA-3 Integration**: Das `file_hash`-Funktion wurde aktualisiert, um SHA3-256 statt SHA-256 zu verwenden, was zu einer sichereren Hash-Berechnung führt.
- **Erweiterte Funktionalität von `sync_directories`**:
  - Unterstützung für den Vergleichsmodus durch das `compare_only` Flag.
  - Im Vergleichsmodus werden Duplikate geloggt und aufgelistet, aber es erfolgt keine Übertragung der Dateien.
- **Modifikation des Hauptausführungsblocks**:
  - Die Logik zur Verarbeitung der Eingabeargumente wurde umgestaltet, um zusätzliche Flexibilität und Funktionalitäten wie `--compare` zu ermöglichen.
  - Hinzufügen einer Überprüfung, um die Hilfe zu zeigen, wenn keine spezifischen Aktionsargumente (`--move`, `--copy`, `--compare`) angegeben sind.

**Benutzerfreundlichkeit:**
- **Verbesserte Hilfeausgabe**: Die Hilfe wurde aktualisiert, um Informationen über die neuen Argumente und den geänderten Hash-Algorithmus bereitzustellen.
- **Erweiterte Logging-Informationen**: Das Logging wurde erweitert, um die Nutzung von SHA-3 zu reflektieren und zusätzliche Details während des Vergleichsprozesses bereitzustellen.

**Beispielhafte Auswirkungen der Änderungen:**
- Die Sicherheit der Datensynchronisation wurde durch die Verwendung von SHA-3 verbessert, da dieser Algorithmus als resistenter gegen Kollisionen gilt.
- Die Einführung des `--compare` Arguments ermöglicht es Benutzern, effizient Duplikate zu identifizieren, was besonders nützlich ist, wenn große Datenmengen verwaltet werden müssen.
- Die Änderung der Ausführungslogik, um nur bei spezifischen Argumenten zu agieren, verhindert ungewollte Ausführungen und macht die Bedienung sicherer und klarer.

**Neue Funktionen:**
- **Multiprocessing Unterstützung:** Hinzugefügt die Fähigkeit, Hash-Berechnungen über mehrere Prozesse parallel durchzuführen, was die Gesamtperformance insbesondere bei der Verarbeitung großer Mengen von Dateien verbessert. Dies nutzt die `multiprocessing` Bibliothek und die Anzahl der verfügbaren CPU-Kerne (`cpu_count()`).
- **Verbesserte Ausgabe:** Integration von `tqdm` für Fortschrittsbalken, die während des Hashings der Dateien in den Quell- und Zielverzeichnissen angezeigt werden. Dies gibt Benutzern eine visuelle Rückmeldung über den Fortschritt des Hashing-Prozesses.

**Geänderte Funktionen:**
- **`file_hash` Funktion:** Änderung des Rückgabewerts von nur dem Hash zu einem Tupel aus Dateipfad und Hash-Wert, um die Integration mit `multiprocessing` zu erleichtern und die Rückverfolgbarkeit zu verbessern.
- **`hash_files` Funktion:** Neu implementiert, um eine Liste von Dateipfaden zu nehmen und deren Hashes parallel zu berechnen, Rückgabe eines Wörterbuchs, das Dateipfade auf ihre Hashes abbildet.

**Optimierungen und Fehlerbehebungen:**
- **Fehlerbehandlung verbessert:** Erweiterte Fehlerbehandlung in der `file_hash` Funktion, um mit nicht lesbaren Dateien besser umzugehen und Fehler spezifischer zu loggen.
- **Effizienzsteigerung im File Handling:** Nutzung von Listen von `Path` Objekten und deren Iteration verbessert die Performance beim Zugriff und der Bearbeitung von Dateisystemoperationen.
- **Bedingte Prüfung für Kopier- und Verschiebeoperationen:** Optimierung der Speicherplatzprüfung, die nun bedingt durchgeführt wird, abhängig davon, ob Dateien zwischen verschiedenen Laufwerken (nicht nur Verzeichnissen) bewegt werden.

**Sonstige Verbesserungen:**
- **Code-Klarheit und Wartbarkeit:** Die strukturellen Änderungen und die Verwendung von beschreibenderen Variablennamen sowie Kommentaren verbessern die Lesbarkeit und Wartbarkeit des Codes.

### Zusammenfassung

Die Änderungen zielen darauf ab, das Skript leistungsfähiger, schneller und nutzerfreundlicher zu gestalten, insbesondere bei der Handhabung großer Datenmengen. Die Integration von `multiprocessing` und `tqdm` hebt die Benutzererfahrung durch sichtbare Fortschritte und bessere Nutzung der Hardware-Ressourcen hervor.
