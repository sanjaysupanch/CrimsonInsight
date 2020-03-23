package com.example.crimson;
import android.Manifest;
import android.annotation.SuppressLint;
import android.app.DownloadManager;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.util.Log;
import android.view.View;
import android.webkit.*;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import android.content.Intent;
import java.io.*;
import java.net.URL;
import java.util.Scanner;

public class MainActivity extends AppCompatActivity {

    private WebView webView;
    String url = "";

    @Override
    protected void onCreate(final Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
        android_permission();

        try {
            url = readFile();
            System.out.println(url);
            System.out.println(url.getClass());
            Log.i("DDDOD", url);
            setUpWebView("http://" + url + "/");
        } catch (final Exception e) {
            e.printStackTrace();
        }
    }

    @SuppressLint("SetJavaScriptEnabled")
    public void setUpWebView(final String url) {
        webView = (WebView) findViewById(R.id.webview);
        webView.getSettings().setLoadsImagesAutomatically(true);
        webView.getSettings().setJavaScriptEnabled(true);
        webView.getSettings().setUseWideViewPort(true);
        webView.getSettings().setDomStorageEnabled(true);
        webView.getSettings().setDatabasePath("/data/data/" + webView.getContext().getPackageName() + "/databases/");

        webView.getSettings().setDatabaseEnabled(true);
        webView.getSettings().setCacheMode(WebSettings.LOAD_CACHE_ELSE_NETWORK);
        webView.getSettings().setAppCacheEnabled(true);
        webView.setScrollBarStyle(View.SCROLLBARS_INSIDE_OVERLAY);
        webView.getSettings().setAllowFileAccess(true);
        webView.getSettings().setAllowContentAccess(true);
        // webView.setWebViewClient(new WebViewClient());

        webView.setWebViewClient(new WebViewClient() {
            // shouldOverrideUrlLoading makes this `WebView` the default handler for URLs
            // inside the app, so that links are not kicked out to other apps.
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, String url) {
                // Use an external email program if the link begins with "mailto:".
                if (url.startsWith("mailto:")) {
                    // We use `ACTION_SENDTO` instead of `ACTION_SEND` so that only email programs
                    // are launched.
                    Intent emailIntent = new Intent(Intent.ACTION_SENDTO);

                    // Parse the url and set it as the data for the `Intent`.
                    emailIntent.setData(Uri.parse(url));

                    // `FLAG_ACTIVITY_NEW_TASK` opens the email program in a new task instead as
                    // part of this application.
                    emailIntent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);

                    // Make it so.
                    startActivity(emailIntent);
                    return true;
                } else {
                    // Returning false causes WebView to load the URL while preventing it from
                    // adding URL redirects to the WebView history.
                    return false;
                }
            }
        });

        webView.loadUrl(url);

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

    @Override
    public void onBackPressed() {
        if (webView.canGoBack()) {
            webView.goBack();
        } else {
            super.onBackPressed();
        }
    }

}