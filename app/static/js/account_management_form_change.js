        document.addEventListener('DOMContentLoaded', () => {
            // ログアウト機能
            const logoutLink = document.querySelector('.logout-link');
            if (logoutLink) {
                logoutLink.addEventListener('click', (e) => {
                    e.preventDefault();
                    console.log('ログアウト処理を実行...');
                    alert('ログアウトします');
                });
            }

            // 変更を保存ボタンのダミー機能
            document.querySelector('.save-button').addEventListener('click', () => {
                console.log('アカウント詳細の変更を保存します');
                alert('アカウント詳細の変更を保存しました');
            });

            // パスワード変更フォームのダミー機能
            document.getElementById('password-change-form').addEventListener('submit', (e) => {
                e.preventDefault();
                console.log('パスワード変更処理を実行...');
                alert('パスワードを変更しました');
            });
            
            // 編集アイコンのダミー機能
            document.querySelectorAll('.edit-icon').forEach(icon => {
                icon.addEventListener('click', () => {
                    if(icon.textContent.trim() === '📝') {
                        alert('氏名フィールドの編集機能を実行します');
                        // 実際にはここでinputのreadonlyを解除するなどする
                    }
                });
            });
        });
