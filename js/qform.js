/**
 * 表單提交處理 (靜態版本)
 * 直接提交到 Google Forms，不需後端 PHP
 *
 * 依賴:
 * - FormValidator (form-validator.js)
 * - RateLimiter (rate-limiter.js)
 * - SweetAlert2
 */

// Google Forms 配置
const GOOGLE_FORM_URL = 'https://docs.google.com/forms/u/0/d/e/1FAIpQLScb94lqodiK-HmoCOGFBpIzOCJB7t9Kid_JcXydkXmez04H1w/formResponse';
const FORM_FIELDS = {
    name: 'entry.162276222',
    email: 'entry.1357191828',
    phone: 'entry.1380546653',
    company: 'entry.743695878',
    consultationType: 'entry.1863307942',
    message: 'entry.48027589'
};

// 諮詢類型變數
var f051="", f052="", f053="", f054="", f055="", f056="", f057="", f058="", f059="";

// 診斷類型 checkbox 事件監聽
let checkbox051 = document.getElementById('f05-1');
if (checkbox051) {
    checkbox051.addEventListener('change', function() {
        f051 = this.checked ? "廣告投放," : "";
    });
}

let checkbox052 = document.getElementById('f05-2');
if (checkbox052) {
    checkbox052.addEventListener('change', function() {
        f052 = this.checked ? "社群服務," : "";
    });
}

let checkbox053 = document.getElementById('f05-3');
if (checkbox053) {
    checkbox053.addEventListener('change', function() {
        f053 = this.checked ? "客服中心," : "";
    });
}

let checkbox054 = document.getElementById('f05-4');
if (checkbox054) {
    checkbox054.addEventListener('change', function() {
        f054 = this.checked ? "ACOUSTIC CXA," : "";
    });
}

let checkbox055 = document.getElementById('f05-5');
if (checkbox055) {
    checkbox055.addEventListener('change', function() {
        f055 = this.checked ? "CDP 顧客數據," : "";
    });
}

let checkbox056 = document.getElementById('f05-6');
if (checkbox056) {
    checkbox056.addEventListener('change', function() {
        f056 = this.checked ? "HCL UNICA," : "";
    });
}

let checkbox057 = document.getElementById('f05-7');
if (checkbox057) {
    checkbox057.addEventListener('change', function() {
        f057 = this.checked ? "MAGNOLIA CMS," : "";
    });
}

let checkbox058 = document.getElementById('f05-8');
if (checkbox058) {
    checkbox058.addEventListener('change', function() {
        f058 = this.checked ? "AI 智慧語伴," : "";
    });
}

let checkbox059 = document.getElementById('f05-9');
if (checkbox059) {
    checkbox059.addEventListener('change', function() {
        f059 = this.checked ? "其他" : "";
    });
}

// 提交按鈕事件
document.getElementById("submitButton").addEventListener("click", async function() {
    // 1. 檢查 Rate Limiting
    if (!RateLimiter.canSubmit()) {
        RateLimiter.showRateLimitError();
        return;
    }

    // 2. 收集表單數據
    const formData = {
        name: document.getElementById("f01").value,
        email: document.getElementById("f02").value,
        phone: document.getElementById("f03").value,
        company: document.getElementById("f04").value,
        consultationType: f051 + f052 + f053 + f054 + f055 + f056 + f057 + f058 + f059,
        message: document.getElementById("f06") ? document.getElementById("f06").value : ''
    };

    // 3. 前端驗證
    const errors = FormValidator.validateForm(formData);
    if (errors.length > 0) {
        Swal.fire({
            icon: 'error',
            title: '表單驗證失敗',
            html: errors.map(e => `• ${e}`).join('<br>'),
            confirmButtonColor: '#F96D00'
        });
        return;
    }

    // 4. 清理數據
    const cleanData = FormValidator.sanitizeFormData(formData);

    // 5. 提交到 Google Forms
    try {
        const submitBtn = document.getElementById("submitButton");
        submitBtn.disabled = true;
        submitBtn.textContent = '提交中...';

        // 組裝 Google Forms 表單數據
        const googleFormData = new URLSearchParams();
        googleFormData.append(FORM_FIELDS.name, cleanData.name);
        googleFormData.append(FORM_FIELDS.email, cleanData.email);
        googleFormData.append(FORM_FIELDS.phone, cleanData.phone);
        googleFormData.append(FORM_FIELDS.company, cleanData.company);
        googleFormData.append(FORM_FIELDS.consultationType, cleanData.consultationType);
        googleFormData.append(FORM_FIELDS.message, cleanData.message);

        // 使用 no-cors 模式直接提交到 Google Forms
        // Google Forms 不回傳可讀的 response，但提交會成功
        await fetch(GOOGLE_FORM_URL, {
            method: 'POST',
            mode: 'no-cors',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: googleFormData.toString()
        });

        // no-cors 模式下無法讀取 response，但如果沒有 throw error 就代表送出了
        // 記錄提交成功
        RateLimiter.recordSubmit();

        // 顯示成功訊息
        Swal.fire({
            icon: 'success',
            title: '提交成功',
            text: '感謝您的諮詢，我們將盡快與您聯繫',
            confirmButtonColor: '#F96D00'
        }).then(() => {
            // 關閉 modal (如果有)
            if (document.getElementById('myModal')) {
                $('#myModal').modal('hide');
            }

            // 清空表單
            document.getElementById("f01").value = '';
            document.getElementById("f02").value = '';
            document.getElementById("f03").value = '';
            document.getElementById("f04").value = '';
            if (document.getElementById("f06")) {
                document.getElementById("f06").value = '';
            }

            // 重置 checkbox
            if (checkbox051) checkbox051.checked = false;
            if (checkbox052) checkbox052.checked = false;
            if (checkbox053) checkbox053.checked = false;
            if (checkbox054) checkbox054.checked = false;
            if (checkbox055) checkbox055.checked = false;
            if (checkbox056) checkbox056.checked = false;
            if (checkbox057) checkbox057.checked = false;
            if (checkbox058) checkbox058.checked = false;
            if (checkbox059) checkbox059.checked = false;

            f051 = f052 = f053 = f054 = f055 = f056 = f057 = f058 = f059 = "";
        });
    } catch (error) {
        console.error('提交錯誤:', error);
        Swal.fire({
            icon: 'error',
            title: '網路錯誤',
            text: '無法連接到伺服器，請檢查網路連線',
            confirmButtonColor: '#F96D00'
        });
    } finally {
        // 恢復提交按鈕
        const submitBtn = document.getElementById("submitButton");
        submitBtn.disabled = false;
        submitBtn.textContent = '送出';
    }
});