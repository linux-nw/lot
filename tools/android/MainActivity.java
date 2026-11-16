package de.lot.app;

import android.os.Bundle;

import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {
    @Override
    public void onCreate(Bundle savedInstanceState) {
        registerPlugin(LotCryptoPlugin.class); // eigenes Plugin: Verschlüsselung über den Android Keystore
        super.onCreate(savedInstanceState);
    }
}
