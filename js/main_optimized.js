/**
 * Aurobase 官網主要 JavaScript
 * Phase 1 優化後 + Particles.js 性能優化
 */

// AOS 滾動動畫初始化
AOS.init({
  duration: 800,
  easing: "slide"
});

(function($) {
  "use strict";

  var counter = 0;

  // 已移除 Stellar (未使用的視差效果)
  
  // 全高度元素設定
  $(".js-fullheight").css("height", $(window).height());
  $(window).resize(function() {
    $(".js-fullheight").css("height", $(window).height());
  });

  // 載入動畫移除
  setTimeout(function() {
    if ($("#ftco-loader").length > 0) {
      $("#ftco-loader").removeClass("show");
    }
  }, 1);

  // 已移除 Scrollax (與 AOS 重複)

  // 導航選單切換
  $(".js-colorlib-nav-toggle").on("click", function(event) {
    event.preventDefault();
    var $this = $(this);
    
    if ($("body").hasClass("offcanvas")) {
      $this.removeClass("active");
      $("body").removeClass("offcanvas");
    } else {
      $this.addClass("active");
      $("body").addClass("offcanvas");
    }
  });

  // 點擊外部關閉導航
  $(document).click(function(event) {
    var $trigger = $("#colorlib-aside, .js-colorlib-nav-toggle");
    if (!$trigger.is(event.target) && $trigger.has(event.target).length === 0) {
      if ($("body").hasClass("offcanvas")) {
        $("body").removeClass("offcanvas");
        $(".js-colorlib-nav-toggle").removeClass("active");
      }
    }
  });

  // 滾動時關閉導航
  $(window).scroll(function() {
    if ($("body").hasClass("offcanvas")) {
      $("body").removeClass("offcanvas");
      $(".js-colorlib-nav-toggle").removeClass("active");
    }
  });

  // 首頁輪播 (如果存在)
  if ($(".home-slider").length > 0) {
    $(".home-slider").owlCarousel({
      loop: true,
      autoplay: true,
      margin: 0,
      animateOut: "fadeOut",
      animateIn: "fadeIn",
      nav: false,
      autoplayHoverPause: false,
      items: 1,
      navText: [
        "<span class='ion-md-arrow-back'></span>",
        "<span class='ion-chevron-right'></span>"
      ],
      responsive: {
        0: { items: 1 },
        600: { items: 1 },
        1000: { items: 1 }
      }
    });
  }

  // 作者輪播 (如果存在)
  if ($(".author-slider").length > 0) {
    $(".author-slider").owlCarousel({
      autoplay: true,
      loop: true,
      items: 1,
      margin: 30,
      stagePadding: 0,
      nav: true,
      dots: true,
      navText: [
        '<span class="ion-ios-arrow-back">',
        '<span class="ion-ios-arrow-forward">'
      ],
      responsive: {
        0: { items: 1 },
        600: { items: 1 },
        1000: { items: 1 }
      }
    });
  }

  // Waypoints 動畫
  $(".ftco-animate").waypoint(
    function(direction) {
      if (direction === "down" && !$(this.element).hasClass("ftco-animated")) {
        counter++;
        $(this.element).addClass("item-animate");
        setTimeout(function() {
          $("body .ftco-animate.item-animate").each(function(k) {
            var el = $(this);
            setTimeout(
              function() {
                var effect = el.data("animate-effect");
                if (effect === "fadeIn") {
                  el.addClass("fadeIn ftco-animated");
                } else if (effect === "fadeInLeft") {
                  el.addClass("fadeInLeft ftco-animated");
                } else if (effect === "fadeInRight") {
                  el.addClass("fadeInRight ftco-animated");
                } else {
                  el.addClass("fadeInUp ftco-animated");
                }
                el.removeClass("item-animate");
              },
              k * 50,
              "easeInOutExpo"
            );
          });
        }, 100);
      }
    },
    { offset: "95%" }
  );

  // 數字計數動畫 (如果存在)
  if ($("#section-counter").length > 0) {
    $("#section-counter").waypoint(
      function(direction) {
        if (direction === "down" && !$(this.element).hasClass("ftco-animated")) {
          var comma_separator_number_step = $.animateNumber.numberStepFactories.separator(",");
          $(".number").each(function() {
            var $this = $(this);
            var num = $this.data("number");
            $this.animateNumber(
              {
                number: num,
                numberStep: comma_separator_number_step
              },
              7000
            );
          });
        }
      },
      { offset: "95%" }
    );
  }

  // 圖片彈窗
  $(".image-popup").magnificPopup({
    type: "image",
    closeOnContentClick: true,
    closeBtnInside: false,
    fixedContentPos: true,
    gallery: {
      enabled: true,
      navigateByImgClick: true,
      preload: [0, 1]
    },
    image: {
      verticalFit: true
    },
    zoom: {
      enabled: true,
      duration: 300
    }
  });

  // 影片彈窗
  $(".popup-youtube, .popup-vimeo, .popup-gmaps").magnificPopup({
    disableOn: 700,
    type: "iframe",
    mainClass: "mfp-fade",
    removalDelay: 160,
    preloader: false,
    fixedContentPos: false
  });

  // 已移除 YTPlayer (未使用)

})(jQuery);

/**
 * ========================================
 * Particles.js 性能優化配置
 * ========================================
 * 優化重點:
 * 1. 響應式粒子數 (桌面 60, 平板 40, 手機 25)
 * 2. 根據設備調整動畫速度
 * 3. 視窗隱藏時暫停動畫
 * 4. 減少互動效果的性能消耗
 * 5. 降低 Retina 顯示器的渲染壓力
 */

(function() {
  // ✅ 檢查頁面是否有 particles-js 容器
  if (!document.getElementById('particles-js')) {
    console.log('No particles-js container found, skipping initialization');
    return; // 如果沒有容器,直接退出
  }

  // 檢測設備類型和性能
  var isMobile = window.innerWidth < 768;
  var isTablet = window.innerWidth >= 768 && window.innerWidth < 1024;
  
  // 響應式粒子數量
  var particleCount;
  var moveSpeed;
  var lineDistance;
  
  if (isMobile) {
    particleCount = 25;  // 手機: 減少 75%
    moveSpeed = 2;       // 降低速度
    lineDistance = 100;  // 縮短連線距離
  } else if (isTablet) {
    particleCount = 40;  // 平板: 減少 60%
    moveSpeed = 4;
    lineDistance = 120;
  } else {
    particleCount = 60;  // 桌面: 減少 40%
    moveSpeed = 4;
    lineDistance = 150;
  }

  // 初始化 Particles.js
  particlesJS("particles-js", {
    particles: {
      number: {
        value: particleCount,
        density: {
          enable: true,
          value_area: 800
        }
      },
      color: {
        value: "#ffffff"
      },
      shape: {
        type: "circle",
        stroke: {
          width: 0,
          color: "#000000"
        }
      },
      opacity: {
        value: 0.5,
        random: false,
        anim: {
          enable: false,
          speed: 1,
          opacity_min: 0.1,
          sync: false
        }
      },
      size: {
        value: 3,
        random: true,
        anim: {
          enable: false,
          speed: 40,
          size_min: 0.1,
          sync: false
        }
      },
      line_linked: {
        enable: true,
        distance: lineDistance,
        color: "#ffffff",
        opacity: 0.4,
        width: 1
      },
      move: {
        enable: true,
        speed: moveSpeed,
        direction: "none",
        random: false,
        straight: false,
        out_mode: "out",
        bounce: false,
        attract: {
          enable: false,
          rotateX: 600,
          rotateY: 1200
        }
      }
    },
    interactivity: {
      detect_on: "canvas",
      events: {
        onhover: {
          enable: !isMobile, // 手機禁用 hover 效果
          mode: "repulse"
        },
        onclick: {
          enable: true,
          mode: "push"
        },
        resize: true
      },
      modes: {
        grab: {
          distance: 400,
          line_linked: {
            opacity: 1
          }
        },
        bubble: {
          distance: 400,
          size: 40,
          duration: 2,
          opacity: 8,
          speed: 3
        },
        repulse: {
          distance: isMobile ? 100 : 200, // 手機縮短距離
          duration: 0.4
        },
        push: {
          particles_nb: isMobile ? 2 : 4 // 手機減少新增粒子
        },
        remove: {
          particles_nb: 2
        }
      }
    },
    retina_detect: !isMobile // 手機禁用 Retina 檢測
  });

  /**
   * 性能優化: 視窗不可見時暫停動畫
   * 節省 CPU/GPU 資源,延長電池壽命
   */
  document.addEventListener("visibilitychange", function() {
    if (typeof pJSDom !== "undefined" && pJSDom.length > 0) {
      if (document.hidden) {
        // 視窗隱藏: 暫停動畫
        pJSDom[0].pJS.particles.move.enable = false;
        pJSDom[0].pJS.fn.particlesRefresh();
      } else {
        // 視窗可見: 恢復動畫
        pJSDom[0].pJS.particles.move.enable = true;
        pJSDom[0].pJS.fn.particlesRefresh();
      }
    }
  });

  /**
   * 響應式調整: 視窗大小改變時重新初始化
   */
  var resizeTimeout;
  window.addEventListener("resize", function() {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(function() {
      var newWidth = window.innerWidth;
      var shouldReinit = false;
      
      // 檢查是否跨越斷點
      if ((isMobile && newWidth >= 768) || 
          (!isMobile && isTablet && (newWidth < 768 || newWidth >= 1024)) ||
          (!isMobile && !isTablet && newWidth < 1024)) {
        shouldReinit = true;
      }
      
      if (shouldReinit && typeof pJSDom !== "undefined" && pJSDom.length > 0) {
        // 更新設備類型
        isMobile = newWidth < 768;
        isTablet = newWidth >= 768 && newWidth < 1024;
        
        // 銷毀並重新初始化
        pJSDom[0].pJS.fn.vendors.destroypJS();
        window.location.reload(); // 簡化處理,重新載入配置
      }
    }, 250); // 防抖 250ms
  });

  /**
   * 低性能模式檢測 (可選)
   * 如果檢測到性能問題,進一步降低粒子數
   */
  if (typeof performance !== "undefined" && performance.memory) {
    // 簡單的性能監控
    setTimeout(function() {
      if (typeof pJSDom !== "undefined" && pJSDom.length > 0) {
        var fps = pJSDom[0].pJS.fn.vendors.draw ? 60 : 30;
        if (fps < 30 && pJSDom[0].pJS.particles.array.length > 20) {
          // FPS 過低,減少粒子數
          console.log("Particles.js: 檢測到低性能,減少粒子數");
          pJSDom[0].pJS.particles.number.value = Math.floor(particleCount * 0.5);
          pJSDom[0].pJS.fn.particlesRefresh();
        }
      }
    }, 3000); // 3秒後檢查
  }

  /**
   * 調試信息 (生產環境可移除)
   */
  if (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1") {
    console.log("Particles.js 優化配置:");
    console.log("- 設備類型:", isMobile ? "手機" : (isTablet ? "平板" : "桌面"));
    console.log("- 粒子數量:", particleCount);
    console.log("- 移動速度:", moveSpeed);
    console.log("- 連線距離:", lineDistance);
    console.log("- Hover 效果:", !isMobile ? "啟用" : "禁用");
    console.log("- Retina 檢測:", !isMobile ? "啟用" : "禁用");
  }
})();
