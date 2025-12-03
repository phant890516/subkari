
// パスワードのバリデーション
function validatePassword() {
    const input = document.getElementById('password');
    const error = document.getElementById('passwordError');
    
    if (input.value.trim() === '') {
        input.classList.add('error');
        error.classList.add('show');
        return false;
    } else {
        input.classList.remove('error');
        error.classList.remove('show');
        return true;
    }
}

// フォーム送信
function handleSubmit(event) {
    event.preventDefault();
    
    const isPasswordValid = validatePassword();
    
    if (isPasswordValid) {
        // パスワード確認処理
        const password = document.getElementById('password').value;
        
        // ここで実際のパスワード確認処理を行う
        console.log('パスワード確認中...');
        
        // 確認後、次のページへ遷移
        // window.location.href = '/next-page';
    }
}

// Enterキーでの送信を有効化
document.getElementById('password').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        handleSubmit(event);
    }
});