// ========== スライド制御 ==========

let currentSlide = 0;
const slideContainer = document.querySelector('.hero-slide');
const slides = document.querySelectorAll('.hero-slide-item');
const totalSlides = slides.length;

// 1スライドあたりの幅（4枚同時表示）
const slideWidth = 100 / 4;

// スライド表示
function showSlide(index) {
  slideContainer.style.transition = 'transform 0.8s ease';
  slideContainer.style.transform = `translateX(-${index * slideWidth}%)`;
}

// 次へ
function nextSlide() {
  currentSlide++;
  if (currentSlide > totalSlides - 4) {
    currentSlide = 0;
  }
  showSlide(currentSlide);
}

// 前へ
function previousSlide() {
  currentSlide--;
  if (currentSlide < 0) {
    currentSlide = totalSlides - 4;
  }
  showSlide(currentSlide);
}

// 自動スライド
let autoSlide = setInterval(nextSlide, 4000);

// hero要素が存在する場合のみイベント付与
const hero = document.querySelector('.hero');
if (hero) {
  hero.addEventListener('mouseenter', () => clearInterval(autoSlide));
  hero.addEventListener('mouseleave', () => {
    autoSlide = setInterval(nextSlide, 4000);
  });
}


