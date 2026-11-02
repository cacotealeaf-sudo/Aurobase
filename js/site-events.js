/* 網站轉換事件：推到 GTM 的 dataLayer，由 GTM 轉成 GA4 事件。
 * 本檔只負責「發生了什麼」；要在 GA4 看到，GTM 需為下列事件名稱各設一個「自訂事件」觸發條件與 GA4 事件代碼。
 *   inquiry_open     打開諮詢表單（form_location：哪一頁）           ← js/inquiry-modal.js 發送
 *   generate_lead    送出諮詢表單（consultation_type：勾選的類型）   ← js/qform.js 發送
 *   search           站內搜尋（search_term、result_count；0 筆就是找不到的需求） ← js/site-search.js 發送
 *   contact_click    點電話或 Email（method：phone / email）
 *   outbound_click   點到其他網站（link_url）
 *   file_download    下載 PDF 等檔案（file_name）
 * 不送姓名、Email、電話等表單內容。 */
(function () {
  window.dataLayer = window.dataLayer || [];
  window.auroTrack = function (event, params) {
    var o = { event: event, page_title: document.title.split('｜')[0].trim() };
    for (var k in params) if (Object.prototype.hasOwnProperty.call(params, k)) o[k] = params[k];
    window.dataLayer.push(o);
  };

  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href]');
    if (!a) return;
    var href = a.getAttribute('href') || '';
    if (/^tel:/i.test(href)) return window.auroTrack('contact_click', { method: 'phone' });
    if (/^mailto:/i.test(href)) return window.auroTrack('contact_click', { method: 'email' });
    if (/\.(pdf|docx?|xlsx?|pptx?|zip)(\?|#|$)/i.test(href)) {
      return window.auroTrack('file_download', { file_name: href.split('/').pop().split(/[?#]/)[0] });
    }
    if (a.host && a.host !== location.host && /^https?:$/.test(a.protocol)) {
      window.auroTrack('outbound_click', { link_url: a.href });
    }
  }, true);
})();
