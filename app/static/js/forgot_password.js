document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector(".forgot-password__form-group");
    const email = document.getElementById("email");
    const errorMessage = document.getElementById("js-error");

    form.addEventListener("submit", function(e) {
        // 前のメッセージ消す
        errorMessage.textContent = "";

        // 空欄チェック
        if (!email.value.trim()) {
            e.preventDefault();
            errorMessage.textContent = "メールアドレスを入力してください。";
            return;
        }
    });
});
