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

// 諮詢類型：直接讀取被勾選 checkbox 的 value。
// 各頁的選項與順序不同（首頁 modal、contact.html、nexus.html…），
// 不能用 id 對應寫死的標籤，否則送出的類型會錯位。
const CONSULTATION_CHECKBOXES = 'input[name="' + FORM_FIELDS.consultationType + '"]';

function consultationScope() {
    return document.getElementById("submitButton").closest('form') || document;
}

function checkedConsultationTypes() {
    return Array.from(consultationScope().querySelectorAll(CONSULTATION_CHECKBOXES + ':checked'))
        .map(function(box) { return box.value; })
        .join(',');
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
        consultationType: checkedConsultationTypes(),
        message: document.getElementById("f06") ? document.getElementById("f06").value : ''
    };

    // 3. 前端驗證
    const errors = FormValidator.validateForm(formData);
    if (errors.length > 0) {
        Swal.fire({
            icon: 'error',
            title: '表單驗證失敗',
            html: errors.map(e => `• ${e}`).join('<br>'),
            confirmButtonColor: '#E63109'
        });
        return;
    }

    // 4. 清理數據
    const cleanData = FormValidator.sanitizeFormData(formData);
    // 附上來源頁面，讓業務知道客戶從哪一個產品或方案頁提出需求
    const source = document.title.split('｜')[0].trim();
    cleanData.message = (cleanData.message ? cleanData.message + '\n\n' : '') + '（來源頁面：' + source + '）';

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
            confirmButtonColor: '#E63109'
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
            consultationScope().querySelectorAll(CONSULTATION_CHECKBOXES).forEach(function(box) {
                box.checked = false;
            });
        });
    } catch (error) {
        console.error('提交錯誤:', error);
        Swal.fire({
            icon: 'error',
            title: '網路錯誤',
            text: '無法連接到伺服器，請檢查網路連線',
            confirmButtonColor: '#E63109'
        });
    } finally {
        // 恢復提交按鈕
        const submitBtn = document.getElementById("submitButton");
        submitBtn.disabled = false;
        submitBtn.textContent = '送出';
    }
});