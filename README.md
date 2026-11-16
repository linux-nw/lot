# Lot

<img src="assets/icon.png" width="96" alt="Lot Icon">

Stempeluhr für Android. Ein Button, kein Kommen/Gehen-Gewähle: Die Reihenfolge der Stempel entscheidet, Pausen ergeben sich von selbst. Alles bleibt auf dem Gerät.

## Funktionen

- Heute-Ansicht mit Tagessaldo, Gearbeitet, Soll und Stundenkonto
- Ein Stempel-Button, Kommen/Gehen und Pausen werden abgeleitet
- Nachtragen und Ändern: alles wird neu berechnet
- Gesetzliche Pause (ab 6 Std. 30 Min., ab 9 Std. 45 Min.) optional automatisch abziehen
- Kalender mit Stempelkasten: Urlaub, Berufsschule, Krank, Ausgleich, Arbeit
- Monatsansicht mit Zeitbalken pro Tag, Wochenansicht mit allen Stempelzeiten, Tageskarte mit Blöcken und Pausen
- Berufsschultage pro Wochentag: jede Woche, gerade oder ungerade Kalenderwochen und frei wählbare Arbeitstage
- Feiertage für alle 16 deutschen Bundesländer und Österreich, offline berechnet, optional
- Schulferien (amtliche Daten der OpenHolidays API, 2025 bis 2029, fest eingebaut), optional; Berufsschule entfällt in den Ferien. Neu holen: `python3 tools/fetch-ferien.py 2025 2029`
- Urlaubskonto und manuelle Stundenkonto-Buchungen
- Startdatum und Startsaldo für den Umstieg aus einem alten System

## Daten

Alle Daten liegen als JSON-Dateien im privaten App-Speicher (`lot/cfg.json`, `lot/adj.json`, `lot/m_JJJJ-MM.json`). Jede Datei wird doppelt geschrieben (`.json` und `.bak`, mit Gegenlesen); bei einer beschädigten Datei greift die Kopie. Kein Konto, keine Cloud, kein Tracking, keine Netzwerkzugriffe. Nichts im Browser-Speicher.

## Bauen

Voraussetzungen: Node 22, JDK 21, Android SDK (Plattform 36).

```bash
npm install
npx cap sync android
cd android && ./gradlew assembleRelease
```

Das Android-Projekt liegt im Repo. Nur wenn du `android/` neu erzeugst (`npx cap add android`), danach einmal `python3 tools/patch-android.py` ausführen (Splash, Icons, Signatur-Konfiguration).

Für ein signiertes Release-APK die Umgebungsvariablen `LOT_KEYSTORE`, `LOT_STOREPASS`, `LOT_KEYALIAS` und `LOT_KEYPASS` setzen. Der Keystore gehört nicht ins Repo. Ohne diese Variablen entsteht ein unsigniertes APK.

## Aufbau

- `www/index.html`: die gesamte App (Vorlage, Logik, Stile)
- `www/fonts/`: IBM Plex, lokal eingebunden
- `tools/make_icons.py`: erzeugt alle Icons aus dem Kerbstab
- `tools/patch-android.py`: Anpassungen am erzeugten Android-Projekt

## Lizenz

MIT
