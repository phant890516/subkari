document.addEventListener('DOMContentLoaded', () => {
    const logoutLink = document.querySelector('.logout-link');
    if (logoutLink) {
        logoutLink.addEventListener('click', (e) => {
            e.preventDefault();
            console.log('ログアウト処理を実行...');
            // 実際にはログアウト処理を記述
        });
    }
});
