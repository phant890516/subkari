
document.addEventListener("DOMContentLoaded", () => {
const navItems = document.querySelectorAll(".nav-item");
const sections = document.querySelectorAll("main > section:not(.nav):not(.profile-card)");

// テキストとsection IDの対応表
const sectionMap = {
    "プロフィール": "profile",
    "やることリスト": "todo",
    "いいね一覧": "likes",
    "フォローリスト": "follow-list",
    "出品した商品": "listed-items",
    "レンタル・購入した商品": "purchased-items",
    "下書き一覧": "drafts",
    "セラーデータセンター": "seller-center",
    "お支払い方法": "payment",
    "個人情報設定": "privacy",
    "お知らせ・機能設定": "notifications",
    "振込申請": "transfer-request",
    "履歴": "history",
    "問い合わせ": "contact",
    "FAQ": "faq",
    "ヘルプセンター": "help-center",
    "利用規約": "terms",
    "プライバシーポリシー": "policy",
    "ログアウト": "logout",
    "アカウント削除": "delete-account"
};

// クリックイベントを設定
navItems.forEach(item => {
    item.addEventListener("click", () => {
    // active状態のリセット
    navItems.forEach(i => i.classList.remove("active"));
    item.classList.add("active");

    // 全section非表示
    sections.forEach(sec => sec.classList.remove("active"));

    // 対応するsectionを表示
    const id = sectionMap[item.textContent.trim()];
    if (id) {
        const target = document.getElementById(id);
        if (target) target.classList.add("active");
    }
    });
});

// 初期状態：プロフィールを表示
document.querySelector(".nav-item").classList.add("active");
document.getElementById("profile").classList.add("active");
});
