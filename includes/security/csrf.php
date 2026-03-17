<?php
/**
 * CSRF Token 處理類別
 * 
 * 用途: 防止跨站請求偽造攻擊
 * 作者: Aurobase Security Team
 * 日期: 2025-11-16
 */

class CSRFProtection {
    
    /**
     * Token 生命週期 (秒)
     */
    private const TOKEN_LIFETIME = 3600; // 1小時
    
    /**
     * Token 長度
     */
    private const TOKEN_LENGTH = 32;
    
    /**
     * Session key 名稱
     */
    private const SESSION_KEY = 'csrf_token';
    private const SESSION_TIME_KEY = 'csrf_token_time';
    
    /**
     * 開始 Session
     */
    private static function startSession() {
        if (session_status() === PHP_SESSION_NONE) {
            session_start();
        }
    }
    
    /**
     * 生成新的 CSRF Token
     * 
     * @return string CSRF token
     */
    public static function generateToken() {
        self::startSession();
        
        // 生成隨機 token
        $token = bin2hex(random_bytes(self::TOKEN_LENGTH));
        
        // 儲存到 session
        $_SESSION[self::SESSION_KEY] = $token;
        $_SESSION[self::SESSION_TIME_KEY] = time();
        
        return $token;
    }
    
    /**
     * 取得當前的 CSRF Token
     * 如果不存在或過期，會生成新的
     * 
     * @return string CSRF token
     */
    public static function getToken() {
        self::startSession();
        
        // 檢查是否存在且未過期
        if (self::isTokenValid()) {
            return $_SESSION[self::SESSION_KEY];
        }
        
        // 生成新 token
        return self::generateToken();
    }
    
    /**
     * 驗證 CSRF Token
     * 
     * @param string $token 要驗證的 token
     * @return bool 是否有效
     */
    public static function validateToken($token) {
        self::startSession();
        
        // 檢查 token 是否存在
        if (!isset($_SESSION[self::SESSION_KEY])) {
            return false;
        }
        
        // 檢查是否過期
        if (!self::isTokenValid()) {
            return false;
        }
        
        // 使用時間安全的比較
        return hash_equals($_SESSION[self::SESSION_KEY], $token);
    }
    
    /**
     * 檢查當前 token 是否有效
     * 
     * @return bool
     */
    private static function isTokenValid() {
        if (!isset($_SESSION[self::SESSION_KEY]) || 
            !isset($_SESSION[self::SESSION_TIME_KEY])) {
            return false;
        }
        
        $tokenAge = time() - $_SESSION[self::SESSION_TIME_KEY];
        return $tokenAge < self::TOKEN_LIFETIME;
    }
    
    /**
     * 清除 CSRF Token
     */
    public static function clearToken() {
        self::startSession();
        unset($_SESSION[self::SESSION_KEY]);
        unset($_SESSION[self::SESSION_TIME_KEY]);
    }
    
    /**
     * 產生 HTML hidden input
     * 
     * @return string HTML
     */
    public static function getTokenField() {
        $token = self::getToken();
        return sprintf(
            '<input type="hidden" name="csrf_token" value="%s" />',
            htmlspecialchars($token, ENT_QUOTES, 'UTF-8')
        );
    }
    
    /**
     * 產生 JavaScript 變數
     * 
     * @return string JavaScript code
     */
    public static function getTokenScript() {
        $token = self::getToken();
        return sprintf(
            '<script>window.CSRF_TOKEN = "%s";</script>',
            htmlspecialchars($token, ENT_QUOTES, 'UTF-8')
        );
    }
}

/**
 * 簡易函數介面
 */
function csrf_token() {
    return CSRFProtection::getToken();
}

function csrf_field() {
    return CSRFProtection::getTokenField();
}

function csrf_validate($token) {
    return CSRFProtection::validateToken($token);
}