/**
 * 前端 Rate Limiter
 * 
 * 用途: 限制表單提交頻率，防止濫用
 * 作者: Aurobase Security Team
 * 日期: 2025-11-16
 * 
 * 使用方式:
 * if (!RateLimiter.canSubmit()) {
 *   alert('提交過於頻繁');
 *   return;
 * }
 * RateLimiter.recordSubmit();
 */

const RateLimiter = {
  /**
   * 配置
   */
  config: {
    // LocalStorage key
    storageKey: 'form_submit_history',
    
    // 冷卻時間 (毫秒)
    cooldownTime: 60000, // 60秒
    
    // 在指定時間內的最大提交次數
    maxAttempts: 3,
    
    // 時間窗口 (毫秒)
    timeWindow: 3600000, // 1小時
    
    // 是否啟用調試模式
    debug: false
  },

  /**
   * 檢查是否可以提交
   * 
   * @returns {boolean} 是否可以提交
   */
  canSubmit() {
    const history = this.getSubmitHistory();
    const now = Date.now();
    
    // 檢查最後一次提交是否在冷卻時間內
    if (history.length > 0) {
      const lastSubmit = history[history.length - 1];
      const timeSinceLastSubmit = now - lastSubmit;
      
      if (timeSinceLastSubmit < this.config.cooldownTime) {
        this.log('冷卻時間內，無法提交');
        return false;
      }
    }
    
    // 檢查時間窗口內的提交次數
    const recentSubmits = history.filter(
      time => now - time < this.config.timeWindow
    );
    
    if (recentSubmits.length >= this.config.maxAttempts) {
      this.log('超過最大提交次數');
      return false;
    }
    
    return true;
  },

  /**
   * 記錄提交
   */
  recordSubmit() {
    const history = this.getSubmitHistory();
    const now = Date.now();
    
    // 加入新的提交時間
    history.push(now);
    
    // 只保留時間窗口內的記錄
    const filtered = history.filter(
      time => now - time < this.config.timeWindow
    );
    
    // 儲存到 localStorage
    this.saveSubmitHistory(filtered);
    
    this.log('記錄提交時間:', new Date(now));
  },

  /**
   * 取得提交歷史
   * 
   * @returns {array} 提交時間戳記陣列
   */
  getSubmitHistory() {
    try {
      const stored = localStorage.getItem(this.config.storageKey);
      return stored ? JSON.parse(stored) : [];
    } catch (e) {
      this.log('讀取歷史記錄失敗:', e);
      return [];
    }
  },

  /**
   * 儲存提交歷史
   * 
   * @param {array} history - 提交時間戳記陣列
   */
  saveSubmitHistory(history) {
    try {
      localStorage.setItem(
        this.config.storageKey, 
        JSON.stringify(history)
      );
    } catch (e) {
      this.log('儲存歷史記錄失敗:', e);
    }
  },

  /**
   * 取得剩餘冷卻時間 (秒)
   * 
   * @returns {number} 剩餘秒數，0 表示可以提交
   */
  getRemainingCooldown() {
    const history = this.getSubmitHistory();
    
    if (history.length === 0) {
      return 0;
    }
    
    const lastSubmit = history[history.length - 1];
    const timePassed = Date.now() - lastSubmit;
    const remaining = this.config.cooldownTime - timePassed;
    
    return Math.max(0, Math.ceil(remaining / 1000));
  },

  /**
   * 取得剩餘可用提交次數
   * 
   * @returns {number} 剩餘次數
   */
  getRemainingAttempts() {
    const history = this.getSubmitHistory();
    const now = Date.now();
    
    const recentSubmits = history.filter(
      time => now - time < this.config.timeWindow
    );
    
    return Math.max(0, this.config.maxAttempts - recentSubmits.length);
  },

  /**
   * 清除歷史記錄 (僅供調試使用)
   */
  clearHistory() {
    localStorage.removeItem(this.config.storageKey);
    this.log('已清除歷史記錄');
  },

  /**
   * 取得狀態資訊
   * 
   * @returns {object} 狀態物件
   */
  getStatus() {
    return {
      canSubmit: this.canSubmit(),
      remainingCooldown: this.getRemainingCooldown(),
      remainingAttempts: this.getRemainingAttempts(),
      submitHistory: this.getSubmitHistory(),
      config: this.config
    };
  },

  /**
   * 格式化剩餘時間為易讀字串
   * 
   * @returns {string} 格式化的時間字串
   */
  getFormattedCooldown() {
    const seconds = this.getRemainingCooldown();
    
    if (seconds === 0) {
      return '已就緒';
    }
    
    if (seconds < 60) {
      return `${seconds} 秒`;
    }
    
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes} 分 ${remainingSeconds} 秒`;
  },

  /**
   * 顯示錯誤訊息 (使用 SweetAlert2)
   */
  showRateLimitError() {
    const remaining = this.getRemainingCooldown();
    
    if (typeof Swal !== 'undefined') {
      if (remaining > 0) {
        Swal.fire({
          icon: 'warning',
          title: '提交過於頻繁',
          html: `請等待 <strong>${this.getFormattedCooldown()}</strong> 後再試`,
          confirmButtonText: '我知道了',
          confirmButtonColor: '#F96D00'
        });
      } else {
        Swal.fire({
          icon: 'warning',
          title: '提交次數過多',
          text: '您今天的提交次數已達上限，請明天再試',
          confirmButtonText: '我知道了',
          confirmButtonColor: '#F96D00'
        });
      }
    } else {
      // Fallback: 使用原生 alert
      if (remaining > 0) {
        alert(`提交過於頻繁，請等待 ${this.getFormattedCooldown()} 後再試`);
      } else {
        alert('您今天的提交次數已達上限，請明天再試');
      }
    }
  },

  /**
   * 更新 UI 顯示剩餘時間
   * 
   * @param {HTMLElement} element - 要更新的元素
   * @param {function} callback - 倒數結束時的回調函數
   */
  startCountdown(element, callback) {
    if (!element) return;
    
    const updateDisplay = () => {
      const remaining = this.getRemainingCooldown();
      
      if (remaining > 0) {
        element.textContent = `請等待 ${this.getFormattedCooldown()}`;
        element.style.display = 'block';
        
        // 繼續倒數
        setTimeout(updateDisplay, 1000);
      } else {
        element.style.display = 'none';
        if (callback) callback();
      }
    };
    
    updateDisplay();
  },

  /**
   * 調試日誌
   * 
   * @param {...any} args - 日誌參數
   */
  log(...args) {
    if (this.config.debug) {
      console.log('[RateLimiter]', ...args);
    }
  },

  /**
   * 初始化 (頁面載入時清理過期記錄)
   */
  init() {
    const history = this.getSubmitHistory();
    const now = Date.now();
    
    // 清理超過時間窗口的記錄
    const filtered = history.filter(
      time => now - time < this.config.timeWindow
    );
    
    if (filtered.length !== history.length) {
      this.saveSubmitHistory(filtered);
      this.log('已清理過期記錄');
    }
    
    this.log('Rate Limiter 已初始化');
    this.log('當前狀態:', this.getStatus());
  }
};

/**
 * 頁面載入時初始化
 */
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    RateLimiter.init();
  });
} else {
  RateLimiter.init();
}

/**
 * 調試工具: 在 Console 中使用
 * 
 * 使用方式:
 * window.debugRateLimiter()  // 查看狀態
 * window.clearRateLimiter()  // 清除限制
 */
if (RateLimiter.config.debug) {
  window.debugRateLimiter = () => {
    console.table(RateLimiter.getStatus());
  };
  
  window.clearRateLimiter = () => {
    RateLimiter.clearHistory();
    console.log('Rate Limiter 已重置');
  };
}

// 匯出給其他模組使用
if (typeof module !== 'undefined' && module.exports) {
  module.exports = RateLimiter;
}