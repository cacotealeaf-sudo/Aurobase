/* Two-step inquiry modal (#myModal.qf-modal): step 1 needs, step 2 contact details.
 * This file only drives the steps and inline validation. The actual submission stays in
 * js/qform.js, which this script blocks (capture listener) until the fields are valid.
 * Depends on FormValidator (js/form-validator.js) and jQuery/Bootstrap for modal events. */
(function () {
  var modal = document.getElementById('myModal');
  if (!modal || !modal.classList.contains('qf-modal')) return;

  var form = modal.querySelector('form');
  var body = modal.querySelector('.modal-body');
  var steps = modal.querySelectorAll('[data-qf-step]');
  var dots = modal.querySelectorAll('[data-qf-dot]');
  var backBtn = modal.querySelector('[data-qf-back]');
  var nextBtn = modal.querySelector('[data-qf-next]');
  var submitBtn = document.getElementById('submitButton');
  var message = document.getElementById('f06');
  var counter = modal.querySelector('[data-qf-count]');
  var current = 1;

  // Required step-2 fields → error text ('' when valid). Rules mirror FormValidator.validateForm.
  var RULES = {
    f01: function (v) { var r = FormValidator.validateName(v); return r.valid ? '' : r.error; },
    f02: function (v) {
      if (!v.trim()) return '請輸入 Email';
      return FormValidator.validateEmail(v.trim()) ? '' : 'Email 格式不正確，例如 name@company.com';
    },
    f03: function (v) {
      if (!v.trim()) return '請輸入聯絡電話';
      return FormValidator.validatePhone(v) ? '' : '請輸入台灣手機或市話，例如 0912-345-678';
    }
  };

  function checkField(input) {
    var error = RULES[input.id](input.value);
    var field = input.closest('.qf-field');
    field.classList.toggle('is-error', !!error);
    field.classList.toggle('is-valid', !error);
    input.setAttribute('aria-invalid', error ? 'true' : 'false');
    document.getElementById(input.id + '-msg').textContent = error;
    return !error;
  }

  function showStep(n) {
    current = n;
    steps.forEach(function (step) { step.hidden = Number(step.dataset.qfStep) !== n; });
    dots.forEach(function (dot) {
      var i = Number(dot.dataset.qfDot);
      dot.classList.toggle('is-active', i === n);
      dot.classList.toggle('is-done', i < n);
      if (i === n) dot.setAttribute('aria-current', 'step'); else dot.removeAttribute('aria-current');
    });
    backBtn.hidden = n === 1;
    nextBtn.hidden = n !== 1;
    submitBtn.hidden = n === 1;
    body.scrollTop = 0;
  }

  function focusStep() {
    var first = modal.querySelector('[data-qf-step="' + current + '"] input, [data-qf-step="' + current + '"] textarea');
    if (first) first.focus({ preventScroll: true });
  }

  function resetForm() {
    Object.keys(RULES).forEach(function (id) {
      var input = document.getElementById(id);
      input.closest('.qf-field').classList.remove('is-error', 'is-valid');
      input.removeAttribute('aria-invalid');
      document.getElementById(id + '-msg').textContent = '';
    });
    updateCount();
    showStep(1);
  }

  function updateCount() {
    counter.textContent = message.value.length + ' / ' + message.maxLength;
  }

  nextBtn.addEventListener('click', function () { showStep(2); focusStep(); });
  backBtn.addEventListener('click', function () { showStep(1); focusStep(); });
  message.addEventListener('input', updateCount);

  // Validate on blur, then live once a field has shown an error.
  Object.keys(RULES).forEach(function (id) {
    var input = document.getElementById(id);
    input.addEventListener('blur', function () { if (input.value) checkField(input); });
    input.addEventListener('input', function () {
      if (input.closest('.qf-field').classList.contains('is-error')) checkField(input);
    });
  });

  // Runs before qform.js's click handler (capture phase on the target fires first).
  submitBtn.addEventListener('click', function (event) {
    var invalid = Object.keys(RULES)
      .map(function (id) { return document.getElementById(id); })
      .filter(function (input) { return !checkField(input); });
    if (!invalid.length) return;
    event.stopImmediatePropagation();
    invalid[0].focus();
  }, true);

  // Enter in a step-2 text field sends the form (textarea keeps Enter for new lines).
  form.addEventListener('keydown', function (event) {
    if (event.key !== 'Enter' || event.isComposing || event.target.tagName !== 'INPUT') return;
    if (event.target.type === 'checkbox') return;
    event.preventDefault();
    if (current === 2) submitBtn.click();
  });
  form.addEventListener('submit', function (event) { event.preventDefault(); });

  $(modal)
    .on('shown.bs.modal', focusStep)
    .on('hidden.bs.modal', function () {
      // qform.js clears the values after a successful send; start the next visit at step 1.
      if (!document.getElementById('f01').value) resetForm();
    });

  updateCount();
})();
