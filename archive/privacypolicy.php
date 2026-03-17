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
		</aside> <!-- END COLORLIB-ASIDE -->
		<div id="colorlib-main">
			
          <!-- particles.js container -->
          <div id="particles-js"></div>
           <section class="ftco-section ftco-bread ftco-extend-mb">
				<div class="container-fluid px-3 px-md-0">
					<div class="row no-gutters slider-text justify-content-end align-items-center">
	          <div class="col-md-10 ftco-animate">
	            <p class="breadcrumbs"><span class="mr-2"><a href="index.php">首頁</a></span><span>隱私權政策</span></p><br> 
	          </div>
	        </div>
				</div>
			</section> 

			<section class="ftco-section ftco-no-pt">
	    	<div class="container-fluid px-3 px-md-0">
	    		<div class="row justify-content-end">
	    			<div class="col-md-10">
			    		<div class="row d-flex">
			    			<div class="col-lg-8 ftco-animate">
                       
			            <h1 class="mb-3 font-weight-bold">隱私權政策</h1>
                  <div class="container">
                    <p style="text-align: left; color: #4a4a4a;">本公司於您申請服務方案諮詢時，為提供本公司相關服務及行銷之目的，蒐集、處理及利用您的個人資料。有關個人資料相關應告知事項，請參閱本公司隱私權保護政策。</p>
                    <h4 class="mb-3 mt-5 font-weight-bold">隱私權保護政策的適用範圍</h4>
                    <p style="text-align: left; color: #4a4a4a;">隱私權保護政策內容，包括本網站如何處理在您使用網站服務時收集到的個人識別資料。隱私權保護政策不適用於本網站以外的相關連結網站，也不適用於非本網站所委託或參與管理的人員。</p>
                    <h4 class="mb-3 mt-5 font-weight-bold">個人資料的蒐集、處理及利用方式</h4>
                    <p style="text-align: left; color: #4a4a4a;">1. 當您造訪本網站或使用本網站所提供之功能服務時，我們將視該服務功能性質，請您提供必要的個人資料，並在該特定目的範圍內處理及利用您的個人資料；非經您書面同意，本網站不會將個人資料用於其他用途。</p>
                    <p style="text-align: left; color: #4a4a4a;">2. 本網站在您使用服務信箱、問卷調查等互動性功能時，會保留您所提供的姓名、電子郵件地址、聯絡方式及使用時間等。 </p>
                    <p style="text-align: left; color: #4a4a4a;">3. 於一般瀏覽時，伺服器會自行記錄相關行徑，包括您使用連線設備的 IP 位址、使用時間、使用的瀏覽器、瀏覽及點選資料記錄等，做為我們增進網站服務的參考依據，此記錄為內部應用，決不對外公佈。 </p>
                    <p style="text-align: left; color: #4a4a4a;">4. 為提供精確的服務，我們會將收集的問卷調查內容進行統計與分析，分析結果之統計數據或說明文字呈現，除供內部研究外，我們會視需要公佈統計數據及說明文字，但不涉及特定個人之資料。  </p>
                    <p style="text-align: left; color: #4a4a4a;">5. 您可以隨時向我們提出請求，以更正或刪除您的帳戶或本網站所蒐集的個人資料等隱私資訊。聯繫方式請見最下方聯繫管道。  </p>
                    <h4 class="mb-3 mt-5 font-weight-bold">資料之保護</h4>
                    <p style="text-align: left; color: #4a4a4a;">1. 本網站主機均設有防火牆、防毒系統等相關的各項資訊安全設備及必要的安全防護措施，加以保護網站及您的個人資料採用嚴格的保護措施，只由經過授權的人員才能接觸您的個人資料，相關處理人員皆簽有保密合約，如有違反保密義務者，將會受到相關的法律處分。</p>
                    <p style="text-align: left; color: #4a4a4a;">2. 如因業務需要有必要委託其他單位提供服務時，本網站亦會嚴格要求其遵守保密義務，並且採取必要檢查程序以確定其將確實遵守。 </p>
                    <h4 class="mb-3 mt-5 font-weight-bold">Cookie 之使用</h4>
                    <p style="text-align: left; color: #4a4a4a;">1. 為了提供您最佳的服務，本網站會在您的電腦中放置並取用我們的 Cookie，若您不願接受 Cookie 的寫入，您可在您使用的瀏覽器功能項中設定隱私權等級為高，即可拒絕 Cookie 的寫入，但可能會導致網站某些功能無法正常執行 。</p>
                    <p style="text-align: left; color: #4a4a4a;">本平台可能因廣告或其他合作促銷活動而包含其他平台之連結，您點選該等連結至其他平台，即不適用本平台使用條款及隱私權政策之規範。您須自行判斷各該平台相關條款對您的權益保障是否足夠，再決定是否使用該平台服務。</p>
                  </div>
			           
			            <!-- <div class="tag-widget post-tag-container mb-5 mt-5">
			              <div class="tagcloud">
			                <a href="#" class="tag-cloud-link">品牌經營</a>
			                <a href="#" class="tag-cloud-link">行銷科技</a>
			                <a href="#" class="tag-cloud-link">數位廣告</a>
			              </div>
			            </div> -->
			    		</div>
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
  <script src="js/aos.js"></script>
  <script src="js/external-link-warning.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
  <script src="js/main_optimized.js"></script>
  <script src="js/form-validator.js"></script>
  <script src="js/rate-limiter.js"></script>
  <script src="js/qform.js"></script>
  </body>
</html>