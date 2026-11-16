#!/usr/bin/env python3
"""Passt das frisch erzeugte Capacitor-Android-Projekt an (Signatur, Splash, Icons). Nach `npx cap add android` ausfuehren."""
import glob, subprocess
from PIL import Image
RES = 'android/app/src/main/res'
# Signatur: Keystore kommt aus Umgebungsvariablen, nie aus dem Repo
p = 'android/app/build.gradle'; s = open(p).read()
if 'KERB_KEYSTORE' not in s and 'LOT_KEYSTORE' not in s:
    s = s.replace("    buildTypes {\n        release {\n",
"""    signingConfigs {
        release {
            // Keystore liegt NICHT im Repo: LOT_KEYSTORE, LOT_STOREPASS, LOT_KEYALIAS, LOT_KEYPASS
            if (System.getenv('LOT_KEYSTORE')) {
                storeFile file(System.getenv('LOT_KEYSTORE'))
                storePassword System.getenv('LOT_STOREPASS')
                keyAlias System.getenv('LOT_KEYALIAS')
                keyPassword System.getenv('LOT_KEYPASS')
            }
        }
    }
    buildTypes {
        release {
            if (System.getenv('LOT_KEYSTORE')) { signingConfig signingConfigs.release }
""", 1)
    open(p, 'w').write(s)
# Splash: dunkel, ohne Capacitor-Logo
for f in glob.glob(RES + '/drawable*/splash.png'):
    w, h = Image.open(f).size; Image.new('RGB', (w, h), (31, 28, 23)).save(f)
p = RES + '/values/styles.xml'; s = open(p).read()
if 'windowSplashScreenBackground' not in s:
    s = s.replace('<item name="android:background">@drawable/splash</item>',
      '<item name="android:background">@drawable/splash</item>\n        <item name="windowSplashScreenBackground">#1F1C17</item>\n        <item name="windowSplashScreenAnimatedIcon">@mipmap/ic_launcher_foreground</item>\n        <item name="postSplashScreenTheme">@style/AppTheme.NoActionBar</item>')
    open(p, 'w').write(s)
import os
if os.path.exists(RES + '/drawable-v24/ic_launcher_foreground.xml'): os.remove(RES + '/drawable-v24/ic_launcher_foreground.xml')
subprocess.check_call(['python3', 'tools/make_icons.py', RES])
# Komplett offline: keine Internet-Berechtigung, kein Cloud-Backup
m = RES + '/../AndroidManifest.xml'; s = open(m).read()
if 'tools:node="remove"' not in s:
    s = s.replace('<manifest xmlns:android="http://schemas.android.com/apk/res/android">', '<manifest xmlns:android="http://schemas.android.com/apk/res/android"\n    xmlns:tools="http://schemas.android.com/tools">')
    s = s.replace('android:allowBackup="true"', 'android:allowBackup="false"\n        android:fullBackupContent="false"\n        android:dataExtractionRules="@xml/data_extraction_rules"\n        android:usesCleartextTraffic="false"\n        tools:replace="android:allowBackup"')
    s = s.replace('<uses-permission android:name="android.permission.INTERNET" />', '<uses-permission android:name="android.permission.INTERNET" tools:node="remove" />\n    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" tools:node="remove" />')
    open(m, 'w').write(s)
    open(RES + '/xml/data_extraction_rules.xml', 'w').write('<?xml version="1.0" encoding="utf-8"?>\n<data-extraction-rules>\n    <cloud-backup>\n        <exclude domain="root" /><exclude domain="file" /><exclude domain="database" /><exclude domain="sharedpref" /><exclude domain="external" />\n    </cloud-backup>\n</data-extraction-rules>\n')
# Verschlüsselung: eigenes Plugin (Android Keystore) und MainActivity, die es registriert
import shutil
JAVA = RES + '/../java/de/lot/app'
for f in ('LotCryptoPlugin.java', 'MainActivity.java'): shutil.copy('tools/android/' + f, JAVA + '/' + f)
print('Android-Projekt angepasst')
