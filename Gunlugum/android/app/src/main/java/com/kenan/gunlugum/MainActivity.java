package com.kenan.gunlugum;

import android.os.Bundle;
import android.webkit.WebView;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowCompat;
import androidx.core.view.WindowInsetsCompat;
import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        WindowCompat.setDecorFitsSystemWindows(getWindow(), false);

        final WebView webView = this.bridge.getWebView();
        ViewCompat.setOnApplyWindowInsetsListener(webView, (view, insets) -> {
            Insets bars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            float density = getResources().getDisplayMetrics().density;
            int top = Math.round(bars.top / density);
            int bottom = Math.round(bars.bottom / density);
            int left = Math.round(bars.left / density);
            int right = Math.round(bars.right / density);
            String js = "(function(){"
                + "var r=document.documentElement.style;"
                + "r.setProperty('--safe-top','" + top + "px');"
                + "r.setProperty('--safe-bottom','" + bottom + "px');"
                + "r.setProperty('--safe-left','" + left + "px');"
                + "r.setProperty('--safe-right','" + right + "px');"
                + "})();";
            ((WebView) view).evaluateJavascript(js, null);
            return insets;
        });
        ViewCompat.requestApplyInsets(webView);
    }
}
