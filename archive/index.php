<?php
// 引入安全 Headers 和 CSRF Token
require_once __DIR__ . '/includes/security/headers.php';
require_once __DIR__ . '/includes/security/csrf.php';
?>

<!DOCTYPE html>
<html lang="zh-hant-TW">
  <head>
    <title>奧洛｜數位整合行銷.數據分析.行銷自動化.專屬LLM.客服中心系統建置/外包服務.</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="奧洛在數位行銷浪潮下，致力于全網行銷技術的深耕于開拓，從網頁，電商建置，投放Google 關鍵字廣告，Facebook 廣告，協助粉絲團經營，分析成效">
    <meta name="keywords" content="廣告投放,廣告代操,google關鍵字,yahoo關鍵字.搜尋廣告,GDN,google聯播網,多媒體聯播網,banner廣告,yahoo原生廣告,LINE廣告,LINE today廣告,社群行銷,社群經營,FB廣告,IG廣告,LINE官方帳號,LINE@,社群聆聽,網路聲量,網站數據分析,廣告數據分析,GA,GA4,Google Analytics,網頁數據,消費者行為">   
      
    <!-- Favicon -->
	<link href="images/favicon.ico" rel="shortcut icon">
    
    <!-- ✅ LINE Seed 字體家族 (取代 Google Fonts) -->
    <!-- 預載入關鍵字體 -->
    <link rel="preload" href="WOFF2/LINESeedSans_W_Rg.woff2" as="font" type="font/woff2" crossorigin>
    <link rel="preload" href="WOFF2/LINESeedTW_OTF_Rg.woff2" as="font" type="font/woff2" crossorigin>
    <!-- 載入字體定義 -->
    <link rel="stylesheet" href="css/line-seed-font.css">

    <link rel="stylesheet" href="css/open-iconic-bootstrap.min.css">
    <link rel="stylesheet" href="css/animate.css">
    <link rel="stylesheet" href="css/owl.carousel.min.css">
    <link rel="stylesheet" href="css/owl.theme.default.min.css">
    <link rel="stylesheet" href="css/magnific-popup.css">
    <link rel="stylesheet" href="css/ionicons.min.css">
    <link rel="stylesheet" href="css/flaticon.css">
    <link rel="stylesheet" href="css/style.css">
    <!-- CSRF Token -->
    <?php echo CSRFProtection::getTokenScript(); ?>
    
    <style>
    /* 卡片式設計樣式 - 簡化版(無動畫衝突) */
    .service-card {
        background: #fff;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
    }
    
    .service-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 12px 40px rgba(249, 109, 0, 0.15);
    }
    
    .service-card-image {
        position: relative;
        width: 100%;
        padding-top: 60%; /* 16:10 比例 */
        overflow: hidden;
        background: linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%);
    }
    
    .service-card-image img {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: transform 0.3s ease;
    }
    
    .service-card:hover .service-card-image img {
        transform: scale(1.05);
    }
    
    .service-card-overlay {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(to bottom, transparent 0%, rgba(0,0,0,0.7) 100%);
        display: flex;
        align-items: flex-end;
        padding: 20px;
    }
    
    .service-card-title {
        color: #fff;
        font-size: 1.5rem;
        font-weight: 600;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .service-card-body {
        padding: 25px;
        flex-grow: 1;
        display: flex;
        flex-direction: column;
    }
    
    .service-card-description {
        color: #666;
        font-size: 0.95rem;
        line-height: 1.6;
        margin-bottom: 20px;
        flex-grow: 1;
    }
    
    .service-card-link {
        display: inline-flex;
        align-items: center;
        color: #F96D00;
        font-weight: 500;
        text-decoration: none;
        transition: all 0.3s ease;
    }
    
    .service-card-link:hover {
        color: #d55a00;
        transform: translateX(5px);
    }
    
    .service-card-link i {
        margin-left: 8px;
        transition: transform 0.3s ease;
    }
    
    .service-card-link:hover i {
        transform: translateX(5px);
    }
    
    /* 解決方案卡片 */
    .solution-card {
        background: #fff;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
        margin-bottom: 30px;
        height: 100%;
    }
    
    .solution-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 40px rgba(249, 109, 0, 0.15);
    }
    
    .solution-card-image {
        position: relative;
        width: 100%;
        padding-top: 56.25%; /* 16:9 比例 */
        overflow: hidden;
    }
    
    .solution-card-image img {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: transform 0.3s ease;
    }
    
    .solution-card:hover .solution-card-image img {
        transform: scale(1.08);
    }
    
    .solution-card-badge {
        position: absolute;
        top: 20px;
        right: 20px;
        background: rgba(249, 109, 0, 0.95);
        color: #fff;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        backdrop-filter: blur(10px);
    }
    
    .solution-card-body {
        padding: 30px;
    }
    
    .solution-card-title {
        font-size: 1.75rem;
        font-weight: 600;
        color: #333;
        margin-bottom: 15px;
    }
    
    .solution-card-subtitle {
        font-size: 1rem;
        color: #F96D00;
        font-weight: 500;
        margin-bottom: 15px;
    }
    
    .solution-card-description {
        color: #666;
        line-height: 1.8;
        margin-bottom: 20px;
    }
    
    .solution-card-features {
        list-style: none;
        padding: 0;
        margin-bottom: 25px;
    }
    
    .solution-card-features li {
        padding: 8px 0;
        color: #555;
        position: relative;
        padding-left: 25px;
    }
    
    .solution-card-features li:before {
        content: "✓";
        position: absolute;
        left: 0;
        color: #F96D00;
        font-weight: bold;
    }
    
    /* 靠左標題樣式 - 無橘色底線 */
    .section-title-left {
        font-size: 3rem;
        font-weight: 700;
        color: #333;
        margin-bottom: 0;
    }
    
    /* 響應式設計 */
    @media (max-width: 768px) {
        .service-card-title {
            font-size: 1.25rem;
        }
        
        .solution-card-title {
            font-size: 1.5rem;
        }
        
        .section-title-left {
            font-size: 2rem;
        }
        
        /* ✅ 手機版卡片間距 30px */
        .ftco-section .row .col-md-6.mb-4 {
            padding-bottom: 30px;
        }
        
        .ftco-section .row .col-md-6.mb-4:last-child {
            padding-bottom: 0;
        }
    }
    
    /* 輪播容器樣式 */
    .solution-carousel-wrapper {
        position: relative;
        padding-bottom: 60px;
    }
    
    /* Owl Carousel 自訂樣式 */
    .solution-carousel .owl-stage-outer {
        overflow: visible;
        padding: 20px 0;
    }
    
    /* 輪播導航箭頭 */
    .solution-carousel .owl-nav {
        position: absolute;
        top: 50%;
        left: 0;
        right: 0;
        transform: translateY(-50%);
        display: flex;
        justify-content: space-between;
        margin: 0 -40px;
        pointer-events: none;
    }
    
    .solution-carousel .owl-nav button {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: #fff !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
        pointer-events: auto;
        border: none;
    }
    
    .solution-carousel .owl-nav button:hover {
        background: #F96D00 !important;
        transform: scale(1.1);
    }
    
    .solution-carousel .owl-nav button span {
        font-size: 30px;
        color: #333;
        line-height: 1;
    }
    
    .solution-carousel .owl-nav button:hover span {
        color: #fff;
    }
    
    /* 輪播導航點 */
    .solution-carousel .owl-dots {
        text-align: center;
        margin-top: 30px;
    }
    
    .solution-carousel .owl-dot {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: #ddd;
        margin: 0 6px;
        transition: all 0.3s ease;
        border: none;
    }
    
    .solution-carousel .owl-dot.active {
        background: #F96D00;
        width: 30px;
        border-radius: 6px;
    }
    
    .solution-carousel .owl-dot:hover {
        background: #FF8C42;
    }
    
    /* 手機版輪播調整 */
    @media (max-width: 768px) {
        .solution-carousel .owl-nav {
            margin: 0 -20px;
        }
        
        .solution-carousel .owl-nav button {
            width: 40px;
            height: 40px;
        }
        
        .solution-carousel .owl-nav button span {
            font-size: 24px;
        }
    }
    </style>
    
	<!-- Google Tag Manager -->
        <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
        new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
        j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
        'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);    
        })(window,document,'script','dataLayer','GTM-MB9RNG8');</script>
    <!-- End Google Tag Manager -->
  </head>
  <body>
	<!-- Google Tag Manager (noscript) -->
        <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-MB9RNG8"
        height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
    <!-- End Google Tag Manager (noscript) -->
	
        <button type="button" title="填單諮詢" class="float" data-toggle="modal" data-target="#myModal">
          <image class="forms_icon" src="images/forms_icon.svg" alt="Inquiry form"></image>
        </button>
      
       <div class="modal fade" id="myModal">
       <div class="modal-dialog modal-dialog-scrollable">
       <div class="modal-content">
 
       <!-- Modal Header -->
       <div class="modal-header">
         <h5 class="modal-title">歡迎填寫諮詢表單，由專人為您量身規劃!</h5>
           <button type="button" class="close" data-dismiss="modal">&times;</button>
       </div>
 
       <!-- Modal body -->
        <form id="pop-qform" class="validate">
		    <?php include './includes/contactform.php'; ?>
        </form>      
        </div>
        </div>
        </div>

	<div id="colorlib-page">
		<a href="#" class="js-colorlib-nav-toggle colorlib-nav-toggle"><i></i></a>
		<aside id="colorlib-aside" role="complementary" class="js-fullheight">
			<?php include './includes/nav.php';?>
		</aside>
        
		<div id="colorlib-main">
            <!-- particles.js container-->
          <div id="particles-js"></div>
          
			<!-- Hero Section -->
			<section class="ftco-section ftco-no-pt ftco-no-pb mb-5 ftco-intro">
				<div class="container-fluid px-3 px-md-0">
					<div class="row justify-content-end">
						<div class="col-md-10 mt-3">
							<h1 class="mb-5 animate-charcter">Digital Advertising-SRM-Automated Marketing</h1>
							<div class="row">
								<div class="col-md-6">
									<h3>▏您最專業的科技行銷顧問</h3>
								</div>
							</div>
						</div>
					</div>
				</div>
			</section>
			
            <!-- 事業夥伴 -->
            <section class="ftco-section" id="section-clients">
	    	<div class="container-fluid px-3 px-md-0">
                <div class="row justify-content-end">
						<div class="col-md-10 mt-3">
							<div class="row">
								<div class="col-md-6">
									<h3>▏事業夥伴</h3>
								</div>
							</div>
						</div>
					</div>
	    		<div class="row d-md-flex align-items-center justify-content-end">
	    			<div class="col-md-10">
	    				<div class="row d-md-flex align-items-start">
			          <div class="col-md d-flex justify-content-center counter-wrap ftco-animate">
			            <div class="block-18">
			             <img src="images/clients/clients-1.svg" style="max-width: 200px" loading="lazy" class="img-fluid" alt="magnolia" width="200" height="100">
			            </div>
			          </div>
			          <div class="col-md d-flex justify-content-center counter-wrap ftco-animate">
			            <div class="block-18">
			              <div class="text">
			                <img src="images/clients/clients-2.svg" style="max-width: 200px" loading="lazy" class="img-fluid" alt="HCLSoftware" width="200" height="100">
			              </div>
			            </div>
			          </div>
			          <div class="col-md d-flex justify-content-center counter-wrap ftco-animate">
			            <div class="block-18">
			              <div class="text">
			                <img src="images/clients/clients-3.svg" style="max-width: 200px" loading="lazy" class="img-fluid" alt="朋昶數位科技" width="200" height="100">
			              </div>
			            </div>
			          </div>
			          <div class="col-md d-flex justify-content-center counter-wrap ftco-animate">
			            <div class="block-18">
			              <div class="text">
			                <img src="images/clients/clients-4.svg" style="max-width: 200px" loading="lazy" class="img-fluid" alt="acoustic" width="200" height="100">
			              </div>
			            </div>
			          </div>
		          </div>
	          </div>
	        </div>
	    	</div>
	        </section>

			<!-- 核心服務 - 卡片式設計 -->
			<section class="ftco-section">
				<div class="container-fluid px-3 px-md-0">
					<div class="row justify-content-end">
						<div class="col-md-10">
							<div class="mb-5">
								<h2 class="section-title-left">▏核心服務</h2>
							</div>
							
							<div class="row">
								<!-- 數位行銷卡片 -->
								<div class="col-md-6 mb-4">
									<a href="marketing.php" class="text-decoration-none">
										<div class="service-card ftco-animate">
											<div class="service-card-image">
												<img src="images/digitalmarketing_img.png" alt="數位行銷" loading="lazy" width="800" height="480">
												<div class="service-card-overlay">
													<h3 class="service-card-title">數位行銷</h3>
												</div>
											</div>
											<div class="service-card-body">
												<p class="service-card-description">
													提供全方位數位行銷解決方案，包含 Google 關鍵字廣告、Facebook 廣告投放、社群經營、SEO 優化等服務，協助企業精準觸及目標客群，提升品牌曝光與轉換率。
												</p>
												<span class="service-card-link">
													了解更多 <i class="ion-ios-arrow-forward"></i>
												</span>
											</div>
										</div>
									</a>
								</div>
								
								<!-- 客服中心卡片 -->
								<div class="col-md-6 mb-4">
									<a href="https://cti.aurocore.com/index.html" target="_blank" class="text-decoration-none">
										<div class="service-card ftco-animate">
											<div class="service-card-image">
												<img src="images/callcenter_img.png" alt="客服中心" loading="lazy" width="800" height="480">
												<div class="service-card-overlay">
													<h3 class="service-card-title">客服中心</h3>
												</div>
											</div>
											<div class="service-card-body">
												<p class="service-card-description">
													專業的客服中心系統建置與外包服務，整合 CTI 系統、CRM、智能客服機器人等功能，提供完整的客戶服務解決方案，提升客戶滿意度與服務效率。
												</p>
												<span class="service-card-link">
													了解更多 <i class="ion-ios-arrow-forward"></i>
												</span>
											</div>
										</div>
									</a>
								</div>
							</div>
						</div>
					</div>
				</div>
			</section>

			<!-- 3C Section -->
			<section class="ftco-services ftco-section">
				<div class="container-fluid px-3 px-md-0">
					<div class="row justify-content-end">
						<div class="col-md-10">
							<div class="row">
			          <div class="col-md-4 d-flex align-self-stretch ftco-animate">
			            <div class="media block-6 services d-block">
			                <img src="images/collisions_icon.webp" style="max-width: 100px" loading="lazy" class="img-fluid" alt="Collisions" width="100" height="100">
			              <div class="media-body p-2 mt-3">
			                <h3 class="heading">Collisions</h3>
			                <p>每一個使用者都是獨立個體，不同的人想法都會有所差異，我們鼓勵思想互相碰撞，藉此激發更多不同面向的想法。</p>
			              </div>
			            </div>      
			          </div>
			          <div class="col-md-4 d-flex align-self-stretch ftco-animate">
			            <div class="media block-6 services d-block">
			              <img src="images/communication_icon.webp" style="max-width: 100px" loading="lazy" class="img-fluid" alt="Communication" width="100" height="100">
			              <div class="media-body p-2 mt-3">
			                <h3 class="heading">Communication</h3>
			                <p>在專案執行之前進行有效溝通，過程中不斷調整，迅速找出最佳解決方案。</p>
			              </div>
			            </div>    
			          </div>
			          <div class="col-md-4 d-flex align-self-stretch ftco-animate">
			            <div class="media block-6 services d-block">
			              <img src="images/collaboration_icon.webp" style="max-width: 100px" loading="lazy" class="img-fluid" alt="Collaboration" width="100" height="100">
			              <div class="media-body p-2 mt-3">
			                <h3 class="heading">Collaboration</h3>
			                <p>我們擁有專業廣告操作經驗，且同時為Google等多家大廠的合作夥伴，對於電商、系統營運架構、數據分析、機器學習、演算法配置亦有豐富的經驗。</p>
			              </div>
			            </div>      
			          </div>
			        </div>
			      </div>
	        </div>
				</div>
			</section>

            <!-- 解決方案&產品 - 網格式設計 -->
            <section class="ftco-section">
				<div class="container-fluid px-3 px-md-0">
					<div class="row justify-content-end">
						<div class="col-md-10">
							<div class="mb-5">
								<h2 class="section-title-left">▏解決方案 & 產品</h2>
							</div>
							
							<div class="row">
								<!-- Acoustic CXA -->
								<div class="col-md-6 mb-4">
									<a href="solution.php#acoustic" class="text-decoration-none">
										<div class="solution-card ftco-animate">
											<div class="solution-card-image">
												<img src="images/acoustic_cxa.png" alt="Acoustic CXA" loading="lazy" width="800" height="450">
												<span class="solution-card-badge">顧客體驗</span>
											</div>
											<div class="solution-card-body">
												<h3 class="solution-card-title">Acoustic CXA</h3>
												<p class="solution-card-subtitle">顧客體驗分析平台</p>
												<p class="solution-card-description">
													深入了解客戶行為，優化使用者體驗。透過先進的分析工具,掌握客戶旅程中的每個接觸點，提升客戶滿意度與轉換率。
												</p>
												<ul class="solution-card-features">
													<li>即時行為分析與追蹤</li>
													<li>客戶旅程視覺化</li>
													<li>個人化內容推薦</li>
													<li>A/B 測試與優化</li>
												</ul>
												<span class="service-card-link">
													了解更多 <i class="ion-ios-arrow-forward"></i>
												</span>
											</div>
										</div>
									</a>
								</div>
								
								<!-- CDP 顧客數據平台 -->
								<div class="col-md-6 mb-4">
									<a href="solution.php#auro_cdp" class="text-decoration-none">
										<div class="solution-card ftco-animate">
											<div class="solution-card-image">
												<img src="images/cdp_img.png" alt="CDP 顧客數據平台" loading="lazy" width="800" height="450">
												<span class="solution-card-badge">數據整合</span>
											</div>
											<div class="solution-card-body">
												<h3 class="solution-card-title">CDP</h3>
												<p class="solution-card-subtitle">顧客數據平台</p>
												<p class="solution-card-description">
													整合多渠道顧客數據，建立完整的360度客戶視圖。運用 AI 技術進行數據分析，實現精準行銷與個人化服務。
												</p>
												<ul class="solution-card-features">
													<li>多源數據整合</li>
													<li>統一客戶檔案管理</li>
													<li>AI 智能分群與預測</li>
													<li>即時數據同步</li>
												</ul>
												<span class="service-card-link">
													了解更多 <i class="ion-ios-arrow-forward"></i>
												</span>
											</div>
										</div>
									</a>
								</div>
							</div>
							
							<div class="row">
								<!-- HCL Unica -->
								<div class="col-md-6 mb-4">
									<a href="solution.php#hcl_unica" class="text-decoration-none">
										<div class="solution-card ftco-animate">
											<div class="solution-card-image">
												<img src="images/hcl_img.png" alt="HCL Unica" loading="lazy" width="800" height="450">
												<span class="solution-card-badge">行銷自動化</span>
											</div>
											<div class="solution-card-body">
												<h3 class="solution-card-title">HCL Unica</h3>
												<p class="solution-card-subtitle">行銷自動化平台</p>
												<p class="solution-card-description">
													企業級行銷自動化解決方案，整合多渠道行銷活動，實現精準的客戶溝通與互動管理。
												</p>
												<ul class="solution-card-features">
													<li>跨渠道行銷編排</li>
													<li>智能化活動管理</li>
													<li>個人化內容投放</li>
													<li>效果追蹤與分析</li>
												</ul>
												<span class="service-card-link">
													了解更多 <i class="ion-ios-arrow-forward"></i>
												</span>
											</div>
										</div>
									</a>
								</div>
								
								<!-- Magnolia CMS -->
								<div class="col-md-6 mb-4">
									<a href="solution.php#magnolia_cms" class="text-decoration-none">
										<div class="solution-card ftco-animate">
											<div class="solution-card-image">
												<img src="images/cms_img.png" alt="Magnolia CMS" loading="lazy" width="800" height="450">
												<span class="solution-card-badge">內容管理</span>
											</div>
											<div class="solution-card-body">
												<h3 class="solution-card-title">Magnolia CMS</h3>
												<p class="solution-card-subtitle">企業內容管理系統</p>
												<p class="solution-card-description">
													強大的企業級內容管理系統，提供靈活的內容創建與管理能力，支援多語言、多網站管理。
												</p>
												<ul class="solution-card-features">
													<li>直覺式內容編輯</li>
													<li>多語言多網站支援</li>
													<li>RESTful API 整合</li>
													<li>Headless CMS 架構</li>
												</ul>
												<span class="service-card-link">
													了解更多 <i class="ion-ios-arrow-forward"></i>
												</span>
											</div>
										</div>
									</a>
								</div>
							</div>
								
								<div class="row">
									<!-- AI 智慧語伴 -->
									<div class="col-md-6 mb-4">
										<a href="ai-companion.php" class="text-decoration-none">
											<div class="solution-card ftco-animate">
												<div class="solution-card-image">
													<img src="images/aichatbot_img.png" alt="AI 智慧語伴" loading="lazy" width="800" height="450">
													<span class="solution-card-badge">智慧照護</span>
												</div>
												<div class="solution-card-body">
													<h3 class="solution-card-title">AI 智慧語伴</h3>
													<p class="solution-card-subtitle">創新研發・智慧陪伴新世代</p>
													<p class="solution-card-description">
														以 AI 語音為核心，打造智慧陪伴與健康守護。結合語音互動與智慧分析，主動陪伴長者、即時掌握健康與情緒變化，協助社工快速掌握狀況。
													</p>
													<ul class="solution-card-features">
														<li>AI 語音情感互動</li>
														<li>健康與情緒監測</li>
														<li>自動關懷報告生成</li>
														<li>用藥提醒與語音回報</li>
													</ul>
													<span class="service-card-link">
														了解更多 <i class="ion-ios-arrow-forward"></i>
													</span>
												</div>
											</div>
										</a>
									</div>
								</div>
						</div>
					</div>
				</div>
		     </section>
        
             <footer id="footer-sec" class="ftco-footer ftco-bg-dark ftco-section">
		        <?php include './includes/footer_simple.php';?>
	         </footer>	
	         </div><!-- END COLORLIB-MAIN -->
	         </div><!-- END COLORLIB-PAGE -->
      
  <!-- loader -->
  <div id="ftco-loader" class="show fullscreen"><svg class="circular" width="48px" height="48px"><circle class="path-bg" cx="24" cy="24" r="22" fill="none" stroke-width="4" stroke="#eeeeee"/><circle class="path" cx="24" cy="24" r="22" fill="none" stroke-width="4" stroke-miterlimit="10" stroke="#F96D00"/></svg></div>
     
  <!-- ✅ Phase 3 優化: 移除未使用的 JS 庫 (節省 70KB) -->
  <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
  <script src="js/jquery.min.js"></script>
  <script src="js/popper.min.js"></script>
  <script src="js/bootstrap.min.js"></script>
  <script src="js/jquery.waypoints.min.js"></script>
  <script src="js/jquery.magnific-popup.min.js"></script>
  <script src="js/aos.js"></script>
  <script src="js/external-link-warning.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
  <script src="js/main_optimized.js"></script>
  <script src="js/form-validator.js"></script>
  <script src="js/rate-limiter.js"></script>
  <script src="js/qform.js"></script>
  
  </body>
</html>
