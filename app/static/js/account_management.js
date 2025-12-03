        document.addEventListener('DOMContentLoaded', () => {
            // ログアウト処理の例
            const logoutLink = document.querySelector('.logout-link');
            if (logoutLink) {
                logoutLink.addEventListener('click', (e) => {
                    e.preventDefault();
                    if (confirm('ログアウトしますか？')) {
                        // ログアウト処理
                        // window.location.href = 'login.html'; 
                    }
                });
            }
        });
