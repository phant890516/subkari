        document.addEventListener('DOMContentLoaded', () => {
            // サイドバーのナビゲーションメニューのトグル機能（変更なし）
            const sidebarLinks = document.querySelectorAll('.sidebar-nav a');
            sidebarLinks.forEach(link => {
                link.addEventListener('click', (e) => {
                    // ログ閲覧のページなので、ここではナビゲーションは行わず、activeクラスを切り替えるだけ
                    sidebarLinks.forEach(l => l.parentElement.classList.remove('active-manual'));
                    // e.currentTarget.parentElement.classList.add('active-manual');
                });
            });

            // ログアウト機能（変更なし）
            const logoutLink = document.querySelector('.logout-link');
            if (logoutLink) {
                logoutLink.addEventListener('click', (e) => {
                    e.preventDefault();
                    console.log('ログアウト処理を実行...');
                    alert('ログアウトします');
                });
            }

            // 検索・クリアボタンのダミー機能（変更なし）
            document.querySelector('.search-button').addEventListener('click', () => {
                alert('検索を実行します');
            });

            document.querySelector('.clear-button').addEventListener('click', () => {
                alert('検索条件をクリアします');
            });
        });
