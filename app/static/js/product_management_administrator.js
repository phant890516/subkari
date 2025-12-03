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

    // 全選択/解除機能
    const selectAllHeader = document.getElementById('select-all-header');
    const rowCheckboxes = document.querySelectorAll('.results-table tbody input[type="checkbox"]');
    const selectAllButton = document.querySelector('.select-all');

    selectAllHeader.addEventListener('change', (e) => {
        rowCheckboxes.forEach(checkbox => {
            checkbox.checked = e.target.checked;
        });
        selectAllButton.textContent = e.target.checked ? '全解除' : '全選択';
    });

    selectAllButton.addEventListener('click', () => {
        const isAllChecked = Array.from(rowCheckboxes).every(cb => cb.checked);
        const newState = !isAllChecked;

        rowCheckboxes.forEach(checkbox => {
            checkbox.checked = newState;
        });
        selectAllHeader.checked = newState;
        selectAllButton.textContent = newState ? '全解除' : '全選択';
    });


    // ページネーションのダミー機能
    window.prevPage = function () {
        console.log('前のページへ移動');
        alert('前のページへ移動します');
    };
    window.nextPage = function () {
        console.log('次のページへ移動');
        alert('次のページへ移動します');
    };

    // 管理ボタンのダミー機能
    document.querySelectorAll('.icon-edit').forEach(button => {
        button.addEventListener('click', (e) => {
            const row = e.currentTarget.closest('tr');
            const productId = row.querySelector('td:nth-child(2)').textContent;
            console.log(`商品ID: ${productId} の編集画面へ遷移`);
            alert(`商品ID: ${productId} の編集画面へ遷移します`);
        });
    });

    document.querySelectorAll('.icon-delete').forEach(button => {
        button.addEventListener('click', (e) => {
            const row = e.currentTarget.closest('tr');
            const productId = row.querySelector('td:nth-child(2)').textContent;
            if (confirm(`商品ID: ${productId} を削除してもよろしいですか？`)) {
                console.log(`商品ID: ${productId} を削除`);
                alert(`商品ID: ${productId} を削除しました`);
                // 実際にはここでサーバーに削除リクエストを送る
            }
        });
    });
});
