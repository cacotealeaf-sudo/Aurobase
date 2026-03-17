<style>
/* 提交按鈕樣式 - 與 contactform.php 一致 */
.btn-form {
    width: 100%;
    padding: 12px 20px;
    background: #6B9BB9; /* 溫和天藍灰 */
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 1rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
    margin-top: 15px;
}

.btn-form:hover {
    background: #578399; /* 深一點的天藍灰 */
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(107, 155, 185, 0.3);
}

.btn-form:active {
    transform: translateY(0);
}

.btn-form:disabled {
    background: #ccc;
    cursor: not-allowed;
    transform: none;
}
</style>

<a class="color-orange">免費諮詢</a>
<h1 class="mb-4 font-weight-bold">創造事業的下一個高峰！</h1>
<p class="mb-4 pb-2">立即填寫諮詢表單，將有專人與您聯繫。</p>
<div class="form-group">
<input id="f01"
    type="text" 
    name="entry.1357191828" 
    class="form-control border-1" placeholder="您的姓名 (必填)" style="height: 55px;" 
    required
    />
</div>
<div class="form-group">
<input id="f02"
    type="text" 
    name="entry.162276222"
    class="form-control border-1" placeholder="您的Email（必填）" style="height: 55px;" 
    required
    />
</div>
<div class="form-group">
<input id="f03"
    type="text" 
    name="entry.1380546653" 
    class="form-control border-1" placeholder="聯絡電話 (必填)" style="height: 55px;"
    required
    />
</div>
<div class="form-group">
<input id="f04"
    type="text" 
    name="entry.743695878" 
    class="form-control border-1" placeholder="公司名稱" 
    style="height: 55px;" 
    />
</div>
<label id="f05" class="mb-4">諮詢類型</label>
<div class="col-mb-12">
<div class="form-check">
<input id="f05-1"
        class="form-check-input" type="checkbox" name="entry.1863307942" value="廣告投放"  style="height: 18px; width: 18px;" />
<label class="form-check-label" for="f05-1">
    廣告投放
</label>
</div>
<div class="form-check">
<input id="f05-2"
        class="form-check-input" type="checkbox" name="entry.1863307942" value="社群服務"  style="height: 18px; width: 18px;" />
<label class="form-check-label" for="f05-2">
    社群服務
</label>
</div>
<div class="form-check">
<input id="f05-3"
        class="form-check-input" type="checkbox" name="entry.1863307942" value="ACOUSTIC CXA" style="height: 18px; width: 18px;" />
<label class="form-check-label" for="f05-3">
    ACOUSTIC CXA
</label>
</div>
<div class="form-check">
<input id="f05-4"
        class="form-check-input" type="checkbox" name="entry.1863307942" 
        value="CDP 顧客數據" 
        
        style="height: 18px; width: 18px;" />
<label class="form-check-label" for="f05-4">
    CDP 顧客數據
</label>
</div>
<div class="form-check">
<input id="f05-5"
        class="form-check-input" type="checkbox" name="entry.1863307942" 
        value="HCL UNICA" 
        style="height: 18px; width: 18px;" />
<label class="form-check-label" for="f05-5">
    HCL UNICA
</label>
</div>
<div class="form-check">
<input id="f05-6"
        class="form-check-input" type="checkbox" name="entry.1863307942" value="MAGNOLIA CMS" 
        style="height: 18px; width: 18px;" />
<label class="form-check-label" for="f05-6">
    MAGNOLIA CMS
</label>
</div>
<div class="form-check">
<input id="f05-7"
        class="form-check-input" type="checkbox" name="entry.1863307942" value="AI 智慧語伴" 
        style="height: 18px; width: 18px;" />
<label class="form-check-label" for="f05-7">
    AI 智慧語伴
</label>
</div>
<div class="form-check">
<input id="f05-8"
        class="form-check-input" type="checkbox" name="entry.1863307942" value="其他" 
        style="height: 18px; width: 18px;" />
<label class="form-check-label" for="f05-8">
    其他
</label>
</div>
</div>
<div class="form-group">
<textarea id="f06" class="form-control border-1" cols="30" rows="5" name="entry.48027589" placeholder="需求說明"></textarea>
</div>
<div class="form-group">
<button id="submitButton" class="btn-form" type="button">送出</button>
</div>