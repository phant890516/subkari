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

    // 全選択/全解除のトグル機能
    const checkAll = document.getElementById('check-all');
    const checkboxes = document.querySelectorAll('.data-table tbody input[type="checkbox"]');

    checkAll.addEventListener('change', () => {
        checkboxes.forEach(checkbox => {
            checkbox.checked = checkAll.checked;
        });
    });

    document.querySelector('.select-all-link').addEventListener('click', (e) => {
        checkAll.checked = !checkAll.checked;
        checkAll.dispatchEvent(new Event('change'));
    });

    // 管理ボタンのプレースホルダー処理
    document.querySelectorAll('.management-actions button').forEach(button => {
        button.addEventListener('click', (e) => {
            const action = button.title;
            const row = button.closest('tr');
            const userId = row.cells[1].textContent;
            alert(`${action} (ID: ${userId}) を実行します。`);
        });
    });
});
