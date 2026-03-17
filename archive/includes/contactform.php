<style>
/* 重置可能的樣式衝突 */
.compact-form * {
    box-sizing: border-box;
}

.compact-form .form-row {
    display: flex;
    gap: 15px;
    margin-bottom: 12px;
}

.compact-form .form-row fieldset {
    flex: 1;
    margin: 0;
}

.compact-form fieldset {
    border: none;
    padding: 0;
    margin-bottom: 12px;
}

.compact-form label {
    display: block;
    margin-bottom: 5px;
    font-weight: 500;
    font-size: 0.9rem;
}

.compact-form input[type="text"],
.compact-form input[type="email"],
.compact-form input[type="tel"] {
    width: 100%;
    padding: 8px 12px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 0.9rem;
}

.compact-form .required {
    color: #f96d00;
}

/* 諮詢類型 - 緊湊的三欄 inline checkbox */
.compact-form .checkbox-inline-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px 15px;
    margin-top: 8px;
}

/* 修正 checkbox 樣式 - 重點區域 */
.compact-form .form-check {
    display: flex;
    align-items: center;
    margin: 0;
    padding: 4px 0;
    position: relative;
}

.compact-form .form-check-input {
    /* 重要：確保 checkbox 不被遮擋 */
    margin: 0 12px 0 0 !important;
    padding: 0 !important;
    cursor: pointer;
    flex-shrink: 0;
    width: 16px !important;
    height: 16px !important;
    position: relative;
    opacity: 1 !important;
    appearance: auto;
    -webkit-appearance: checkbox;
}

.compact-form .form-check label {
    /* 確保文字不會覆蓋到 checkbox */
    margin: 0;
    padding: 0;
    font-weight: 400;
    font-size: 0.85rem;
    cursor: pointer;
    white-space: nowrap;
    line-height: 1.5;
    user-select: none;
}

.compact-form textarea.form-control {
    width: 100%;
    min-height: 70px;
    padding: 8px 12px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 0.9rem;
    resize: vertical;
}

/* 提交按鈕樣式 */
.compact-form .btn-form {
    width: 100%;
    padding: 12px 20px;
    background: #6B9BB9; 
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 1rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
    margin-top: 15px;
}

.compact-form .btn-form:hover {
    background: #578399; 
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(90, 108, 125, 0.3);
}

.compact-form .btn-form:active {
    transform: translateY(0);
}

.compact-form .btn-form:disabled {
    background: #ccc;
    cursor: not-allowed;
    transform: none;
}

/* 響應式設計 */
@media (max-width: 768px) {
    .compact-form .form-row {
        flex-direction: column;
        gap: 12px;
    }
    
    .compact-form .checkbox-inline-grid {
        grid-template-columns: repeat(2, 1fr);
        gap: 8px 12px;
    }
}

@media (max-width: 480px) {
    .compact-form .checkbox-inline-grid {
        grid-template-columns: 1fr;
    }
}
</style>

<div class="compact-form">
    <!-- 第一列：姓名 + Email -->
    <div class="form-row">
        <fieldset>
            <label for="f01">您的姓名 <span class="required">*</span></label>
            <input 
                type="text" 
                name="entry.162276222" 
                id="f01" 
                placeholder="請輸入姓名" 
                required 
            />
        </fieldset>
        
        <fieldset>
            <label for="f02">Email <span class="required">*</span></label>
            <input 
                type="email" 
                name="entry.1357191828" 
                id="f02" 
                placeholder="example@gmail.com" 
                required 
            />
        </fieldset>
    </div>

    <!-- 第二列：電話 + 公司名稱 -->
    <div class="form-row">
        <fieldset>
            <label for="f03">聯絡電話 <span class="required">*</span></label>
            <input 
                type="tel" 
                name="entry.1380546653" 
                id="f03" 
                placeholder="0911-XXX-XXX" 
                required 
            />
        </fieldset>
        
        <fieldset>
            <label for="f04">公司名稱</label>
            <input 
                type="text" 
                name="entry.743695878" 
                id="f04" 
                placeholder="選填" 
            />
        </fieldset>
    </div>

    <!-- 諮詢類型 - 三欄緊湊排列 -->
    <fieldset>
        <label>諮詢類型</label>
        <div class="checkbox-inline-grid">
            <div class="form-check">
                <input 
                    class="form-check-input" 
                    type="checkbox"
                    name="entry.1863307942"
                    value="廣告投放" 
                    id="f05-1" 
                /> 
                <label for="f05-1">廣告投放</label>
            </div>
            
            <div class="form-check">
                <input 
                    class="form-check-input" 
                    type="checkbox" 
                    name="entry.1863307942"
                    value="社群服務" 
                    id="f05-2" 
                /> 
                <label for="f05-2">社群服務</label>
            </div>
            
            <div class="form-check">
                <input 
                    class="form-check-input" 
                    type="checkbox" 
                    name="entry.1863307942"
                    value="ACOUSTIC CXA" 
                    id="f05-3" 
                /> 
                <label for="f05-3">ACOUSTIC CXA</label>
            </div>
            
            <div class="form-check">
                <input 
                    class="form-check-input" 
                    type="checkbox" 
                    name="entry.1863307942"
                    value="CDP 顧客數據" 
                    id="f05-4" 
                /> 
                <label for="f05-4">CDP 顧客數據</label>
            </div>
            
            <div class="form-check">
                <input 
                    class="form-check-input" 
                    type="checkbox" 
                    name="entry.1863307942"
                    value="HCL UNICA" 
                    id="f05-5" 
                /> 
                <label for="f05-5">HCL UNICA</label>
            </div>
            
            <div class="form-check">
                <input 
                    class="form-check-input" 
                    type="checkbox" 
                    name="entry.1863307942"
                    value="MAGNOLIA CMS" 
                    id="f05-6" 
                /> 
                <label for="f05-6">MAGNOLIA CMS</label>
            </div>
            
            <div class="form-check">
                <input 
                    class="form-check-input" 
                    type="checkbox" 
                    name="entry.1863307942"
                    value="AI 智慧語伴" 
                    id="f05-7" 
                /> 
                <label for="f05-7">AI 智慧語伴</label>
            </div>
            
            <div class="form-check">
                <input 
                    class="form-check-input" 
                    type="checkbox" 
                    name="entry.1863307942"
                    value="其他" 
                    id="f05-8" 
                /> 
                <label for="f05-8">其他</label>
            </div>
        </div>
    </fieldset>

    <!-- 需求說明 -->
    <fieldset>
        <label for="f06">需求說明</label>
        <textarea 
            id="f06" 
            class="form-control" 
            name="entry.48027589" 
            placeholder="請簡述您的需求（選填）"
        ></textarea>
    </fieldset>

    <button id="submitButton" class="btn-form" type="button">送出</button>
</div>