package de.lot.app;

import android.security.keystore.KeyGenParameterSpec;
import android.security.keystore.KeyProperties;
import android.util.Base64;

import com.getcapacitor.JSObject;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;

import java.nio.charset.StandardCharsets;
import java.security.KeyStore;

import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.spec.GCMParameterSpec;

/**
 * Verschlüsselt die Daten von Lot mit AES-256-GCM.
 * Der Schlüssel wird im Android Keystore erzeugt und verlässt ihn nie (nicht exportierbar).
 * Format: "LOT1:" + Base64(IV[12] || Ciphertext+Tag)
 */
@CapacitorPlugin(name = "LotCrypto")
public class LotCryptoPlugin extends Plugin {

    private static final String ALIAS = "lot-data-key-v1";
    private static final String PREFIX = "LOT1:";
    private static final int IV_LEN = 12;
    private static final int TAG_BITS = 128;

    private static synchronized SecretKey key() throws Exception {
        KeyStore ks = KeyStore.getInstance("AndroidKeyStore");
        ks.load(null);
        if (ks.containsAlias(ALIAS)) {
            KeyStore.Entry e = ks.getEntry(ALIAS, null);
            if (e instanceof KeyStore.SecretKeyEntry) return ((KeyStore.SecretKeyEntry) e).getSecretKey();
        }
        KeyGenerator kg = KeyGenerator.getInstance(KeyProperties.KEY_ALGORITHM_AES, "AndroidKeyStore");
        kg.init(new KeyGenParameterSpec.Builder(ALIAS, KeyProperties.PURPOSE_ENCRYPT | KeyProperties.PURPOSE_DECRYPT)
            .setBlockModes(KeyProperties.BLOCK_MODE_GCM)
            .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)
            .setKeySize(256)
            .setRandomizedEncryptionRequired(true)
            .build());
        return kg.generateKey();
    }

    @PluginMethod
    public void encrypt(PluginCall call) {
        String data = call.getString("data");
        if (data == null) { call.reject("Keine Daten"); return; }
        try {
            Cipher c = Cipher.getInstance("AES/GCM/NoPadding");
            c.init(Cipher.ENCRYPT_MODE, key());
            byte[] iv = c.getIV();
            byte[] ct = c.doFinal(data.getBytes(StandardCharsets.UTF_8));
            byte[] out = new byte[iv.length + ct.length];
            System.arraycopy(iv, 0, out, 0, iv.length);
            System.arraycopy(ct, 0, out, iv.length, ct.length);
            JSObject r = new JSObject();
            r.put("data", PREFIX + Base64.encodeToString(out, Base64.NO_WRAP));
            call.resolve(r);
        } catch (Exception e) {
            call.reject("Verschlüsseln fehlgeschlagen", e);
        }
    }

    @PluginMethod
    public void decrypt(PluginCall call) {
        String data = call.getString("data");
        if (data == null || !data.startsWith(PREFIX)) { call.reject("Unbekanntes Format"); return; }
        try {
            byte[] in = Base64.decode(data.substring(PREFIX.length()), Base64.NO_WRAP);
            if (in.length <= IV_LEN) { call.reject("Zu kurz"); return; }
            Cipher c = Cipher.getInstance("AES/GCM/NoPadding");
            c.init(Cipher.DECRYPT_MODE, key(), new GCMParameterSpec(TAG_BITS, in, 0, IV_LEN));
            byte[] pt = c.doFinal(in, IV_LEN, in.length - IV_LEN);
            JSObject r = new JSObject();
            r.put("data", new String(pt, StandardCharsets.UTF_8));
            call.resolve(r);
        } catch (Exception e) {
            call.reject("Entschlüsseln fehlgeschlagen", e);
        }
    }
}
