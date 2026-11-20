# Lot

**Status:** 🟢 Aktiv · Version 1.6

Stempeluhr für Android. Ein Button, kein Kommen/Gehen-Gewähle: Die Reihenfolge der Stempel entscheidet, Pausen ergeben sich von selbst.

**Name:** Das Lot war eine alte Masseneinheit, ungefähr ein Löffel voll, bis ins 19. Jahrhundert im Gebrauch. Das Logo ist ein Kerbstab, auf dem früher mitgeschrieben wurde. Lot misst dafür deine Arbeitszeit statt Gewicht.

---

## Download

➡️ [Neueste Version (APK)](https://github.com/linux-nw/lot/releases/latest)

Die APK kommt nicht aus dem Play Store, deshalb fragt Android bei der Installation einmalig nach der Erlaubnis für "Unbekannte Quellen". Das ist normal. Die SHA-256-Prüfsumme steht in den Release-Notes.

---

## Nutzung

1. App öffnen, Soll-Arbeitszeit und optional Bundesland einstellen.
2. Den Stempel-Button drücken. Kommen, Gehen und Pausen leitet Lot aus der Reihenfolge ab.
3. Vergessen? Nachtragen oder ändern, alles wird neu berechnet.

---

## Selbst bauen

Voraussetzungen: Node 22, JDK 21, Android SDK (Plattform 36).

```bash
npm install
npx cap sync android
cd android && ./gradlew assembleRelease
```

Für ein signiertes APK die Umgebungsvariablen `LOT_KEYSTORE`, `LOT_STOREPASS`, `LOT_KEYALIAS` und `LOT_KEYPASS` setzen. Ohne sie entsteht ein unsigniertes APK.

---

## Repo-Struktur

```
www/        die gesamte App (index.html) und lokale Schriften
android/    Capacitor-Android-Projekt
tools/      Hilfsskripte (Icons, Android-Patch, Schulferien-Daten)
assets/     App-Icon
```

---

## Datenschutz

Alles bleibt auf dem Gerät, verschlüsselt (AES-256-GCM, Schlüssel im Android Keystore). Kein Konto, keine Cloud, kein Tracking, keine Internet-Berechtigung.

---

## Lizenz

[MIT](LICENSE)
