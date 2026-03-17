<?php
/**
 * 安全 Headers 設定
 * 
 * 用途: 設定各種安全相關的 HTTP Headers
 * 作者: Aurobase Security Team
 * 日期: 2025-11-16
 * 更新: 2025-11-20 - 修正 CSP 重複定義和語法錯誤
 */

/**
 * Content Security Policy (CSP)
 * 
 * 已調整以支援:
 * - Google Analytics (GA4)
 * - Google Tag Manager
 * - YouTube 嵌入
 * - CDN 外部資源
 * - jQuery CDN
 * - Google Fonts
 */
$csp_directives = [
    "default-src 'self'",
    "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://www.googletagmanager.com https://www.google-analytics.com https://ssl.google-analytics.com https://www.google.com https://cdnjs.cloudflare.com https://cdn.jsdelivr.net https://code.jquery.com",
    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdnjs.cloudflare.com https://cdn.jsdelivr.net",
    "font-src 'self' data: https://fonts.gstatic.com https://cdnjs.cloudflare.com",
    "img-src 'self' data: https: http:",
    "connect-src 'self' https://docs.google.com https://www.google-analytics.com https://analytics.google.com https://www.google.com https://stats.g.doubleclick.net https://region1.google-analytics.com",
    "frame-src 'self' https://www.google.com https://www.googletagmanager.com https://www.youtube.com",
    "object-src 'none'",
    "base-uri 'self'",
    "form-action 'self'",
    "frame-ancestors 'self'"
];

header("Content-Security-Policy: " . implode("; ", $csp_directives));

/**
 * X-Content-Type-Options
 * 防止瀏覽器 MIME 類型嗅探
 */
header("X-Content-Type-Options: nosniff");

/**
 * X-Frame-Options
 * 防止點擊劫持攻擊
 */
header("X-Frame-Options: SAMEORIGIN");

/**
 * X-XSS-Protection
 * 啟用瀏覽器內建的 XSS 防護
 */
header("X-XSS-Protection: 1; mode=block");

/**
 * Referrer-Policy
 * 控制 Referrer 資訊的傳送
 */
header("Referrer-Policy: strict-origin-when-cross-origin");

/**
 * Strict-Transport-Security (HSTS)
 * 強制使用 HTTPS（僅在 HTTPS 環境下設定）
 */
if (
    (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ||
    $_SERVER['SERVER_PORT'] == 443
) {
    header("Strict-Transport-Security: max-age=31536000; includeSubDomains; preload");
}

/**
 * Permissions-Policy
 * 控制瀏覽器功能權限
 */
$permissions_policy = [
    "geolocation=()",
    "microphone=()",
    "camera=()",
    "payment=()",
    "usb=()",
    "magnetometer=()"
];
header("Permissions-Policy: " . implode(", ", $permissions_policy));

/**
 * Cache-Control
 * 控制快取行為（針對敏感頁面）
 */
header("Cache-Control: no-cache, no-store, must-revalidate");
header("Pragma: no-cache");
header("Expires: 0");

/**
 * 設定字元編碼
 */
header("Content-Type: text/html; charset=UTF-8");

/**
 * 移除可能洩漏資訊的 headers
 */
if (function_exists('header_remove')) {
    header_remove('X-Powered-By');
}

/**
 * 調試模式（開發環境用）
 */
define('SECURITY_DEBUG', false);

if (SECURITY_DEBUG && isset($_GET['debug-headers'])) {
    echo "<h3>已設定的安全 Headers:</h3>";
    echo "<pre>";
    foreach (headers_list() as $header) {
        echo htmlspecialchars($header) . "\n";
    }
    echo "</pre>";
    exit;
}