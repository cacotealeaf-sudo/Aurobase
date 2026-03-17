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
    
    <!-- ✅ LINE Seed 字體家族 (與 index.php 一致) -->
    <link rel="preload" href="WOFF2/LINESeedSans_W_Rg.woff2" as="font" type="font/woff2" crossorigin>
    <link rel="preload" href="WOFF2/LINESeedTW_OTF_Rg.woff2" as="font" type="font/woff2" crossorigin>
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
			
      <!-- particles.js container -->
      <div id="particles-js"></div>
      
      <section class="ftco-section ftco-bread ftco-extend-mb">
				<div class="container-fluid px-3 px-md-0">
					<div class="row no-gutters slider-text justify-content-end align-items-center">
	          <div class="col-md-10 ftco-animate">
	            <p class="breadcrumbs"><span class="mr-2"><a href="index.php">首頁</a></span> <span>新聞中心</span></p>
				      <br />
				      <h3 style="color:#28282c; text-indent: 0.35em;">▏提供您最專業獨到的品牌經營、廣告投放規劃、行銷科技分析情報！</h3> 
	          </div>
	        </div>
				</div>
			</section> 

			<!-- Blog Section -->
			<section id="blog-cards" class="ftco-section ftco-no-pt">  
			  <?php include './includes/blog_cards.php'; ?>
      </section>
			
	    <footer id="footer-sec" class="ftco-footer ftco-bg-dark ftco-section">
		    <?php include './includes/footer_simple.php'; ?>
	    </footer>
	  </div><!-- END COLORLIB-MAIN -->
	</div><!-- END COLORLIB-PAGE -->

  <!-- loader -->
  <div id="ftco-loader" class="show fullscreen"><svg class="circular" width="48px" height="48px"><circle class="path-bg" cx="24" cy="24" r="22" fill="none" stroke-width="4" stroke="#eeeeee"/><circle class="path" cx="24" cy="24" r="22" fill="none" stroke-width="4" stroke-miterlimit="10" stroke="#F96D00"/></svg></div>

  <!-- ✅ 優化後的 JS -->
  <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
  <script src="js/jquery.min.js"></script>
  <script src="js/popper.min.js"></script>
  <script src="js/bootstrap.min.js"></script>
  <script src="js/jquery.waypoints.min.js"></script>
  <script src="js/owl.carousel.min.js"></script>
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
