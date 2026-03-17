/**
 * 外部連結跳轉提醒 - 完整版
 */

(function($) {
  'use strict';

  // 配置
  const config = {
    currentDomain: window.location.hostname,
    // 信任的域名 (不顯示警告)
    trustedDomains: [
      'facebook.com',
      'www.facebook.com'
      // cti.aurocore.com 已移除,會顯示警告
    ],
    // 是否開新視窗
    openInNewTab: true
  };

  // 檢查是否為外部連結
  function isExternalLink(href) {
    if (!href || 
        href.startsWith('#') || 
        href.startsWith('javascript:') || 
        href.startsWith('mailto:') || 
        href.startsWith('tel:') ||
        !href.startsWith('http')) {
      return false;
    }

    try {
      const url = new URL(href);
      const domain = url.hostname;
      
      // 檢查是否為當前域名
      if (domain === config.currentDomain) {
        return false;
      }
      
      // 檢查是否為信任域名
      if (config.trustedDomains.some(trusted => domain.includes(trusted))) {
        return false;
      }
      
      return true;
    } catch (e) {
      return false;
    }
  }

  // ✅ 顯示警告彈窗 (針對 CTI 顯示不同訊息)
  function showWarning(url, linkText) {
    // 檢查是否為 CTI 網站
    const isCTI = url.includes('cti.aurocore.com');
    
    return Swal.fire({
      title: isCTI ? '前往客服中心' : '即將離開本站',
      html: isCTI ? `
        <div style="text-align: left;">
          <p>您即將前往奧洛客服中心系統：</p>
          <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 15px 0;">
            <strong style="color: #F96D00;">${linkText}</strong><br>
            <small class="text-muted">${url}</small>
          </div>
          <p class="text-muted small mb-0">
            <i class="icon-info"></i> 此為奧洛旗下系統,安全可信賴
          </p>
        </div>
      ` : `
        <div style="text-align: left;">
          <p>您即將前往外部網站：</p>
          <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 15px 0;">
            <strong style="color: #F96D00;">${linkText}</strong><br>
            <small class="text-muted">${url}</small>
          </div>
          <p class="text-muted small mb-0">
            <i class="icon-info"></i> 請確認您信任此網站後再繼續
          </p>
        </div>
      `,
      icon: isCTI ? 'question' : 'info',
      iconColor: '#F96D00',
      showCancelButton: true,
      confirmButtonColor: '#F96D00',
      cancelButtonColor: '#6c757d',
      confirmButtonText: isCTI ? '前往客服中心' : '確定前往',
      cancelButtonText: '取消',
      reverseButtons: true
    });
  }

  // 初始化
  function init() {
    $('a[href]').each(function() {
      const $link = $(this);
      const href = $link.attr('href');
      
      // 跳過有 data-no-warning 屬性的連結
      if ($link.data('no-warning')) {
        return;
      }

      // 不跳過 target="_blank" 的連結
      const hasTargetBlank = $link.attr('target') === '_blank';

      // 檢查是否為外部連結
      if (isExternalLink(href)) {
      // 標記外部連結
      $link.addClass('external-link');
      
      // 如果原本有 target="_blank",移除它
      if (hasTargetBlank) {
        $link.removeAttr('target');
      }
        
        // 綁定點擊事件
        $link.on('click', function(e) {
          e.preventDefault();
          
          const targetUrl = $(this).attr('href');
          const linkText = $(this).text().trim() || '外部網站';

          showWarning(targetUrl, linkText).then((result) => {
            if (result.isConfirmed) {
              if (config.openInNewTab) {
                window.open(targetUrl, '_blank');
              } else {
                window.location.href = targetUrl;
              }
            }
          });
        });
      }
    });
  }

  // DOM 載入完成後執行
  $(document).ready(function() {
    init();
  });

})(jQuery);