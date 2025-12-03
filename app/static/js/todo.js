        // JS: 振込履歴の最初の項目をクリックしたら詳細画面に遷移する処理
        document.getElementById('transfer-item-1').addEventListener('click', (e) => {
            // aタグにhref="screen5_transfer_detail.html"が設定されているため、デフォルトの動作をキャンセルしなくても遷移する
            console.log('振込履歴（詳細）へ遷移します。');
            // e.preventDefault();
            // window.location.href = 'screen5_transfer_detail.html';
        });

        // その他の項目はコンソール出力のみ
        document.querySelectorAll('.list-item:not(#transfer-item-1)').forEach(item => {
            item.addEventListener('click', () => {
                console.log('振込履歴項目がクリックされました。');
            });
        });
