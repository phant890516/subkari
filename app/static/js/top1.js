// ===============================
// Hero Slider（フェード切り替え）
// ===============================
const slides = document.querySelectorAll('.hero-slide-item');
let currentIndex = 0;
let slideInterval;

// 初期スタイル設定
slides.forEach((slide, i) => {
    slide.style.position = 'absolute';
    slide.style.top = 0;
    slide.style.left = 0;
    slide.style.width = '100%';
    slide.style.height = '100%';
    slide.style.backgroundSize = 'cover';
    slide.style.backgroundPosition = 'center';
    slide.style.opacity = i === 0 ? 1 : 0;
    slide.style.transition = 'opacity 1s ease';
});

// スライドを切り替える関数
function showSlide(index) {
    slides.forEach((slide, i) => {
        slide.style.opacity = i === index ? 1 : 0;
    });
    currentIndex = index;
}

// 次のスライド
function nextSlide() {
    let nextIndex = (currentIndex + 1) % slides.length;
    showSlide(nextIndex);
}

// 前のスライド
function previousSlide() {
    let prevIndex = (currentIndex - 1 + slides.length) % slides.length;
    showSlide(prevIndex);
}

// 自動スライド
function startAutoSlide() {
    slideInterval = setInterval(nextSlide, 5000);
}

// 停止して再スタート（矢印操作用）
function resetAutoSlide() {
    clearInterval(slideInterval);
    startAutoSlide();
}

// 矢印にイベントを追加
document.querySelector('.slider-arrows .slider-arrow:first-child').addEventListener('click', () => {
    previousSlide();
    resetAutoSlide();
});
document.querySelector('.slider-arrows .slider-arrow:last-child').addEventListener('click', () => {
    nextSlide();
    resetAutoSlide();
});

// 自動スライド開始
startAutoSlide();
