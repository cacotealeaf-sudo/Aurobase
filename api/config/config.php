<?php
/**
 * API 配置檔案
 * 
 * 用途: 集中管理所有配置參數
 * 作者: Aurobase Security Team
 * 日期: 2025-11-16
 */

// 防止直接訪問
if (!defined('API_ACCESS')) {
    define('API_ACCESS', true);
}

/**
 * 環境檢測
 */
$envFile = __DIR__ . '/.env';
if (file_exists($envFile)) {
    $lines = file($envFile, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
    foreach ($lines as $line) {
        if (strpos($line, '=') !== false && strpos($line, '#') !== 0) {
            list($key, $value) = explode('=', $line, 2);
            $key = trim($key);
            $value = trim($value);
            putenv("$key=$value");
            $_ENV[$key] = $value;
        }
    }
}

/**
 * Google Forms 配置
 */
define('GOOGLE_FORM_URL', getenv('GOOGLE_FORM_URL') ?: 
    'https://docs.google.com/forms/u/0/d/e/1FAIpQLScb94lqodiK-HmoCOGFBpIzOCJB7t9Kid_JcXydkXmez04H1w/formResponse'
);

/**
 * Rate Limiting 配置
 */
define('RATE_LIMIT_WINDOW', (int)getenv('RATE_LIMIT_WINDOW') ?: 60); // 秒
define('RATE_LIMIT_MAX_ATTEMPTS', (int)getenv('RATE_LIMIT_MAX_ATTEMPTS') ?: 1);

/**
 * 安全配置
 */
define('CSRF_TOKEN_LIFETIME', (int)getenv('CSRF_TOKEN_LIFETIME') ?: 3600); // 秒
define('SESSION_LIFETIME', (int)getenv('SESSION_LIFETIME') ?: 7200); // 秒

/**
 * 日誌配置
 */
define('LOG_LEVEL', getenv('LOG_LEVEL') ?: 'INFO'); // DEBUG, INFO, WARNING, ERROR
define('LOG_MAX_SIZE', (int)getenv('LOG_MAX_SIZE') ?: 10485760); // 10MB

/**
 * 輸入驗證配置
 */
define('MAX_NAME_LENGTH', 100);
define('MAX_COMPANY_LENGTH', 200);
define('MAX_MESSAGE_LENGTH', 1000);
define('MIN_NAME_LENGTH', 2);

/**
 * CORS 配置 (如果需要)
 */
define('CORS_ALLOWED_ORIGINS', getenv('CORS_ALLOWED_ORIGINS') ?: '');
define('CORS_ENABLED', !empty(CORS_ALLOWED_ORIGINS));

/**
 * 調試模式
 */
define('DEBUG_MODE', getenv('DEBUG_MODE') === 'true');

/**
 * Session 配置
 */
if (session_status() === PHP_SESSION_NONE) {
    ini_set('session.cookie_httponly', 1);
    ini_set('session.cookie_secure', !empty($_SERVER['HTTPS']));
    ini_set('session.cookie_samesite', 'Strict');
    ini_set('session.gc_maxlifetime', SESSION_LIFETIME);
}

/**
 * 錯誤處理配置
 */
if (DEBUG_MODE) {
    ini_set('display_errors', 1);
    error_reporting(E_ALL);
} else {
    ini_set('display_errors', 0);
    error_reporting(E_ALL & ~E_DEPRECATED & ~E_STRICT);
}

/**
 * 時區設定
 */
date_default_timezone_set('Asia/Taipei');

/**
 * 輔助函數
 */

/**
 * 檢查是否為開發環境
 */
function isDevelopment() {
    return DEBUG_MODE || 
           in_array($_SERVER['REMOTE_ADDR'] ?? '', ['127.0.0.1', '::1']) ||
           strpos($_SERVER['HTTP_HOST'] ?? '', 'localhost') !== false;
}

/**
 * 取得客戶端 IP
 */
function getClientIP() {
    $ip = $_SERVER['REMOTE_ADDR'] ?? 'unknown';
    
    // 檢查是否有代理 header
    if (!empty($_SERVER['HTTP_X_FORWARDED_FOR'])) {
        $ips = explode(',', $_SERVER['HTTP_X_FORWARDED_FOR']);
        $ip = trim($ips[0]);
    } elseif (!empty($_SERVER['HTTP_CLIENT_IP'])) {
        $ip = $_SERVER['HTTP_CLIENT_IP'];
    } elseif (!empty($_SERVER['HTTP_X_REAL_IP'])) {
        $ip = $_SERVER['HTTP_X_REAL_IP'];
    }
    
    return $ip;
}

/**
 * 產生唯一 ID
 */
function generateUniqueId($prefix = '') {
    return $prefix . uniqid('', true) . bin2hex(random_bytes(8));
}