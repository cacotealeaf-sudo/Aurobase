<?php
/**
 * 相關文章推薦 - 從 Meta 標籤自動提取資訊
 * 隨機顯示 3 篇文章
 */

// 獲取當前文章檔名
$current_post = basename($_SERVER['PHP_SELF']);

// 掃描 blogpost 目錄
$blog_dir = __DIR__ . '/../blogpost/';
$post_files = glob($blog_dir . 'single-*.php');

$all_posts = [];

// 遍歷每個文章檔案,提取 Meta 資訊
foreach ($post_files as $file) {
    $filename = basename($file);
    
    // 排除當前文章
    if ($filename === $current_post) {
        continue;
    }
    
    // 讀取檔案內容
    $content = file_get_contents($file);
    
    // 提取 Meta 標籤內容
    $title = '';
    $category = '';
    $date = '';
    $image = '';
    
    // 提取 article-title
    if (preg_match('/<meta name="article-title" content="([^"]+)"/', $content, $match)) {
        $title = $match[1];
    }
    
    // 提取 article-category
    if (preg_match('/<meta name="article-category" content="([^"]+)"/', $content, $match)) {
        $category = $match[1];
    }
    
    // 提取 article-date
    if (preg_match('/<meta name="article-date" content="([^"]+)"/', $content, $match)) {
        $date = $match[1];
    }
    
    // 提取 article-image
    if (preg_match('/<meta name="article-image" content="([^"]+)"/', $content, $match)) {
        $image = $match[1];
    }
    
    // 如果成功提取到標題,則加入列表
    if (!empty($title)) {
        $all_posts[] = [
            'url' => $filename,
            'title' => $title,
            'category' => $category ?: '未分類',
            'date' => $date ?: '',
            'image' => $image ?: '../images/default.jpg'
        ];
    }
}

// 隨機打亂並取 3 篇
shuffle($all_posts);
$related_posts = array_slice($all_posts, 0, 3);
?>

<!-- 相關文章推薦區塊 -->
<div class="sidebar-box ftco-animate">
    <h3 class="heading-2">相關文章推薦</h3>
    
    <?php if (!empty($related_posts)): ?>
        <?php foreach ($related_posts as $post): ?>
        <div class="block-21 mb-4 d-flex">
            <a href="<?php echo htmlspecialchars($post['url']); ?>" 
               class="blog-img mr-4" 
               style="background-image: url(<?php echo htmlspecialchars($post['image']); ?>);"></a>
            <div class="text">
                <h3 class="heading">
                    <a href="<?php echo htmlspecialchars($post['url']); ?>">
                        <?php echo htmlspecialchars($post['title']); ?>
                    </a>
                </h3>
                <div class="meta">
                    <div><a href="#"><span class="icon-calendar"></span> <?php echo htmlspecialchars($post['date']); ?></a></div>
                    <div><a href="#"><span class="icon-folder-o"></span> <?php echo htmlspecialchars($post['category']); ?></a></div>
                </div>
            </div>
        </div>
        <?php endforeach; ?>
    <?php else: ?>
        <p class="text-muted">暫無相關文章</p>
    <?php endif; ?>
</div>

<!-- 返回新聞中心按鈕 -->
<div class="sidebar-box ftco-animate">
    <a href="../blog.php" class="btn btn-primary btn-block">
        <span class="icon-arrow-left"></span> 返回新聞中心
    </a>
</div>