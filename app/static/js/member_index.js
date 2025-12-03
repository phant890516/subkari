
$('.center').slick({
    infinite: true,
    centerMode: true,          // 中央モードON
    centerPadding: '50px',     // 左右が少し見切れ、約4枚に見えるように調整
    slidesToShow: 4,           // 表示枚数を4枚に設定
    slidesToScroll: 1,
    dots: false,
    arrows: true,              // 矢印を表示
    autoplay: true,
    autoplaySpeed: 3000,
    speed: 500,
    responsive: [
        {
            breakpoint: 1024,
            settings: { slidesToShow: 3, centerPadding: '40px' } // 中画面
        },
        {
            breakpoint: 768,
            settings: { slidesToShow: 2, arrows: false, centerPadding: '30px' } // 小画面 (矢印非表示)
        },
        {
            breakpoint: 480,
            settings: { slidesToShow: 1, arrows: false, centerPadding: '20px' } // スマホ (矢印非表示)
        }
    ]
});
