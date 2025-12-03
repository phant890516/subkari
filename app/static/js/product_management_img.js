const imageColors = ['#333333', '#888888', '#b3e0e5', '#ff9999', '#99ff99']; // ダミー画像の色（画像代わり）
let currentIndex = 0;

const mainImage = document.getElementById('main-product-image');
const thumbnailList = document.getElementById('thumbnail-list');

// サムネイルの初期生成
function createThumbnails() {
    thumbnailList.innerHTML = ''; // リストをクリア
    imageColors.forEach((color, index) => {
        const thumb = document.createElement('div');
        thumb.className = 'thumbnail';
        // ダミーとして色を背景に設定
        thumb.style.backgroundColor = color;
        thumb.textContent = `Image ${index + 1}`; // インデックスを表示
        thumb.setAttribute('data-index', index);

        // クリックイベントの追加
        thumb.addEventListener('click', () => {
            showImage(index);
        });

        if (index === currentIndex) {
            thumb.classList.add('active');
        }

        thumbnailList.appendChild(thumb);
    });
    // 最初の画像を表示
    mainImage.style.backgroundColor = imageColors[currentIndex];
}

// メイン画像とアクティブなサムネイルを更新する関数
function showImage(index) {
    // インデックスの境界チェック
    if (index < 0) {
        index = imageColors.length - 1; // 最後の画像へループ
    } else if (index >= imageColors.length) {
        index = 0; // 最初の画像へループ
    }

    currentIndex = index;

    // メイン画像の更新 (ここでは背景色を変更)
    mainImage.style.backgroundColor = imageColors[currentIndex];

    // サムネイルのアクティブ状態を更新
    document.querySelectorAll('.thumbnail').forEach((thumb, i) => {
        thumb.classList.remove('active');
        if (i === currentIndex) {
            thumb.classList.add('active');
        }
    });
}

// 矢印ボタンで画像を切り替える関数 (グローバルスコープ)
window.changeImage = function (direction) {
    showImage(currentIndex + direction);
};

// 初期ロード時にサムネイルを生成
createThumbnails();

// その他のダミー機能（変更なし）
document.addEventListener('DOMContentLoaded', () => {
    const logoutLink = document.querySelector('.logout-link');
    if (logoutLink) {
        logoutLink.addEventListener('click', (e) => {
            e.preventDefault();
            console.log('ログアウト処理を実行...');
            alert('ログアウトします');
        });
    }
});
