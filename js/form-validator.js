/**
 * 表單驗證器
 * 
 * 用途: 提供前端輸入驗證和清理功能
 * 作者: Aurobase Security Team
 * 日期: 2025-11-16
 * 
 * 使用方式:
 * const errors = FormValidator.validateForm(formData);
 * if (errors.length > 0) { // 顯示錯誤 }
 */

const FormValidator = {
  /**
   * 配置
   */
  config: {
    maxNameLength: 100,
    maxCompanyLength: 200,
    maxMessageLength: 1000,
    minNameLength: 2,
  },

  /**
   * 驗證 Email 格式
   * 
   * @param {string} email - Email 地址
   * @returns {boolean} 是否有效
   */
  validateEmail(email) {
    // RFC 5322 簡化版正則表達式
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    
    if (!re.test(email)) {
      return false;
    }
    
    // 額外檢查: 長度限制
    if (email.length > 254) {
      return false;
    }
    
    // 額外檢查: 常見錯誤格式
    if (email.includes('..') || email.startsWith('.') || email.endsWith('.')) {
      return false;
    }
    
    return true;
  },

  /**
   * 驗證台灣手機號碼格式
   * 
   * 支援格式:
   * - 0912345678
   * - 0912-345-678
   * - 0912 345 678
   * 
   * @param {string} phone - 手機號碼
   * @returns {boolean} 是否有效
   */
  validatePhone(phone) {
    // 移除空白和連字號
    const cleaned = phone.replace(/[\s-]/g, '');
    
    // 台灣手機號碼: 09 開頭，共10碼
    const mobileRe = /^09\d{8}$/;
    
    // 台灣市話: 02/03/04/05/06/07/08/09 開頭
    const landlineRe = /^0[2-9]\d{7,8}$/;
    
    return mobileRe.test(cleaned) || landlineRe.test(cleaned);
  },

  /**
   * 驗證姓名
   * 
   * @param {string} name - 姓名
   * @returns {object} {valid: boolean, error: string}
   */
  validateName(name) {
    const trimmed = name.trim();
    
    if (!trimmed) {
      return { valid: false, error: '姓名不能為空' };
    }
    
    if (trimmed.length < this.config.minNameLength) {
      return { 
        valid: false, 
        error: `姓名至少需要 ${this.config.minNameLength} 個字元` 
      };
    }
    
    if (trimmed.length > this.config.maxNameLength) {
      return { 
        valid: false, 
        error: `姓名不能超過 ${this.config.maxNameLength} 個字元` 
      };
    }
    
    // 檢查是否包含特殊字元 (允許中英文、數字、空格)
    const validCharsRe = /^[\u4e00-\u9fa5a-zA-Z0-9\s]+$/;
    if (!validCharsRe.test(trimmed)) {
      return { 
        valid: false, 
        error: '姓名只能包含中英文、數字和空格' 
      };
    }
    
    return { valid: true, error: '' };
  },

  /**
   * 清理輸入 (防止 XSS)
   * 
   * @param {string} input - 原始輸入
   * @returns {string} 清理後的輸入
   */
  sanitizeInput(input) {
    if (typeof input !== 'string') {
      return '';
    }
    
    return input
      .trim()
      // 移除 HTML 標籤
      .replace(/<[^>]*>/g, '')
      // 移除特殊字元 (保留常用標點符號)
      .replace(/[<>]/g, '')
      // 正規化空白
      .replace(/\s+/g, ' ');
  },

  /**
   * 限制字串長度
   * 
   * @param {string} str - 字串
   * @param {number} maxLength - 最大長度
   * @returns {string} 截斷後的字串
   */
  truncate(str, maxLength) {
    if (!str || str.length <= maxLength) {
      return str;
    }
    return str.substring(0, maxLength);
  },

  /**
   * 完整表單驗證
   * 
   * @param {object} formData - 表單數據
   * @param {string} formData.name - 姓名
   * @param {string} formData.email - Email
   * @param {string} formData.phone - 電話
   * @param {string} formData.company - 公司名稱 (選填)
   * @param {string} formData.message - 訊息 (選填)
   * @returns {array} 錯誤訊息陣列 (空陣列表示驗證通過)
   */
  validateForm(formData) {
    const errors = [];
    
    // 1. 驗證姓名
    const nameValidation = this.validateName(formData.name);
    if (!nameValidation.valid) {
      errors.push(nameValidation.error);
    }
    
    // 2. 驗證 Email
    if (!formData.email || !formData.email.trim()) {
      errors.push('Email 不能為空');
    } else if (!this.validateEmail(formData.email.trim())) {
      errors.push('Email 格式不正確');
    }
    
    // 3. 驗證電話
    if (!formData.phone || !formData.phone.trim()) {
      errors.push('聯絡電話不能為空');
    } else if (!this.validatePhone(formData.phone)) {
      errors.push('電話號碼格式不正確 (請輸入台灣手機或市話)');
    }
    
    // 4. 驗證公司名稱 (選填，但有填就要檢查長度)
    if (formData.company && formData.company.length > this.config.maxCompanyLength) {
      errors.push(`公司名稱不能超過 ${this.config.maxCompanyLength} 個字元`);
    }
    
    // 5. 驗證訊息 (選填，但有填就要檢查長度)
    if (formData.message && formData.message.length > this.config.maxMessageLength) {
      errors.push(`需求說明不能超過 ${this.config.maxMessageLength} 個字元`);
    }
    
    return errors;
  },

  /**
   * 清理表單數據
   * 
   * @param {object} formData - 原始表單數據
   * @returns {object} 清理後的表單數據
   */
  sanitizeFormData(formData) {
    return {
      name: this.truncate(
        this.sanitizeInput(formData.name), 
        this.config.maxNameLength
      ),
      email: this.sanitizeInput(formData.email).toLowerCase(),
      phone: this.sanitizeInput(formData.phone).replace(/[\s-]/g, ''),
      company: this.truncate(
        this.sanitizeInput(formData.company || ''), 
        this.config.maxCompanyLength
      ),
      message: this.truncate(
        this.sanitizeInput(formData.message || ''), 
        this.config.maxMessageLength
      ),
      consultationType: formData.consultationType || ''
    };
  },

  /**
   * 格式化電話號碼顯示
   * 
   * @param {string} phone - 原始電話
   * @returns {string} 格式化後的電話
   */
  formatPhone(phone) {
    const cleaned = phone.replace(/[\s-]/g, '');
    
    // 手機號碼: 0912-345-678
    if (cleaned.length === 10 && cleaned.startsWith('09')) {
      return `${cleaned.slice(0, 4)}-${cleaned.slice(4, 7)}-${cleaned.slice(7)}`;
    }
    
    // 市話: 02-1234-5678
    if (cleaned.length === 9) {
      return `${cleaned.slice(0, 2)}-${cleaned.slice(2, 6)}-${cleaned.slice(6)}`;
    }
    
    return cleaned;
  },

  /**
   * 即時驗證提示
   * 
   * 用於 input 的 onblur 事件
   * 
   * @param {HTMLElement} inputElement - Input 元素
   * @param {string} validationType - 驗證類型 (email/phone/name)
   */
  showValidationFeedback(inputElement, validationType) {
    const value = inputElement.value.trim();
    let isValid = true;
    let message = '';
    
    // 移除舊的錯誤訊息
    const existingError = inputElement.parentElement.querySelector('.validation-error');
    if (existingError) {
      existingError.remove();
    }
    
    // 執行驗證
    switch (validationType) {
      case 'email':
        if (value && !this.validateEmail(value)) {
          isValid = false;
          message = 'Email 格式不正確';
        }
        break;
      
      case 'phone':
        if (value && !this.validatePhone(value)) {
          isValid = false;
          message = '電話號碼格式不正確';
        }
        break;
      
      case 'name':
        const nameResult = this.validateName(value);
        if (!nameResult.valid) {
          isValid = false;
          message = nameResult.error;
        }
        break;
    }
    
    // 顯示錯誤訊息
    if (!isValid) {
      inputElement.classList.add('is-invalid');
      const errorDiv = document.createElement('div');
      errorDiv.className = 'validation-error text-danger small mt-1';
      errorDiv.textContent = message;
      inputElement.parentElement.appendChild(errorDiv);
    } else {
      inputElement.classList.remove('is-invalid');
      inputElement.classList.add('is-valid');
    }
  }
};

/**
 * 自動綁定即時驗證
 * 
 * 在頁面載入後執行
 */
document.addEventListener('DOMContentLoaded', function() {
  // Email 驗證
  const emailInputs = document.querySelectorAll('input[type="email"], input[id*="email"]');
  emailInputs.forEach(input => {
    input.addEventListener('blur', () => {
      FormValidator.showValidationFeedback(input, 'email');
    });
  });
  
  // 電話驗證
  const phoneInputs = document.querySelectorAll('input[type="tel"], input[id*="phone"], input[id*="tel"]');
  phoneInputs.forEach(input => {
    input.addEventListener('blur', () => {
      FormValidator.showValidationFeedback(input, 'phone');
    });
  });
  
  // 姓名驗證
  const nameInputs = document.querySelectorAll('input[id*="name"], input[name*="name"]');
  nameInputs.forEach(input => {
    input.addEventListener('blur', () => {
      FormValidator.showValidationFeedback(input, 'name');
    });
  });
});

// 匯出給其他模組使用
if (typeof module !== 'undefined' && module.exports) {
  module.exports = FormValidator;
}