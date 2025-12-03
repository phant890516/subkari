/* ==================== マウスドラッグでスライダーを動かす ==================== */
const heroSlider = document.querySelector('.hero-slider');
let isDown = false;
let startX;
let scrollLeft;

// ドラッグ開始
heroSlider.addEventListener('mousedown', (e) => {
  isDown = true;
  heroSlider.classList.add('active');
  startX = e.pageX - heroSlider.offsetLeft;
  scrollLeft = heroSlider.scrollLeft;
});

// ドラッグ終了（マウスを離したとき）
heroSlider.addEventListener('mouseup', () => {
  isDown = false;
  heroSlider.classList.remove('active');
});

// ドラッグ領域外に出たら終了
heroSlider.addEventListener('mouseleave', () => {
  isDown = false;
  heroSlider.classList.remove('active');
});

// 実際にドラッグして動かす処理
heroSlider.addEventListener('mousemove', (e) => {
  if (!isDown) return;
  e.preventDefault();
  const x = e.pageX - heroSlider.offsetLeft;
  const walk = (x - startX) * 1.5; // ← スクロールの速度（1.0〜2.0で調整）
  heroSlider.scrollLeft = scrollLeft - walk;
});

// ==================== スマホ（タッチ操作）にも対応 ====================
heroSlider.addEventListener('touchstart', (e) => {
  isDown = true;
  startX = e.touches[0].pageX - heroSlider.offsetLeft;
  scrollLeft = heroSlider.scrollLeft;
});

heroSlider.addEventListener('touchend', () => {
  isDown = false;
});

heroSlider.addEventListener('touchmove', (e) => {
  if (!isDown) return;
  const x = e.touches[0].pageX - heroSlider.offsetLeft;
  const walk = (x - startX) * 1.5;
  heroSlider.scrollLeft = scrollLeft - walk;
});
