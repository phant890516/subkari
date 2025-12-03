// メール再送リクエスト用login1
document.addEventListener("DOMContentLoaded", () => {
  const resendBtn = document.getElementById("resendBtn");
  if (resendBtn) {
    resendBtn.addEventListener("click", () => {
      alert("再送リクエストを送信しました。");
    });
  }
});

// ---------- 共通部は既にある前提 ----------
// ここは login 用のイベント処理（script.js に追記）login2
document.addEventListener('DOMContentLoaded', () => {
  // login form submit handler
  const loginForm = document.getElementById('loginForm');
  if (loginForm) {
    loginForm.addEventListener('submit', function (e) {
      e.preventDefault();
      const email = document.getElementById('email')?.value.trim();
      const password = document.getElementById('password')?.value;

      if (email && password) {
        alert('ログインしました');
        // 実際のログイン処理をここに置く（API呼び出しなど）
        // window.location.href = 'home.html';
      } else {
        alert('メールアドレスとパスワードを入力してください。');
      }
    });
  }
});

// -----------------------------
// メールアドレス忘れた方ページlogin3
// -----------------------------
document.addEventListener('DOMContentLoaded', () => {
  const forgotForm = document.getElementById('forgotEmailForm');
  if (forgotForm) {
    forgotForm.addEventListener('submit', function (e) {
      e.preventDefault();
      const phone = document.getElementById('phone')?.value.trim();

      if (phone && phone.length >= 10 && phone.length <= 11) {
        alert('登録された電話番号にメールアドレスをSMSで送信しました。');
        window.location.href = 'email-sent.html';
      } else {
        alert('正しい電話番号を入力してください。');
      }
    });
  }
});

// login4 - 登録 (メールアドレス・パスワード)
function handleRegister(event) {
    event.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirm = document.getElementById('password-confirm').value;

    if (password !== confirm) {
        alert('パスワードが一致しません。');
        return false;
    }

    if (password.length < 8) {
        alert('パスワードは8文字以上で入力してください。');
        return false;
    }

    alert('確認メールを送信しました。');
    // window.location.href = 'register-form.html';
    return false;
}

// 登録フォーム (個人情報) 送信処理
function handleRegisterForm(event) {
  event.preventDefault();

  const phone = document.getElementById('phone').value.trim();
  const postal = document.getElementById('postal').value.trim();
  const birthday = document.getElementById('birthday').value;
  // ★修正箇所: HTMLのクラス名に合わせて .rfo-prefecture-selected に変更
  const selectedPrefecture = document.querySelector('.rfo-prefecture-selected').textContent;

  if (phone.length < 10 || phone.length > 11) {
    alert('電話番号は10桁または11桁で入力してください。');
    return false;
  }

  if (postal.length !== 7) {
    alert('郵便番号は7桁で入力してください。');
    return false;
  }

  if (!birthday) {
    alert('生年月日を選択してください。');
    return false;
  }

  if (selectedPrefecture === '選択してください') {
    alert('都道府県を選択してください。');
    return false;
  }

  alert('会員登録が完了しました。');
  window.location.href = 'registration-complete.html';
  return false;
}

// 郵便番号から住所自動入力（簡易版）
document.getElementById('postal')?.addEventListener('blur', function() {
  const postal = this.value;
  if (postal.length === 7) {
    console.log('郵便番号から住所を検索: ' + postal);
  }
});


// ★カスタムセレクト動作 (rfo- プレフィックスを使用しているため、このブロックのみ残す)
document.addEventListener('DOMContentLoaded', function() {
    const prefectureFrame = document.getElementById('prefectureFrame');
    if (!prefectureFrame) return; // 要素がない場合は何もしない

    const selectedDiv = prefectureFrame.querySelector('.rfo-prefecture-selected');
    const optionsList = prefectureFrame.querySelector('.rfo-prefecture-options');
    const options = optionsList.querySelectorAll('li');

    // 1. フレームをクリックしたらリストの表示/非表示を切り替える
    prefectureFrame.addEventListener('click', function(e) {
        // クリックがリスト内の要素でない場合、リストの表示を切り替える
        if (e.target.closest('.rfo-prefecture-options') === null) {
            optionsList.style.display = optionsList.style.display === 'block' ? 'none' : 'block';
        }
    });

    // 2. リストの項目をクリックしたときの処理
    options.forEach(option => {
        option.addEventListener('click', function() {
            // 選択された値を表示部に反映させる
            selectedDiv.textContent = this.textContent;
            
            // リストを非表示にする
            optionsList.style.display = 'none';
        });
    });

    // 3. 画面のどこかをクリックしたらリストを閉じる（UX向上）
    document.addEventListener('click', function(e) {
        if (!prefectureFrame.contains(e.target)) {
            optionsList.style.display = 'none';
        }
    });
});


document.addEventListener('DOMContentLoaded', () => {
    const sentMessage = document.getElementById('sentMessage');
    const urlParams = new URLSearchParams(window.location.search);
    const purpose = urlParams.get('purpose');

    // パスワード再設定からの遷移の場合、メッセージを切り替える
    if (purpose === 'reset' && sentMessage) {
        sentMessage.innerHTML = `
            ご登録いただいたメールアドレス宛に、パスワード再設定用のURLを送信しました。
            <br>メールをご確認のうえ、本文中のURLからパスワードを再設定してください。
        `;
    }
});

document.addEventListener('DOMContentLoaded', () => {
    const inputs = document.querySelectorAll('.code-input');
    const verifyButton = document.getElementById('verify-button');

    // 1. 自動フォーカス移動と入力制御
    inputs.forEach((input, index) => {
        // 入力時の処理
        input.addEventListener('input', (e) => {
            // 数字以外を削除
            input.value = input.value.replace(/[^0-9]/g, '');

            // 1文字入力したら次のフィールドへ移動
            if (input.value.length === 1 && index < inputs.length - 1) {
                inputs[index + 1].focus();
            }
            checkInputs();
        });

        // キーダウン時の処理（Backspaceで前のフィールドへ戻る）
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Backspace' && input.value === '' && index > 0) {
                inputs[index - 1].focus();
            }
        });
    });

    // 2. 「認証する」ボタンの活性化チェック
    function checkInputs() {
        let allFilled = true;
        inputs.forEach(input => {
            if (input.value.length !== 1) {
                allFilled = false;
            }
        });

        // 全て入力されたらボタンを活性化（今回は常に活性化されている画像デザインを優先）
        // 画像では常に活性化状態に見えるため、ここではボタンのアクションを追加するのみに留めます。
        
        // if (allFilled) {
        //     verifyButton.disabled = false;
        //     verifyButton.style.opacity = 1;
        // } else {
        //     verifyButton.disabled = true;
        //     verifyButton.style.opacity = 0.6;
        // }
    }

    // 3. ボタンクリック時の動作（デモンストレーション）
    verifyButton.addEventListener('click', () => {
        const code = Array.from(inputs).map(input => input.value).join('');
        if (code.length === 6) {
            alert(`認証コード: ${code} で認証します。`);
            // ここに実際の認証APIコールを記述します。
        } else {
            alert('6桁の認証コードを入力してください。');
        }
    });

    const resendButton = document.getElementById('resend-button');
    resendButton.addEventListener('click', () => {
        alert('再送リクエストを送信しました。');
        // ここに再送リクエストAPIコールとタイマー処理を記述します。
    });

    // 初期状態でカーソルを最初の入力フィールドに置く
    if (inputs.length > 0) {
        inputs[0].focus();
    }
});

// ログイン画面へ戻る
function goToLogin() {
    window.location.href = "login.html"; // ログイン画面のURLに変更してください
}

// 再送リクエストを送信
function resendRequest() {
    window.location.href = "resend_request.html"; // 再送リクエスト画面のURLに変更してください
}

// 新規アカウント作成
function createNewAccount() {
    window.location.href = "new_account.html"; // 新規アカウント作成画面のURLに変更してください
}
