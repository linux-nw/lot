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
print('Android-Projekt angepasst')
