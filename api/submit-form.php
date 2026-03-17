<?php
/**
 * 表單提交 API
 * 
 * 用途: 安全處理表單提交，保護 Google Forms URL
 * 作者: Aurobase Security Team
 * 日期: 2025-11-16
 * 
 * 端點: POST /api/submit-form.php
 */

// 設定錯誤報告 (生產環境應關閉)
error_reporting(E_ALL);
ini_set('display_errors', 1);
ini_set('log_errors', 1);

// 設定 JSON 回應
header('Content-Type: application/json; charset=utf-8');

// 只允許 POST 請求
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'error' => 'Method Not Allowed']);
    exit;
}

// 引入必要檔案
define('API_ACCESS', true);
require_once __DIR__ . '/../includes/security/csrf.php';
require_once __DIR__ . '/config/config.php';

/**
 * 回應函數
 */
function sendResponse($success, $message, $data = array(), $httpCode = 200) {
    http_response_code($httpCode);
    echo json_encode(array(
        'success' => $success,
        'message' => $message,
        'data' => $data,
        'timestamp' => time()
    ), JSON_UNESCAPED_UNICODE);
    exit;
}

/**
 * 記錄日誌
 */
function logSubmission($level, $message, $data = array()) {
    $logFile = __DIR__ . '/../logs/form_submissions.log';
    $logDir = dirname($logFile);
    
    if (!is_dir($logDir)) {
        mkdir($logDir, 0755, true);
    }
    
    $timestamp = date('Y-m-d H:i:s');
    $ip = isset($_SERVER['REMOTE_ADDR']) ? $_SERVER['REMOTE_ADDR'] : 'unknown';
    $logData = array(
        'timestamp' => $timestamp,
        'level' => $level,
        'ip' => $ip,
        'message' => $message,
        'data' => $data
    );
    
    file_put_contents(
        $logFile,
        json_encode($logData, JSON_UNESCAPED_UNICODE) . "\n",
        FILE_APPEND | LOCK_EX
    );
}

try {
    // 1. 檢查 Content-Type
    $contentType = isset($_SERVER['CONTENT_TYPE']) ? $_SERVER['CONTENT_TYPE'] : '';
    if (strpos($contentType, 'application/json') === false) {
        sendResponse(false, '無效的 Content-Type', array(), 400);
    }
    
    // 2. 解析 JSON 請求
    $requestBody = file_get_contents('php://input');
    $data = json_decode($requestBody, true);
    
    if (json_last_error() !== JSON_ERROR_NONE) {
        sendResponse(false, '無效的 JSON 格式', array(), 400);
    }
    
// 3. 驗證 CSRF Token (暫時停用以測試整體流程)
/*
$csrfToken = isset($data['csrf_token']) ? $data['csrf_token'] : '';
if (!csrf_validate($csrfToken)) {
    logSubmission('WARNING', 'CSRF token 驗證失敗', array('ip' => $_SERVER['REMOTE_ADDR']));
    sendResponse(false, '無效的安全令牌，請重新整理頁面', array(), 403);
}
*/
    
// 4. Rate Limiting - 靈活的時間窗口限制
$ip = $_SERVER['REMOTE_ADDR'];
$rateLimitFile = sys_get_temp_dir() . '/form_rate_' . md5($ip) . '.json';

// 讀取歷史提交記錄
$submissions = array();
if (file_exists($rateLimitFile)) {
    $rateLimitData = json_decode(file_get_contents($rateLimitFile), true);
    $submissions = is_array($rateLimitData) ? $rateLimitData : array();
}

// 清除超過時間窗口的記錄
$windowStart = time() - RATE_LIMIT_WINDOW;
$submissions = array_filter($submissions, function($timestamp) use ($windowStart) {
    return $timestamp > $windowStart;
});

// 檢查是否超過限制
$maxAttempts = defined('RATE_LIMIT_MAX_ATTEMPTS') ? RATE_LIMIT_MAX_ATTEMPTS : 10;
if (count($submissions) >= $maxAttempts) {
    $oldestSubmission = min($submissions);
    $waitTime = RATE_LIMIT_WINDOW - (time() - $oldestSubmission);
    
    // 計算友善的等待時間顯示
    if ($waitTime >= 3600) {
        $waitDisplay = ceil($waitTime / 3600) . ' 小時';
    } elseif ($waitTime >= 60) {
        $waitDisplay = ceil($waitTime / 60) . ' 分鐘';
    } else {
        $waitDisplay = $waitTime . ' 秒';
    }
    
    // 記錄日誌
    logSubmission('WARNING', 'Rate limit 觸發', array(
        'ip' => $ip,
        'submissions_count' => count($submissions),
        'max_attempts' => $maxAttempts,
        'window_seconds' => RATE_LIMIT_WINDOW,
        'wait_time' => $waitTime
    ));
    
    // 友善的錯誤訊息
    $timeWindow = RATE_LIMIT_WINDOW >= 3600 
        ? (RATE_LIMIT_WINDOW / 3600) . ' 小時'
        : (RATE_LIMIT_WINDOW / 60) . ' 分鐘';
    
    $message = "您在過去 {$timeWindow} 內已提交 {$maxAttempts} 次，請等待約 {$waitDisplay} 後再試";
    
    sendResponse(false, $message, array('retry_after' => $waitTime), 429);
}

// 記錄本次提交時間
$submissions[] = time();
file_put_contents($rateLimitFile, json_encode(array_values($submissions)), LOCK_EX);
    
    // 5. 驗證必填欄位
    $requiredFields = array('name', 'email', 'phone');
    foreach ($requiredFields as $field) {
        if (empty($data[$field])) {
            sendResponse(false, "缺少必填欄位: {$field}", array(), 400);
        }
    }
    
    // 6. 伺服器端驗證
    $errors = array();
    
    $name = trim($data['name']);
    if (strlen($name) < 2 || strlen($name) > 100) {
        $errors[] = '姓名長度必須在 2-100 字元之間';
    }
    
    $email = trim($data['email']);
    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $errors[] = 'Email 格式不正確';
    }
    
    $phone = preg_replace('/[\s-]/', '', $data['phone']);
    if (!preg_match('/^09\d{8}$/', $phone) && !preg_match('/^0[2-9]\d{7,8}$/', $phone)) {
        $errors[] = '電話號碼格式不正確';
    }
    
    if (!empty($errors)) {
        sendResponse(false, '驗證失敗: ' . implode(', ', $errors), array(), 400);
    }
    
    // 7. 清理輸入
    $cleanData = array(
        'name' => htmlspecialchars(strip_tags($name), ENT_QUOTES, 'UTF-8'),
        'email' => filter_var($email, FILTER_SANITIZE_EMAIL),
        'phone' => $phone,
        'company' => htmlspecialchars(strip_tags(trim(isset($data['company']) ? $data['company'] : '')), ENT_QUOTES, 'UTF-8'),
        'consultationType' => isset($data['consultationType']) ? $data['consultationType'] : '',
        'message' => htmlspecialchars(strip_tags(trim(isset($data['message']) ? $data['message'] : '')), ENT_QUOTES, 'UTF-8')
    );
    
    // 8. 準備提交到 Google Forms
    $googleFormData = array(
        'entry.162276222' => $cleanData['name'],
        'entry.1357191828' => $cleanData['email'],
        'entry.1380546653' => $cleanData['phone'],
        'entry.743695878' => $cleanData['company'],
        'entry.1863307942' => $cleanData['consultationType'],
        'entry.48027589' => $cleanData['message']
    );
    
    // 9. 使用 cURL 提交到 Google Forms
    $ch = curl_init();

    // 判斷是否為本地環境
    $isLocal = in_array($_SERVER['REMOTE_ADDR'], array('127.0.0.1', '::1')) || 
           strpos($_SERVER['HTTP_HOST'], 'localhost') !== false;

    curl_setopt_array($ch, array(
        CURLOPT_URL => GOOGLE_FORM_URL,
        CURLOPT_POST => true,
        CURLOPT_POSTFIELDS => http_build_query($googleFormData),
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_FOLLOWLOCATION => true,
        CURLOPT_TIMEOUT => 30,
        CURLOPT_SSL_VERIFYPEER => !$isLocal,  // 本地關閉，正式站開啟
        CURLOPT_SSL_VERIFYHOST => !$isLocal,  // 本地關閉，正式站開啟
        CURLOPT_USERAGENT => 'Aurobase Form Submission'
    ));
    
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $curlError = curl_error($ch);
    curl_close($ch);
    
    // 10. 檢查提交結果
    if ($curlError) {
        logSubmission('ERROR', 'cURL 錯誤', array('error' => $curlError, 'email' => $cleanData['email']));
        sendResponse(false, '提交失敗，請稍後再試', array(), 500);
    }
    
    if ($httpCode < 200 || $httpCode >= 300) {
        logSubmission('ERROR', 'Google Forms 回應異常', array('http_code' => $httpCode, 'email' => $cleanData['email']));
        sendResponse(false, '提交失敗，請稍後再試', array(), 500);
    }
    
    // 11. 記錄成功的提交
    
    logSubmission('INFO', '表單提交成功', array(
        'name' => $cleanData['name'],
        'email' => $cleanData['email'],
        'company' => $cleanData['company']
    ));
    
    // 12. 回應成功
    sendResponse(true, '感謝您的諮詢，我們將盡快與您聯繫', array('submitted_at' => date('Y-m-d H:i:s')));
    
} catch (Exception $e) {
    logSubmission('ERROR', '未預期的錯誤', array('error' => $e->getMessage(), 'trace' => $e->getTraceAsString()));
    sendResponse(false, '系統錯誤，請稍後再試', array(), 500);
}