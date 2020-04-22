package com.example.crimson;

import android.os.Bundle;
import android.webkit.*;
import androidx.appcompat.app.AppCompatActivity;
import android.*;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import android.Manifest;
import android.annotation.SuppressLint;
import android.app.DownloadManager;
import android.content.pm.PackageManager;
import android.net.Uri;

import android.os.Environment;
import android.util.Log;
import android.view.View;

import android.widget.Toast;
import androidx.core.app.ActivityCompat;
import android.content.Intent;
import android.widget.FrameLayout;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.ConnectivityManager;

import java.io.*;
import java.net.URL;
import java.util.Scanner;

public class MainActivity extends AppCompatActivity {

    private WebView webView;
    String url;
    String domain_url;

    @Override
    protected void onSaveInstanceState(Bundle outState) {
        webView.saveState(outState);
    }

    @Override
    protected void onCreate(final Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
        // RequestQueue queue = Volley.newRequestQueue(this);
        // String urls ="http://0b1fe95c.ngrok.io/dashboard/keydata/data/";

        // StringRequest stringRequest = new StringRequest(Request.Method.GET, urls,
        //             new Response.Listener<String>() {
        //     @Override
        //     public void onResponse(String response) {
        //         domain_url=response.toString();
        //         System.out.println("Response is: "+ response);
        //     }
        // }, new Response.ErrorListener() {
        //     @Override
        //     public void onErrorResponse(VolleyError error) {
        //         System.out.println("!!!!!!!!!!!!!!!!");
        //     }
        // });

        // queue.add(stringRequest);

        android_permission();
        setUpWebView(savedInstanceState);


    }

    // ==============================function============================================================

    @SuppressLint("SetJavaScriptEnabled")
    // @Override
    public void setUpWebView(final Bundle savedInstanceState) {

        webView = (WebView) findViewById(R.id.webview);// .restoreState(savedInstanceState);

        WebSettings webSettings = webView.getSettings();

        webView.setWebChromeClient(new ChromeClient());
        webSettings.setJavaScriptEnabled(true);
        webSettings.setJavaScriptCanOpenWindowsAutomatically(true);
        webSettings.setLoadWithOverviewMode(true);
        webSettings.setUseWideViewPort(true);
        webSettings.setSupportZoom(true);
        webSettings.setAllowFileAccess(true);
        webSettings.setAllowContentAccess(true);
        webSettings.setDisplayZoomControls(true);
        // webSettings.setAppCacheEnabled(true);
        // webSettings.setUserAgentString(
        // "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko)
        // Chrome/81.0.4044.96 Mobile Safari/537.36");
        webSettings.setUserAgentString(
                "Mozilla/5.0 (Linux; Android 5.1.1; Nexus 5 Build/LMY48B; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.65 Mobile Safari/537.36");
        webView.getSettings().setRenderPriority(WebSettings.RenderPriority.HIGH);
        webSettings.setSavePassword(true);
        webSettings.setSaveFormData(true);
        webSettings.setEnableSmoothTransition(true);

        webSettings.setDomStorageEnabled(true);
        webSettings.setDatabaseEnabled(true);
        webSettings.setBlockNetworkLoads(false);
        // webView.setWebViewClient(new WebViewClient());
        webView.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, String url) {
                if (URLUtil.isNetworkUrl(url)) {
                    return false;
                }
                if (appInstalledOrNot(url)) {
                    Intent intent = new Intent(Intent.ACTION_VIEW, Uri.parse(url));
                    startActivity(intent);
                } else {
                    // do something if app is not installed
                }
                return true;
            }

        });

        webView.setDownloadListener(new DownloadListener() {
            @Override
            public void onDownloadStart(final String url, final String userAgent, final String contentDisposition,
                    final String mimeType, final long contentLength) {
                final DownloadManager.Request request = new DownloadManager.Request(Uri.parse(url));
                request.setMimeType(mimeType);
                final String cookies = CookieManager.getInstance().getCookie(url);
                request.addRequestHeader("cookie", cookies);
                request.addRequestHeader("User-Agent", userAgent);
                request.setDescription("Downloading File...");
                request.setTitle(URLUtil.guessFileName(url, contentDisposition, mimeType));
                request.allowScanningByMediaScanner();
                request.setNotificationVisibility(DownloadManager.Request.VISIBILITY_VISIBLE_NOTIFY_COMPLETED);
                request.setDestinationInExternalPublicDir(Environment.DIRECTORY_DOWNLOADS,
                        URLUtil.guessFileName(url, contentDisposition, mimeType));
                final DownloadManager dm = (DownloadManager) getSystemService(DOWNLOAD_SERVICE);
                assert dm != null;
                dm.enqueue(request);
                Toast.makeText(getApplicationContext(), "Downloading File", Toast.LENGTH_LONG).show();
            }
        });

        if (savedInstanceState != null)
            ((WebView) findViewById(R.id.webview)).restoreState(savedInstanceState);
        else
            loadWebSite();

    }

    public String readFile() {
        final StringBuilder text = new StringBuilder();
        try {
            final BufferedReader br = new BufferedReader(
                    new InputStreamReader(getResources().openRawResource(R.raw.domain)));
            String line;
            while ((line = br.readLine()) != null) {
                text.append(line);
                text.append('\n');
                System.out.println(text);
            }
            br.close();
        } catch (final IOException ignored) {
        }
        final int i = Log.i("Error", "DODO");

        return text.toString();
    }

    private void loadWebSite() {
        String domain;
        domain = readFile();
        url = "http://"+domain+"/";
        
        webView.loadUrl(url);
    }

    private boolean appInstalledOrNot(String uri) {
        PackageManager pm = getPackageManager();
        try {
            pm.getPackageInfo(uri, PackageManager.GET_ACTIVITIES);
            return true;
        } catch (PackageManager.NameNotFoundException e) {
        }

        return false;
    }

    public void android_permission() {
        if (android.os.Build.VERSION.SDK_INT >= 23) {
            if (checkSelfPermission(Manifest.permission.READ_EXTERNAL_STORAGE) == PackageManager.PERMISSION_GRANTED) {
                Log.v("permission", "Permissiongranted-1");

            } else {
                Log.v("permission", " Permission is revoked-1 ");
                ActivityCompat.requestPermissions(this, new String[] { Manifest.permission.READ_EXTERNAL_STORAGE }, 3);
            }
        } else {
            Log.v("permission", "Permission is granted1");
        }

        if (android.os.Build.VERSION.SDK_INT >= 23) {
            if (checkSelfPermission(Manifest.permission.WRITE_EXTERNAL_STORAGE) == PackageManager.PERMISSION_GRANTED) {
                Log.v("permission", "Permissiongranted-2");
            } else {
                Log.v("permission", " Permission is revoked-2 ");
                ActivityCompat.requestPermissions(this, new String[] { Manifest.permission.WRITE_EXTERNAL_STORAGE }, 2);
            }
        } else {
            Log.v("permission", "Permission is granted2");
        }
    }

    private class ChromeClient extends WebChromeClient {
        private View mCustomView;
        private WebChromeClient.CustomViewCallback mCustomViewCallback;
        protected FrameLayout mFullscreenContainer;
        private int mOriginalOrientation;
        private int mOriginalSystemUiVisibility;

        ChromeClient() {
        }

        public Bitmap getDefaultVideoPoster() {
            if (mCustomView == null) {
                return null;
            }
            return BitmapFactory.decodeResource(getApplicationContext().getResources(), 2130837573);
        }

        public void onHideCustomView() {
            ((FrameLayout) getWindow().getDecorView()).removeView(this.mCustomView);
            this.mCustomView = null;
            getWindow().getDecorView().setSystemUiVisibility(this.mOriginalSystemUiVisibility);
            setRequestedOrientation(this.mOriginalOrientation);
            this.mCustomViewCallback.onCustomViewHidden();
            this.mCustomViewCallback = null;
        }

        public void onShowCustomView(View paramView, WebChromeClient.CustomViewCallback paramCustomViewCallback) {
            if (this.mCustomView != null) {
                onHideCustomView();
                return;
            }
            this.mCustomView = paramView;
            this.mOriginalSystemUiVisibility = getWindow().getDecorView().getSystemUiVisibility();
            this.mOriginalOrientation = getRequestedOrientation();
            this.mCustomViewCallback = paramCustomViewCallback;
            ((FrameLayout) getWindow().getDecorView()).addView(this.mCustomView, new FrameLayout.LayoutParams(-1, -1));
            getWindow().getDecorView().setSystemUiVisibility(3846 | View.SYSTEM_UI_FLAG_LAYOUT_STABLE);
        }
    }

    @Override
    public void onBackPressed() {
        if (webView.canGoBack()) {
            webView.goBack();
        } else {
            super.onBackPressed();
        }
    }

}
