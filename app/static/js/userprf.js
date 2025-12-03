function toggleDropdown() {
    const dropdown = document.getElementById('dropdownMenu');
    dropdown.classList.toggle('show');
}

// ドロップダウン外をクリックしたら閉じる
window.onclick = function(event) {
    if (!event.target.matches('.menu-btn')) {
        const dropdowns = document.getElementsByClassName("dropdown-content");
        for (let i = 0; i < dropdowns.length; i++) {
            const openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}

// プロフィールの続きを表示/非表示
function toggleDescription(event) {
    event.preventDefault();
    const moreText = document.getElementById('moreText');
    const showMoreBtn = document.getElementById('showMoreBtn');
    const showLessBtn = document.getElementById('showLessBtn');
    
    if (moreText.style.display === 'none') {
        moreText.style.display = 'inline';
        showMoreBtn.style.display = 'none';
        showLessBtn.style.display = 'inline-block';
    } else {
        moreText.style.display = 'none';
        showMoreBtn.style.display = 'inline-block';
        showLessBtn.style.display = 'none';
    }
}




// ===== ブロック・報告ポップアップ機能 =====
const modal = document.getElementById("modalOverlay");
const modalTitle = document.getElementById("modalTitle");
const modalMessage = document.getElementById("modalMessage");
const cancelBtn = document.getElementById("cancelBtn");
const confirmBtn = document.getElementById("confirmBtn");

document.querySelectorAll(".dropdown-item").forEach(item => {
    item.addEventListener("click", (e) => {
        const text = e.target.textContent;

        if (text.includes("ブロック")) {
            showModal("ブロックしますか？", 
                      "ブロックすると、あなたをフォローすることや、あなたの出品商品に購入・コメント・いいね！などができなくなります。");
            confirmBtn.textContent = "ブロック";
            confirmBtn.style.backgroundColor = "#e74c3c";
        } 
        else if (text.includes("報告")) {
            showModal("報告しますか？","報告内容を確認し、必要に応じて対応いたします。誤った報告はお控えください。");
            confirmBtn.textContent = "報告";
            confirmBtn.style.backgroundColor = "#f39c12";
        }
    });
});

function showModal(title, message) {
    modalTitle.textContent = title;
    modalMessage.textContent = message;
    modal.style.display = "flex";
}

// モーダル閉じる処理
cancelBtn.addEventListener("click", () => modal.style.display = "none");
modal.addEventListener("click", (e) => {
    if (e.target === modal) modal.style.display = "none";
});

// 実行ボタン（仮）
confirmBtn.addEventListener("click", () => {
    // alert(confirmBtn.textContent + "を実行しました。");
    modal.style.display = "none";
});
