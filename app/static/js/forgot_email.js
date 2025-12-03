document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("forgotEmailForm");
  const phoneInput = document.getElementById("phone");
  const errorMessage = document.getElementById("error-message");

  const correctPhone = "09012345678";

  // --- 入力中の処理（数字以外禁止・11桁制限） ---
  phoneInput.addEventListener("input", () => {
    let value = phoneInput.value;

    // 数字以外は削除
    value = value.replace(/[^0-9]/g, "");

    // 11桁以上は入力させない
    if (value.length > 11) {
      value = value.slice(0, 11);
    }

    phoneInput.value = value;

    // 入力中はエラー非表示
    errorMessage.textContent = "";
  });

  // --- 送信時バリデーション ---
  form.addEventListener("submit", (e) => {
    const phone = phoneInput.value.trim();
    errorMessage.style.color = "red";
    errorMessage.textContent = "";

    // 未入力
    if (phone === "") {
      e.preventDefault();
      errorMessage.textContent = "電話番号を入力してください";
      return;
    }

    // 桁数チェック
    if (phone.length < 10 || phone.length > 11) {
      e.preventDefault();
      errorMessage.textContent = "電話番号は10〜11桁で入力してください";
      return;
    }

    // 電話番号不一致
    if (phone !== correctPhone) {
      e.preventDefault();
      errorMessage.textContent = "電話番号が違います";
      return;
    }

    // 正しい場合 → preventDefaultしないのでそのまま画面遷移
  });
});
