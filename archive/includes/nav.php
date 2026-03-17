<?php
/**
 * 動態路徑計算
 * 使用 __DIR__ 計算相對於網站根目錄的路徑
 * 
 * 範例:
 * - index.php → base=''
 * - blogpost/single.php → base='../'
 */
if (!isset($base)) {
    // nav.php 所在的 includes 資料夾
    $includes_dir = __DIR__;
    // 網站根目錄 (includes 的上一層)
    $root_dir = dirname($includes_dir);
    // 當前執行的 PHP 檔案所在目錄
    $current_dir = dirname($_SERVER['SCRIPT_FILENAME']);
    
    // 標準化路徑 (統一使用 /)
    $root_dir = str_replace('\\', '/', $root_dir);
    $current_dir = str_replace('\\', '/', $current_dir);
    
    // 計算當前頁面相對於根目錄的深度
    if ($current_dir === $root_dir) {
        // 在根目錄
        $base = '';
    } else {
        // 在子目錄，計算需要往上幾層
        $relative = str_replace($root_dir . '/', '', $current_dir . '/');
        $depth = substr_count(trim($relative, '/'), '/') + 1;
        $base = str_repeat('../', $depth);
    }
}
?>

<nav id="colorlib-main-menu" role="navigation">
  	<ul>
  		<li><a href="<?php echo $base; ?>marketing.php">數位行銷</a></li>
  		<li><a href="<?php echo $base; ?>solution.php">解決方案＆產品</a></li>
  		<li><a href="https://cti.aurocore.com/index.html" target="_blank">客服中心</a></li>
  		<li><a href="<?php echo $base; ?>ai-companion.php">AI 智慧語伴</a></li>
  		<li><a href="<?php echo $base; ?>blog.php">新聞中心</a></li>
  		<li><a href="<?php echo $base; ?>contact.php">聯絡我們</a></li>
  	</ul>
  	<p class="social">
          <span><a href="https://www.facebook.com/AurobaseTW/" target="_blank"><svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="currentColor" class="bi bi-facebook" viewBox="0 0 16 16">
          <path d="M16 8.049c0-4.446-3.582-8.05-8-8.05C3.58 0-.002 3.603-.002 8.05c0 4.017 2.926 7.347 6.75 7.951v-5.625h-2.03V8.05H6.75V6.275c0-2.017 1.195-3.131 3.022-3.131.876 0 1.791.157 1.791.157v1.98h-1.009c-.993 0-1.303.621-1.303 1.258v1.51h2.218l-.354 2.326H9.25V16c3.824-.604 6.75-3.934 6.75-7.951"/>
          </svg> 粉絲專頁</a></span>
  	</p>
  </nav>
  
  <div class="colorlib-footer">
  	<h1><a href="<?php echo $base; ?>index.php">
          <img src="<?php echo $base; ?>images/logo.svg" style="max-width: 185px" alt="AUROBASE" />
      </a></h1>
  </div>