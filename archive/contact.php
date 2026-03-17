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
    <div id="colorlib-page">
        <a href="#" class="js-colorlib-nav-toggle colorlib-nav-toggle"><i></i></a>
        <aside id="colorlib-aside" role="complementary" class="js-fullheight">
          <?php include './includes/nav.php'; ?>
        </aside>
        <!-- END COLORLIB-ASIDE -->
        <div id="colorlib-main">
            <!-- particles.js container -->
            <div id="particles-js"></div>
            <section class="ftco-section ftco-bread ftco-extend-mb">
                <div class="container-fluid px-3 px-md-0">
                    <div class="row no-gutters slider-text justify-content-end align-items-center">
                        <div class="col-md-10 ftco-animate">
                            <p class="breadcrumbs">
                                <span class="mr-2"><a href="index.php">首頁</a></span> <span>聯絡我們</span>
                            </p>
                            <br />
                            <h3 style="color:#28282c; text-indent: 0.35em;">▏全球辦公室據點</h3> 
                        </div>
                    </div>
                </div>
            </section>

            <section class="ftco-section contact-section ftco-no-pt">
                <div class="container-fluid px-md-0 px-3">
                    <div class="row mb-5 contact-info justify-content-end">
                        <div class="col-md-5">
                            <h2><b>奧洛/特聿科技行銷 股份有限公司</b></h2>
                            <div class="row">
                                <div class="col-md-9">
                                    <div class="info py-4">
                                        <p><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-geo-alt-fill" viewBox="0 0 16 16">
                                        <path d="M8 16s6-5.686 6-10A6 6 0 0 0 2 6c0 4.314 6 10 6 10m0-7a3 3 0 1 1 0-6 3 3 0 0 1 0 6"/>
                                        </svg> 114 台北市內湖區洲子街101號2樓</p>
                                        <p><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-telephone-fill" viewBox="0 0 16 16">
                                        <path fill-rule="evenodd" d="M1.885.511a1.745 1.745 0 0 1 2.61.163L6.29 2.98c.329.423.445.974.315 1.494l-.547 2.19a.68.68 0 0 0 .178.643l2.457 2.457a.68.68 0 0 0 .644.178l2.189-.547a1.75 1.75 0 0 1 1.494.315l2.306 1.794c.829.645.905 1.87.163 2.611l-1.034 1.034c-.74.74-1.846 1.065-2.877.702a18.6 18.6 0 0 1-7.01-4.42 18.6 18.6 0 0 1-4.42-7.009c-.362-1.03-.037-2.137.703-2.877z"/>
                                        </svg><a href="tel:+886-2-5568-4688"> 02-5568-4688</a></p>
                                        <p><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-printer-fill" viewBox="0 0 16 16">
                                        <path d="M5 1a2 2 0 0 0-2 2v1h10V3a2 2 0 0 0-2-2zm6 8H5a1 1 0 0 0-1 1v3a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1v-3a1 1 0 0 0-1-1"/>
                                        <path d="M0 7a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2h-1v-2a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v2H2a2 2 0 0 1-2-2zm2.5 1a.5.5 0 1 0 0-1 .5.5 0 0 0 0 1"/>
                                        </svg> 02-2659-6627</p>
                                        <p><a href="mailto:ad@aurocore.com"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-envelope-fill" viewBox="0 0 16 16">
                                        <path d="M.05 3.555A2 2 0 0 1 2 2h12a2 2 0 0 1 1.95 1.555L8 8.414zM0 4.697v7.104l5.803-3.558zM6.761 8.83l-6.57 4.027A2 2 0 0 0 2 14h12a2 2 0 0 0 1.808-1.144l-6.57-4.027L8 9.586zm3.436-.586L16 11.801V4.697z"/>
                                        </svg> ad@aurocore.com</a></p>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-5">
                            <h2><b>廣州辦事處</b></h2>
                            <div class="row">
                                <div class="col-md-9">
                                    <div class="info py-4">
                                        <p><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-geo-alt-fill" viewBox="0 0 16 16">
                                        <path d="M8 16s6-5.686 6-10A6 6 0 0 0 2 6c0 4.314 6 10 6 10m0-7a3 3 0 1 1 0-6 3 3 0 0 1 0 6"/>
                                        </svg> 广州市天河区岑村圣堂大街工业区3号321室</p>
                                        <p><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-telephone-fill" viewBox="0 0 16 16">
                                        <path fill-rule="evenodd" d="M1.885.511a1.745 1.745 0 0 1 2.61.163L6.29 2.98c.329.423.445.974.315 1.494l-.547 2.19a.68.68 0 0 0 .178.643l2.457 2.457a.68.68 0 0 0 .644.178l2.189-.547a1.75 1.75 0 0 1 1.494.315l2.306 1.794c.829.645.905 1.87.163 2.611l-1.034 1.034c-.74.74-1.846 1.065-2.877.702a18.6 18.6 0 0 1-7.01-4.42 18.6 18.6 0 0 1-4.42-7.009c-.362-1.03-.037-2.137.703-2.877z"/>
                                        </svg> 18925022494</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="row block-9 justify-content-end">
                        <div class="col-md-10">
                            <div class="row">
                                <div class="col-md-6 d-flex">
                                    <iframe
                                        class="position-absolute w-100 h-100"
                                        style="object-fit: cover;"
                                        src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3613.6430423887405!2d121.5651966726451!3d25.08008498717496!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3442ac6f755c2fb3%3A0xd1e120b473f5358f!2zMTE05Y-w5YyX5biC5YWn5rmW5Y2A5rSy5a2Q6KGXMTAx6Jmf!5e0!3m2!1szh-TW!2stw!4v1705648910939!5m2!1szh-TW!2stw"
                                        frameborder="0"
                                        allowfullscreen=""
                                        aria-hidden="false"
                                        tabindex="0"
                                    ></iframe>
                                </div>
                                <div class="col-md-6 d-flex">
                                    <form id="contactpage-form"   class="bg-white p-5 contact-form">
                                        <?php include './includes/contactpageform.php'; ?>
                                    </form>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <footer class="ftco-footer ftco-bg-dark ftco-section">
               <?php include './includes/footer_simple.php'; ?>
	        </footer>
            </div><!-- END COLORLIB-MAIN -->
	        </div><!-- END COLORLIB-PAGE -->

    <!-- loader -->
    <div id="ftco-loader" class="show fullscreen">
        <svg class="circular" width="48px" height="48px">
            <circle class="path-bg" cx="24" cy="24" r="22" fill="none" stroke-width="4" stroke="#eeeeee" />
            <circle class="path" cx="24" cy="24" r="22" fill="none" stroke-width="4" stroke-miterlimit="10" stroke="#F96D00" />
        </svg>
    </div>
    
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