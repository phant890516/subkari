console.log("register_account is loaded.");
const errorMes = {
    mail: "メールを入力してください",
    password: "パスワードを入力してください",
    password_confirm: "確認用パスワードを入力してください",
};

$("#register_btn").on("click", function () {
    console.log("check");

    $(".error").remove();
    const mail = $("input[name='mail']").val();
    const password = $("input[name='password']").val();
    const password_confirm = $("input[name='password_confirm']").val();

    // email check
    if (mail === "") {
        $("input[name='mail']").after(`<div class="error" style="color: red;">${errorMes.mail}</div>`);

    }

    // password check
    if (password === "") {
        $("input[name='password']").after(`<div class="error" style="color: red;">${errorMes.password}</div>`);

    }

    // password_confirm check
    if (password_confirm === "") {
        $("input[name='password_confirm']").after(`<div class="error" style="color: red;">${errorMes.password_confirm}</div>`);

    }

});
document.addEventListener("DOMContentLoaded", () => {
    const popupOverlay = document.getElementById("popupOverlay");
    const agreePopup = document.getElementById("agreePopup");

    // ページロード時にポップアップは表示済み
    popupOverlay.style.display = "flex";

    // 同意ボタンでポップアップを閉じる
    agreePopup.addEventListener("click", () => {
        popupOverlay.style.display = "none";
    });
});


document.addEventListener("DOMContentLoaded", () => {
    const popupOverlay = document.getElementById("popupOverlay");
    const agreePopup = document.getElementById("agreePopup");
    const declinePopup = document.getElementById("declinePopup"); // 新しく同意しないボタンを取得

    // ページロード時にポップアップは表示
    popupOverlay.style.display = "flex";

    // 同意ボタンでポップアップを閉じる
    agreePopup.addEventListener("click", () => {
        popupOverlay.style.display = "none";
    });

    // 同意しないボタンでトップページへ遷移
    declinePopup.addEventListener("click", () => {
        window.location.href = "/top"; // トップページのURLに遷移
    });
});

$("#register_btn").on("click", function (event) {
    let hasError = false;

    $(".error").remove();
    const email = $("input[name='mail']").val();
    const password = $("input[name='password']").val();
    const password_confirm = $("input[name='password_confirm']").val();

    if (email === "") {
        $("input[name='mail']").after(`<div class="error" style="color: red;">メールアドレスを入力してください</div>`);
        hasError = true;
    }

    if (password === "") {
        $("input[name='password']").after(`<div class="error" style="color: red;">パスワードを入力してください</div>`);
        hasError = true;
    }

    if (password_confirm === "") {
        $("input[name='password_confirm']").after(`<div class="error" style="color: red;">確認用パスワードを入力してください</div>`);
        hasError = true;
    }

    // ❗ エラーがあればフォーム送信を止める
    if (hasError) {
        event.preventDefault();
    }
});
