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
          <a href="#advertising" class="btn btn-primary btn-sm">廣告投放</a>
          <a href="#community" class="btn btn-primary btn-sm">社群服務</a>
          <a href="#data_analysis" class="btn btn-primary btn-sm">數據分析</a>
        </div>
        <!-- END Anchor manu -->
        
		<div id="colorlib-main">
          <!-- particles.js container
          <div id="particles-js"></div> -->
           <section class="ftco-section ftco-bread ftco-extend-mb">
				<div class="container-fluid px-3 px-md-0">
					<div class="row no-gutters slider-text justify-content-end align-items-center">
	          <div class="col-md-10 ftco-animate">
	            <p class="breadcrumbs"><span class="mr-2"><a href="index.php">首頁</a></span> <span>數位行銷</span></p><br>
                <h2 style="color:#d9e0e7;">數位行銷</h2>  
	          </div>
	        </div>
				</div>
			</section>   
            <section id="advertising" class="ftco-section">
				
					<div class="row  justify-content-end">
                        <div class="col-md-10">
						<div class="col-md-12 project ftco-animate">
							<div class="img img-fluid-d" style="height: 50vw; background-image: url(images/google01.webp); background-size:cover; background-position: center center;" alt="google關鍵字廣告:茫茫人海如何相遇，使用關鍵字搜尋增加曝光成交率，客製化文案及網站額外資訊吸引消費者目光。">    
							<div class="text text-left">
								<h2>廣告投放</h2>
							</div>
							</div>
                            <div class="img img-fluid-d ftco-animate" style="height: 50vw; background-image: url(images/google02.webp); background-size:cover; background-position: center center;" alt="google GDN聯播網:無時無刻在你/妳身邊！強大媒合技術，使用內容搭配興趣設定，投放您的資訊到目標客戶眼中。">
							</div>
                            <div class="img img-fluid-d ftco-animate" style="height: 50vw; background-image: url(images/youtube01.webp); background-size:cover; background-position: center center;" alt="youtube影音廣告:在用戶觀看Youtube影音內容時，您可置入「5秒可略過」或「不可略過」的廣告影片，透過影音快速、廣泛地觸及您的目標客群。並在用戶與廣告互動的時候，引導到合適的網址來幫助您的業績成長！">
							</div>
                            <div class="img img-fluid-d ftco-animate" style="height: 50vw; background-image: url(images/yahoo01.webp); background-size:cover; background-position: center center;" alt="yahoo原生廣告:無縫接軌各種版面型式呈現，無論行動裝置或電腦，與客群溝通無礙，接觸範圍包括新聞網頁、網誌以及眾多入口網站，為品牌帶來大量曝光。">
							</div>
                            <div class="img img-fluid-d ftco-animate" style="height: 50vw; background-image: url(images/line.webp); background-size:cover; background-position: center center;" alt="LINE廣告廣告:台灣90%以上使用者日常通訊軟體：LINE，每月活躍用戶達2100萬以上，透過LINE行銷，您可以輕鬆融入潛在消費者的日常生活中，除了持續培養用戶的忠誠度，更可以在LINE上面獲得即時的消費者反饋！">
							</div>
                        
                            <img src="images/google01-m.webp" class="img-fluid-m ftco-animate" alt="google關鍵字廣告:茫茫人海如何相遇，使用關鍵字搜尋增加曝光成交率，客製化文案及網站額外資訊吸引消費者目光。">
                            <img src="images/google02-m.webp" class="img-fluid-m ftco-animate" alt="google GDN聯播網:無時無刻在你/妳身邊！強大媒合技術，使用內容搭配興趣設定，投放您的資訊到目標客戶眼中。">
                            <img src="images/youtube01-m.webp" class="img-fluid-m ftco-animate" alt="youtube影音廣告:在用戶觀看Youtube影音內容時，您可置入「5秒可略過」或「不可略過」的廣告影片，透過影音快速、廣泛地觸及您的目標客群。並在用戶與廣告互動的時候，引導到合適的網址來幫助您的業績成長！">
                            <img src="images/yahoo01-m.webp" class="img-fluid-m ftco-animate" alt="yahoo原生廣告:無縫接軌各種版面型式呈現，無論行動裝置或電腦，與客群溝通無礙，接觸範圍包括新聞網頁、網誌以及眾多入口網站，為品牌帶來大量曝光。">
                            <img src="images/line-m.webp" class="img-fluid-m ftco-animate" alt="LINE廣告廣告:台灣90%以上使用者日常通訊軟體：LINE，每月活躍用戶達2100萬以上，透過LINE行銷，您可以輕鬆融入潛在消費者的日常生活中，除了持續培養用戶的忠誠度，更可以在LINE上面獲得即時的消費者反饋！">
            
				         </div>					
					     </div>
				     </div>
                  
		    </section> 
            
            <section id="community" class="ftco-section">
				
					<div class="row  justify-content-end">
                        <div class="col-md-10">
						<div class="col-md-12 project ftco-animate">
							<div class="img img-fluid-d" style="height: 50vw; background-image: url(images/fb&ig01.webp); background-size:cover; background-position: center center;" alt="Facebook社群/連結廣告，引導流量、活動推廣，內容利用大尺寸圖片曝光，吸引消費者(客群)目光，或可引導至購物頁面等。Facebook、Instagram貼文廣告，適用目標：活動曝光、推廣，利用大尺寸精美圖片曝光，吸引消費者目光， 活化粉絲 。(如：新品優惠、促銷等)。">    
							<div class="text text-right">
								<h2>社群服務</h2>
							</div>
							</div>
                            <div class="img img-fluid-d ftco-animate" style="height: 50vw; background-image: url(images/line_account.webp); background-size:cover; background-position: center center;" alt="LINE官方帳號建置:透過LINE官方帳號建置，可以協助您建立顧客分眾標籤，提升行銷活動的效益，穩定地留存舊有客戶；更可規劃如集點卡、優惠券、互動遊戲等行銷活動，有效地開發新的潛在客群。">
							</div>
                            <div class="img img-fluid-d ftco-animate" style="height: 50vw; background-image: url(images/social_listening.webp); background-size:cover; background-position: center center;" alt="輿情監測:您想知道品牌、產品或服務在網路上被討論的狀況嗎？又是在哪裡被討論呢？透過強大的社群監測工具與AI分析，幫助您找出網友討論的內容，並進一步挖掘其潛在情報，將正面的評論內容轉化為收入，同時迅速解決負面情緒，控管公關危機！">
							</div>
                            
                            <img src="images/fb&ig01-m.webp" class="img-fluid-m ftco-animate" alt="Facebook社群/連結廣告，引導流量、活動推廣，內容利用大尺寸圖片曝光，吸引消費者(客群)目光，或可引導至購物頁面等。Facebook、Instagram貼文廣告，適用目標：活動曝光、推廣，利用大尺寸精美圖片曝光，吸引消費者目光， 活化粉絲 。(如：新品優惠、促銷等)。">
                            <img src="images/line_account-m.webp" class="img-fluid-m ftco-animate" alt="LINE官方帳號建置:透過LINE官方帳號建置，可以協助您建立顧客分眾標籤，提升行銷活動的效益，穩定地留存舊有客戶；更可規劃如集點卡、優惠券、互動遊戲等行銷活動，有效地開發新的潛在客群。">
                            <img src="images/social_listening-m.webp" class="img-fluid-m ftco-animate" alt="輿情監測:您想知道品牌、產品或服務在網路上被討論的狀況嗎？又是在哪裡被討論呢？透過強大的社群監測工具與AI分析，幫助您找出網友討論的內容，並進一步挖掘其潛在情報，將正面的評論內容轉化為收入，同時迅速解決負面情緒，控管公關危機！">
            
				         </div>					
					     </div>
				     </div>
                  
		    </section> 
            
            <section id="data_analysis" class="ftco-section">
				
					<div class="row  justify-content-end">
                        <div class="col-md-10">
						<div class="col-md-12 project ftco-animate">
							<div class="img img-fluid-d" style="height: 50vw; background-image: url(images/analytics.webp); background-size:cover; background-position: center center;" alt="網頁行為分析:透過第三方監測工具(Google Analytics 、 Tealeaf)幫助您了解網站的流量狀況，從哪裡來、做了什麼事、去了哪裡...更重要的是，消費者是否有在網站達成目標(購買)？分析網頁行為，了解顧客偏好與使用障礙，提供網站優化建議與行銷策略的參考，幫助企業提高收益，提高顧客滿意度！">    
							<div class="text text-left">
								<h2>數據分析</h2>
							</div>
							</div>
                            
                            <img src="images/analytics-m.webp" class="img-fluid-m ftco-animate" alt="網頁行為分析:透過第三方監測工具(Google Analytics 、 Tealeaf)幫助您了解網站的流量狀況，從哪裡來、做了什麼事、去了哪裡...更重要的是，消費者是否有在網站達成目標(購買)？分析網頁行為，了解顧客偏好與使用障礙，提供網站優化建議與行銷策略的參考，幫助企業提高收益，提高顧客滿意度！">
            
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