
// カード番号の自動フォーマット
document.getElementById('cardNumber').addEventListener('input', function(e) {
    let value = e.target.value.replace(/\s/g, '');
    let formattedValue = value.match(/.{1,4}/g)?.join(' ') || value;
    e.target.value = formattedValue;
});

// 有効期限の自動フォーマット
document.getElementById('cardExpiry').addEventListener('input', function(e) {
    let value = e.target.value.replace(/\D/g, '');
    if (value.length >= 2) {
        value = value.slice(0, 2) + '/' + value.slice(2, 4);
    }
    e.target.value = value;
});

// セキュリティコードは数字のみ
document.getElementById('securityCode').addEventListener('input', function(e) {
    e.target.value = e.target.value.replace(/\D/g, '');
});

function openSecurityHelp() {
    document.getElementById('securityHelpModal').classList.add('active');
}

function closeSecurityHelp() {
    document.getElementById('securityHelpModal').classList.remove('active');
}

function registerCard(e) {
    e.preventDefault();
    const cardNumber = document.getElementById('cardNumber').value;
    const cardExpiry = document.getElementById('cardExpiry').value;
    const securityCode = document.getElementById('securityCode').value;

    if (!cardNumber || !cardExpiry || !securityCode) {
        alert('すべての項目を入力してください');
        return;
    }

    alert('クレジットカードが登録されました');
    
    // フォームをリセット
    document.getElementById('cardNumber').value = '';
    document.getElementById('cardExpiry').value = '';
    document.getElementById('securityCode').value = '';
}

// モーダル外クリックで閉じる
document.getElementById('securityHelpModal').addEventListener('click', function(e) {
    if (e.target === this) {
        closeSecurityHelp();
    }
});