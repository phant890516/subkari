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
        });
        
        // 対応完了ボタンのダミー機能
        function completeReport() {
            const memoContent = document.getElementById('memo').value;
            console.log(`通報ID 44 の対応を完了します。メモ: ${memoContent}`);
            alert('通報対応を完了しました。');
            // 実際にはここでデータをサーバーに送信し、ページ遷移または更新を行います。
        }

