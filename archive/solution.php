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
    
	<!-- ✅ LINE Seed 字體家族 -->
    <link rel="preload" href="WOFF2/LINESeedSans_W_Rg.woff2" as="font" type="font/woff2" crossorigin>
    <link rel="preload" href="WOFF2/LINESeedTW_OTF_Rg.woff2" as="font" type="font/woff2" crossorigin>
    <link rel="stylesheet" href="css/line-seed-font.css">

    <link rel="stylesheet" href="css/open-iconic-bootstrap.min.css">
    <link rel="stylesheet" href="css/animate.css">
    
    <link rel="stylesheet" href="css/owl.carousel.min.css">
    <link rel="stylesheet" href="css/owl.theme.default.min.css">
    <link rel="stylesheet" href="css/magnific-popup.css">

    <!--<link rel="stylesheet" href="css/aos.css">-->

    <link rel="stylesheet" href="css/ionicons.min.css">

    <!--<link rel="stylesheet" href="css/bootstrap-datepicker.css">-->
    <!--<link rel="stylesheet" href="css/jquery.timepicker.css">-->

    
    <link rel="stylesheet" href="css/flaticon.css">
    <link rel="stylesheet" href="css/style.css">
	<!-- CSRF Token -->
    <?php echo CSRFProtection::getTokenScript(); ?>

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
	    <form   id="pop-qform" class="validate">
           <?php include './includes/contactform.php'; ?>
        </form>     
        </div>
        </div>
        </div>
      

	<div id="colorlib-page">
		<a href="#" class="js-colorlib-nav-toggle colorlib-nav-toggle"><i></i></a>
		<aside id="colorlib-aside" role="complementary" class="js-fullheight">
		<?php include './includes/nav.php'; ?>
		</aside> <!-- END COLORLIB-ASIDE -->
        
        <!-- Anchor manu start --> 
        <div class="btn fixed-top text-right">
          <a href="#acoustic" class="btn btn-primary btn-sm">Acoustic</a>
          <a href="#auro_cdp" class="btn btn-primary btn-sm">CDP</a>
          <a href="#hcl_unica" class="btn btn-primary btn-sm">HCL UNICA</a>
          <a href="#magnolia_cms" class="btn btn-primary btn-sm">Magnolia CMS</a>    
        </div>
        <!-- END Anchor manu -->
        
        <div id="colorlib-main">
            <!-- particles.js container
            <div id="particles-js"></div> -->
			<section class="ftco-section ftco-bread ftco-extend-mb">
				<div class="container-fluid px-3 px-md-0">
					<div class="row no-gutters slider-text justify-content-end align-items-center">
	          <div class="col-md-10 ftco-animate">
	            <p class="breadcrumbs"><span class="mr-2"><a href="index.php">首頁</a></span> <span>解決方案＆產品</span></p><br>
                <h2 style="color:#d9e0e7;">解決方案＆產品</h2>
	          </div>
	        </div>
				</div>
			</section>
            <section id="acoustic" class="ftco-section">
            				
            					<div class="row  justify-content-end">
                                    <div class="col-md-10">
            						<div class="col-md-12 project ftco-animate">
            							<div class="img img-fluid-d" style="height: 50vw; background-image: url(images/cxa01.webp); background-size:cover; background-position: center center;" alt="顧客體驗分析：業界唯一開創『可視化顧客旅程』透過顧客數位行為軌跡，全面掌握顧客線上操作行為與瀏覽習慣，洞察顧客操作困境，有效挽回流失顧客。可視化影像回放，了解使用者實際操作瀏覽狀況，左側可看見使用者所有動作（如點擊、填寫資料等）。從Session Replay中，也可看見該頁程式資訊，方便行銷人員與IT溝通。">    
            							<div class="text text-left">
            								<h2>Acoustic</h2>
            							</div>
            							</div>
                                        <div class="img img-fluid-d ftco-animate" style="height: 50vw; background-image: url(images/cxa02.webp); background-size:cover; background-position: center center;" alt="表格分析:可了解使用者於網頁上欄位填寫的跳離比率、花費多久時間填寫、重複修改次數等。熱點圖：了解客戶點擊熱區，哪些是使用者最常點擊的地方。關注圖：觀察使用者關注熱區，可將重點資訊調整挪移。行為分析：可進行使用者各裝置移轉使用分析。">
            							</div>
                                        <div class="img img-fluid-d ftco-animate" style="height: 50vw; background-image: url(images/cxa03.webp); background-size:cover; background-position: center center;" alt="警示通知：系統可發出警示訊息提醒監測者，預設之觀測事件（可客製化）是否發生異常。裝置分析：可知道使用者的裝置與品牌，並加以歸納分析。產品內容優勢包含：影像回放、操作分析、行為認知、用戶旅程分析與數據集成。">
            							</div>
                                    
                                        <img src="images/cxa01-m.webp" class="img-fluid-m ftco-animate" alt="顧客體驗分析：業界唯一開創『可視化顧客旅程』透過顧客數位行為軌跡，全面掌握顧客線上操作行為與瀏覽習慣，洞察顧客操作困境，有效挽回流失顧客。可視化影像回放，了解使用者實際操作瀏覽狀況，左側可看見使用者所有動作（如點擊、填寫資料等）。從Session Replay中，也可看見該頁程式資訊，方便行銷人員與IT溝通。">
                                        <img src="images/cxa02-m.webp" class="img-fluid-m ftco-animate" alt="表格分析:可了解使用者於網頁上欄位填寫的跳離比率、花費多久時間填寫、重複修改次數等。熱點圖：了解客戶點擊熱區，哪些是使用者最常點擊的地方。">
                                        <img src="images/cxa03-m.webp" class="img-fluid-m ftco-animate" alt="關注圖：觀察使用者關注熱區，可將重點資訊調整挪移。行為分析：可進行使用者各裝置移轉使用分析。">
                                        <img src="images/cxa04-m.webp" class="img-fluid-m ftco-animate" alt="警示通知：系統可發出警示訊息提醒監測者，預設之觀測事件（可客製化）是否發生異常。裝置分析：可知道使用者的裝置與品牌，並加以歸納分析。">
                                        <img src="images/cxa05-m.webp" class="img-fluid-m ftco-animate" alt="產品內容優勢包含：影像回放、操作分析、行為認知、用戶旅程分析與數據集成。">
                        
            				        </div>					
            					    </div>
            				    </div>
                              
            </section>
			<section id="auro_cdp" class="ftco-section">
							
								<div class="row  justify-content-end">
			                        <div class="col-md-10">
									<div class="col-md-12 project ftco-animate">
										<div class="img img-fluid-d" style="height: 50vw; background-image: url(images/cdp01.webp); background-size:cover; background-position: center center;" alt="顧客體驗分析：業界唯一開創『可視化顧客旅程』透過顧客數位行為軌跡，全面掌握顧客線上操作行為與瀏覽習慣，洞察顧客操作困境，有效挽回流失顧客。可視化影像回放，了解使用者實際操作瀏覽狀況，左側可看見使用者所有動作（如點擊、填寫資料等）。從Session Replay中，也可看見該頁程式資訊，方便行銷人員與IT溝通。">    
										<div class="text text-right">
											<h2>CDP</h2>
										</div>
										</div>
			                            <div class="img img-fluid-d ftco-animate" style="height: 50vw; background-image: url(images/cdp02.webp); background-size:cover; background-position: center center;" alt="表格分析＆熱點圖：可了解使用者於網頁上欄位填寫的跳離比率、花費多久時間填寫、重複修改次數等。熱點圖可了解客戶點擊熱區，哪些是使用者最常點擊的地方。">
										</div>
			                            <div class="img img-fluid-d ftco-animate" style="height: 50vw; background-image: url(images/cdp03.webp); background-size:cover; background-position: center center;" alt="CDP基本架構：檢視各產業、電商於坊間常用數據觀測工具，了解顧客實際旅程，快速檢視整體/分店業績、會員數、熱賣品狀態等，有效檢視行銷活動策略、廣告表現、客戶貼標等項目，個性化分眾行銷，讓運營策略再進化。">
										</div>
			                        
			                            <img src="images/cdp01-m.webp" class="img-fluid-m ftco-animate" alt="解決方案與產品：CXA顧客體驗分析、CDP顧客數據平台">
			                            <img src="images/cdp02-m.webp" class="img-fluid-m ftco-animate" alt="解決方案與產品：HCL Unica行銷自動化、Magnolia CMS內容管理">
                                        <img src="images/cdp03-m.webp" class="img-fluid-m ftco-animate" alt="解決方案與產品：HCL Unica行銷自動化、Magnolia CMS內容管理">
			            
							        </div>					
								    </div>
							    </div>
			                  
			</section>
			<section id="hcl_unica" class="ftco-section">
							
								<div class="row  justify-content-end">
			                        <div class="col-md-10">
									<div class="col-md-12 project ftco-animate">
										<div class="img img-fluid-d" style="height: 50vw; background-image: url(images/hclunica01.webp); background-size:cover; background-position: center center;" alt="行銷自動化：通過 HCL Unica 精準行銷工具，可以透過設定規則降低活動接觸疲勞，並且使用客戶喜歡的通路來降低排斥，在正確的時間向正確的目標客戶提供正確的活動內容!進而提高品牌活動精準度與增加品牌忠誠度。">    
										<div class="text text-left">
											<h2>HCL UNICA</h2>
										</div>
										</div>
			                            <div class="img img-fluid-d ftco-animate" style="height: 50vw; background-image: url(images/hclunica02.webp); background-size:cover; background-position: center center;" alt="HCL Unica-Plan 模組：管理您的行銷計畫，專案計畫專案和請求、管理您的資源，任務，批准和工作流程、管理您的預算，訂單和分配、在創意，抵押品和其他數位資產上進行協同合作、計畫您的廣告系列，活動內容和目標客群。HCL Unica-Campaign 模組：控制和精確地建立客戶群、跨通路和接觸點共用客戶群和清單、從多個來源訪問客戶資料、大規模個人化活動、通過整合活動聯繫和響應跟蹤來閉合環路。">
										</div>
			                            <div class="img img-fluid-d ftco-animate" style="height: 50vw; background-image: url(images/hclunica03.webp); background-size:cover; background-position: center center;" alt="HCL Unica-Optimize 模組：確保注意接觸疲勞和客戶喜好並重、避免廣告系列之間的優惠活動衝突和冗餘、在廣告、客戶和活動優惠整體下提供營銷預算的優化、根據行銷能力確認和定位聯繫通路、基於業務目標或KPI對活動進行評分。HCL Unica-Journey 模組：即時定義和調整目標驅動的客戶體驗、視覺化，創建，執行和衡量個人化的全通路客▪戶體驗、一站式涵蓋客戶參與的所有通路、來自使用者介面發起帶入或發送客戶交互資▪料資料到任何接觸點。">
										</div>
										<div class="img img-fluid-d ftco-animate" style="height: 50vw; background-image: url(images/hclunica04.webp); background-size:cover; background-position: center center;" alt="HCL Unica-Interact 模組:基於個人資料，上下文和行為的優化個人化推推薦、可插入任何通路應用：網站、電子郵件、IVR、、互動式資訊服務站(Kiosk)、POS銷售點、ATM等、A/B測試以優化下一個最佳參與選擇、在內建的認知學習中提供建議、通過分群，活動和連絡人/回應等資料共用來調整推播式(outbound)和集客式(inbound)的個人化設置。HCL Unica-Deliver 模組:通過電子郵件，簡訊通路發送和追蹤個人化通信、有效的電子郵件設計和郵件內容的A/B測試、生產力工具可自動執行複雜的體驗、通路事件可以驅動整合後續的聯繫和回應跟蹤。">
										</div>
										<div class="img img-fluid-d ftco-animate" style="height: 50vw; background-image: url(images/hclunica05.webp); background-size:cover; background-position: center center;" alt="HCL Unica-Link 模組:資料來源和目標端點之間提供指向和點擊資▪料資料對映、標準和簡化的工具，可實現快速整合、支援身份驗證，限制和重試策略、領先的電子郵件，SMS，CRM供應商的連接能力。HCL Unica-附加組件:Unica COM 集中是促銷活動管理、Unica Director 佈置監控、Unica Insights 即時洞察。">
										</div>
			                        
			                            <img src="images/hclunica01-m.webp" class="img-fluid-m ftco-animate" alt="行銷自動化：通過 HCL Unica 精準行銷工具，可以透過設定規則降低活動接觸疲勞，並且使用客戶喜歡的通路來降低排斥，在正確的時間向正確的目標客戶提供正確的活動內容!進而提高品牌活動精準度與增加品牌忠誠度。">
			                            <img src="images/hclunica02-m.webp" class="img-fluid-m ftco-animate" alt="HCL Unica-Plan 模組：管理您的行銷計畫，專案計畫專案和請求、管理您的資源，任務，批准和工作流程、管理您的預算，訂單和分配、在創意，抵押品和其他數位資產上進行協同合作、計畫您的廣告系列，活動內容和目標客群。HCL Unica-Campaign 模組：控制和精確地建立客戶群、跨通路和接觸點共用客戶群和清單、從多個來源訪問客戶資料、大規模個人化活動、通過整合活動聯繫和響應跟蹤來閉合環路。">
                                        <img src="images/hclunica03-m.webp" class="img-fluid-m ftco-animate" alt="HCL Unica-Optimize 模組：確保注意接觸疲勞和客戶喜好並重、避免廣告系列之間的優惠活動衝突和冗餘、在廣告、客戶和活動優惠整體下提供營銷預算的優化、根據行銷能力確認和定位聯繫通路、基於業務目標或KPI對活動進行評分。HCL Unica-Journey 模組：即時定義和調整目標驅動的客戶體驗、視覺化，創建，執行和衡量個人化的全通路客▪戶體驗、一站式涵蓋客戶參與的所有通路、來自使用者介面發起帶入或發送客戶交互資▪料資料到任何接觸點。">
			                            <img src="images/hclunica04-m.webp" class="img-fluid-m ftco-animate" alt="HCL Unica-Interact 模組:基於個人資料，上下文和行為的優化個人化推推薦、可插入任何通路應用：網站、電子郵件、IVR、、互動式資訊服務站(Kiosk)、POS銷售點、ATM等、A/B測試以優化下一個最佳參與選擇、在內建的認知學習中提供建議、通過分群，活動和連絡人/回應等資料共用來調整推播式(outbound)和集客式(inbound)的個人化設置。HCL Unica-Deliver 模組:通過電子郵件，簡訊通路發送和追蹤個人化通信、有效的電子郵件設計和郵件內容的A/B測試、生產力工具可自動執行複雜的體驗、通路事件可以驅動整合後續的聯繫和回應跟蹤。">
                                        <img src="images/hclunica05-m.webp" class="img-fluid-m ftco-animate" alt="HCL Unica-Link 模組:資料來源和目標端點之間提供指向和點擊資▪料資料對映、標準和簡化的工具，可實現快速整合、支援身份驗證，限制和重試策略、領先的電子郵件，SMS，CRM供應商的連接能力。HCL Unica-附加組件:Unica COM 集中是促銷活動管理、Unica Director 佈置監控、Unica Insights 即時洞察。">
			            
							        </div>					
								    </div>
							    </div>
			                  
			</section>
			<section id="magnolia_cms" class="ftco-section">
							
								<div class="row  justify-content-end">
			                        <div class="col-md-10">
									<div class="col-md-12 project ftco-animate">
										<div class="img img-fluid-d" style="height: 50vw; background-image: url(images/magnoliaCMS01.webp); background-size:cover; background-position: center center;" alt="內容管理Magnolia CMS:快速、多元、靈活，讓繁雜的內容管理，變的得心應手! Magnolia 的優勢:多元快速簡單、專注、無阻的團隊合作、達成實際效益。">    
										<div class="text text-right">
											<h2>Magnolia CMS</h2>
										</div>
										</div>
			                            <div class="img img-fluid-d ftco-animate" style="height: 50vw; background-image: url(images/magnoliaCMS02.webp); background-size:cover; background-position: center center;" alt="Magnolia 整合框架:商務框架+行銷自動化框架+數位資產管理框架+分析框架">
										</div>
			                            <div class="img img-fluid-d ftco-animate" style="height: 50vw; background-image: url(images/magnoliaCMS03.webp); background-size:cover; background-position: center center;" alt="為現實您行銷需求而設計的平台:以視覺方式構建體驗、跨網站和渠道重用內容、個性化和優化、利用 AI 增強內容創作。">
										</div>
										<div class="img img-fluid-d ftco-animate" style="height: 50vw; background-image: url(images/magnoliaCMS04.webp); background-size:cover; background-position: center center;" alt="更快的數位交付-不再憂慮權衡取捨:內容中心整合多個來源的內容，允許跨渠道重複使用。輕鬆集成連接現在和未來的任何數據源、應用程序或渠道。統一創作無論內容來源如何，都可以在一個無縫工作流程中創建體驗。">
										</div>
										<div class="img img-fluid-d ftco-animate" style="height: 50vw; background-image: url(images/magnoliaCMS05.webp); background-size:cover; background-position: center center;" alt="功能介紹-創造:享受有特色的創作體驗並創建客戶喜愛的網頁界面。Magnolia 為您提供強大的工具和容易使用的界面，使工作更有效率工作。">
										</div>
										<div class="img img-fluid-d ftco-animate" style="height: 50vw; background-image: url(images/magnoliaCMS06.webp); background-size:cover; background-position: center center;" alt="功能介紹-管理:在一處訪問和管理您的所有內容、數據和應用程序。 Magnolia 允許您引入所有來源的內容，對其進行有效組織，並根據您自己的內部流程和工作流程使用它。">
										</div>
										<div class="img img-fluid-d ftco-animate" style="height: 50vw; background-image: url(images/magnoliaCMS07.webp); background-size:cover; background-position: center center;" alt="功能介紹-渠道:通過一個界面在網絡和所有渠道上提供引人入勝的體驗。Magnolia 能夠統一客戶旅程並創建全渠道體驗，從而增加流量、參與度和忠誠度。">
										</div>
										<div class="img img-fluid-d ftco-animate" style="height: 50vw; background-image: url(images/magnoliaCMS08.webp); background-size:cover; background-position: center center;" alt="功能介紹-優化:享受有特色的創作體驗並創建客戶喜愛的網頁界面。Magnolia 為您提供強大的工具和容易使用的界面，使工作更有效率工作。">
										</div>
			                        
			                            <img src="images/magnoliaCMS01-m.webp" class="img-fluid-m ftco-animate" alt="內容管理Magnolia CMS:快速、多元、靈活，讓繁雜的內容管理，變的得心應手! Magnolia 的優勢:多元快速簡單、專注、無阻的團隊合作、達成實際效益。">
			                            <img src="images/magnoliaCMS02-m.webp" class="img-fluid-m ftco-animate" alt="為現實您行銷需求而設計的平台:以視覺方式構建體驗、跨網站和渠道重用內容、個性化和優化、利用 AI 增強內容創作。">
                                        <img src="images/magnoliaCMS03-m.webp" class="img-fluid-m ftco-animate" alt="更快的數位交付-不再憂慮權衡取捨:內容中心整合多個來源的內容，允許跨渠道重複使用。輕鬆集成連接現在和未來的任何數據源、應用程序或渠道。統一創作無論內容來源如何，都可以在一個無縫工作流程中創建體驗。">
                                        <img src="images/magnoliaCMS04-m.webp" class="img-fluid-m ftco-animate" alt="功能介紹-創造:享受有特色的創作體驗並創建客戶喜愛的網頁界面。Magnolia 為您提供強大的工具和容易使用的界面，使工作更有效率工作。">
                                        <img src="images/magnoliaCMS05-m.webp" class="img-fluid-m ftco-animate" alt="功能介紹-管理:在一處訪問和管理您的所有內容、數據和應用程序。 Magnolia 允許您引入所有來源的內容，對其進行有效組織，並根據您自己的內部流程和工作流程使用它。">
                                        <img src="images/magnoliaCMS06-m.webp" class="img-fluid-m ftco-animate" alt="功能介紹-渠道:通過一個界面在網絡和所有渠道上提供引人入勝的體驗。Magnolia 能夠統一客戶旅程並創建全渠道體驗，從而增加流量、參與度和忠誠度。">
                                        <img src="images/magnoliaCMS07-m.webp" class="img-fluid-m ftco-animate" alt="功能介紹-優化:享受有特色的創作體驗並創建客戶喜愛的網頁界面。Magnolia 為您提供強大的工具和容易使用的界面，使工作更有效率工作。">
			            
							        </div>					
								    </div>
							    </div>
			</section>
		
	        <footer id="footer-sec" class="ftco-footer ftco-bg-dark ftco-section">
		        <?php include './includes/footer_simple.php'; ?>
	        </footer>
		    </div><!-- END COLORLIB-MAIN -->
	        </div><!-- END COLORLIB-PAGE -->

  <!-- loader -->
  <div id="ftco-loader" class="show fullscreen"><svg class="circular" width="48px" height="48px"><circle class="path-bg" cx="24" cy="24" r="22" fill="none" stroke-width="4" stroke="#eeeeee"/><circle class="path" cx="24" cy="24" r="22" fill="none" stroke-width="4" stroke-miterlimit="10" stroke="#F96D00"/></svg></div>

    <!-- ✅ 優化後的 JS 載入 -->
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