        document.addEventListener('DOMContentLoaded', () => {
            // ログアウト処理の例
            const logoutLink = document.querySelector('.logout-link');
            if (logoutLink) {
                logoutLink.addEventListener('click', (e) => {
                    e.preventDefault();
                    if (confirm('ログアウトしますか？')) {
                        console.log('ログアウト処理を実行...');
                        // 実際にはログアウト処理を記述
                    }
                });
            }

            // フィルターボタンの切り替え処理
            const filterButtons = document.querySelectorAll('.filter-buttons button');
            filterButtons.forEach(button => {
                button.addEventListener('click', (e) => {
                    filterButtons.forEach(btn => btn.classList.remove('active'));
                    e.target.classList.add('active');
                    console.log('フィルター:', e.target.textContent);
                    // 実際にはここでテーブルのデータをフィルタリングする処理を記述
                });
            });
        });
