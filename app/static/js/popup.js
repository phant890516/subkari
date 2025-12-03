const popupBtn = document.getElementById('popupBtn');
const popupModal = document.getElementById('popupModal');

popupBtn.addEventListener('click', () => {
    popupModal.classList.add('show');
});

function closeModal() {
    popupModal.classList.remove('show');
}

// 背景クリックで閉じる
popupModal.addEventListener('click', (e) => {
    if (e.target === popupModal) {
        closeModal();
    }
});

// ESCキーで閉じる
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeModal();
    }
});

const popupBtnClean = document.getElementById('popupBtnClean');
const popupModalClean = document.getElementById('popupModalClean');

popupBtnClean.addEventListener('click', () => {
    popupModalClean.classList.add('show');
});

function closeModalClean() {
    popupModalClean.classList.remove('show');
}

// 背景クリックで閉じる
popupModalClean.addEventListener('click', (e) => {
    if (e.target === popupModalClean) {
        closeModalClean();
    }
});

// ESCキーで閉じる
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeModalClean();
    }
});