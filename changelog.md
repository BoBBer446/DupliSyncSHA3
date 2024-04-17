### Changelog

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
