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