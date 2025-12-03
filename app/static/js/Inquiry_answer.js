
        document.addEventListener('DOMContentLoaded', () => {
            const logoutLink = document.querySelector('.logout-link');
            if (logoutLink) {
                logoutLink.addEventListener('click', (e) => {
                    e.preventDefault();
                    if (confirm('ログアウトしますか？')) {
                        console.log('ログアウト処理を実行...');
                    }
                });
            }

            document.getElementById('answer-form').addEventListener('submit', function (e) {
                e.preventDefault();
                const replyContent = document.getElementById('reply-content').value;

                if (replyContent.trim() === '') {
                    alert('返信内容を入力してください。');
                    return;
                }

                if (confirm('この内容で返信を送信しますか？')) {
                    alert('返信を送信しました。');
                    console.log('返信内容:', replyContent);
                    // 実際にはサーバーへの送信処理
                    // window.location.href = 'contact_list.html';
                }
            });
        });
