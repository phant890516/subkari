        // JS: リスト項目がクリックされた時の処理
        document.querySelectorAll('.list-item').forEach(item => {
            item.addEventListener('click', () => {
                console.log('売上履歴項目がクリックされました。');
                // 実際は売上詳細画面へ遷移する処理
                // window.location.href = 'sales_detail.html';
            });
        });
