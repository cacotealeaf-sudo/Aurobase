/* 留 Email 換資料（.lm-form）：只要一個 Email，送到與諮詢表單同一份 Google 表單，送出後顯示下載連結。
 * 依賴 js/qform.js 的 GOOGLE_FORM_URL、FORM_FIELDS（有諮詢彈窗的頁面都會載入）與 js/form-validator.js。
 * 業務在試算表看到的：Email、諮詢類型（data-lead-type）、需求說明「（索取：<資料名稱>）（來源頁面：…）」。
 * GA：送出成功推 generate_lead（lead_type=資料代號），點下載連結由 site-events.js 記 file_download。 */
(function () {
  var forms = document.querySelectorAll('form.lm-form');
  if (!forms.length) return;

  function valid(email) {
    if (window.FormValidator) return FormValidator.validateEmail(email);
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }

  Array.prototype.forEach.call(forms, function (form) {
    var input = form.querySelector('input[type="email"]');
    var button = form.querySelector('button[type="submit"]');
    var msg = form.querySelector('.lm-msg');
    var sent = false;

    form.addEventListener('submit', function (event) {
      event.preventDefault();
      if (sent) return;
      var email = input.value.trim();
      if (!valid(email)) {
        msg.textContent = 'Email 格式不正確，例如 name@company.com';
        form.classList.add('is-error');
        input.setAttribute('aria-invalid', 'true');
        input.focus();
        return;
      }
      form.classList.remove('is-error');
      input.removeAttribute('aria-invalid');
      if (typeof GOOGLE_FORM_URL === 'undefined') { msg.textContent = '目前無法送出，請改寫信到 ad@aurocore.com'; return; }

      var source = (document.querySelector('meta[name="inquiry-source"]') || {}).content || document.title.split('｜')[0].trim();
      var data = new URLSearchParams();
      data.append(FORM_FIELDS.email, email.toLowerCase());
      data.append(FORM_FIELDS.consultationType, form.dataset.leadType || '');
      data.append(FORM_FIELDS.message, '（索取：' + form.dataset.leadName + '）（來源頁面：' + source + '）');

      button.disabled = true;
      button.textContent = '送出中…';
      fetch(GOOGLE_FORM_URL, {
        method: 'POST', mode: 'no-cors',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: data.toString()
      }).then(function () {
        sent = true;
        if (window.auroTrack) window.auroTrack('generate_lead', { consultation_type: form.dataset.leadType || '', lead_type: form.dataset.leadId });
        form.classList.add('is-done');
        input.disabled = true;
        button.textContent = '已送出';
        msg.innerHTML = '';
        var a = document.createElement('a');
        a.href = form.dataset.leadFile;
        a.textContent = '下載' + form.dataset.leadName + '（PDF）';
        a.setAttribute('download', '');
        msg.appendChild(document.createTextNode('謝謝，'));
        msg.appendChild(a);
        a.focus();
      }).catch(function () {
        button.disabled = false;
        button.textContent = form.dataset.leadButton;
        msg.textContent = '網路連線失敗，請稍後再試，或寫信到 ad@aurocore.com';
      });
    });
  });
})();
