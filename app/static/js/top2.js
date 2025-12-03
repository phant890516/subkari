document.addEventListener('DOMContentLoaded', () => {
    const productsContainer = document.querySelector('.products-container');
    const productCards = Array.from(productsContainer.querySelectorAll('.product-card'));
    const pageLinks = document.querySelectorAll('.pagination .page-link');
    const prevBtn = document.querySelector('.pagination .prev');
    const nextBtn = document.querySelector('.pagination .next');

    const itemsPerPage = 36; // 1ページあたりの表示数
    let currentPage = 1;
    const totalPages = Math.ceil(productCards.length / itemsPerPage);

    const showPage = (page) => {
        currentPage = page;
        // 商品を全て非表示
        productCards.forEach(card => card.style.display = 'none');

        // 対応するページの商品だけ表示
        const start = (page - 1) * itemsPerPage;
        const end = start + itemsPerPage;
        productCards.slice(start, end).forEach(card => card.style.display = 'block');

        // ページ番号のアクティブ状態を更新
        pageLinks.forEach(link => link.classList.remove('active'));
        const activeLink = Array.from(pageLinks).find(link => parseInt(link.textContent) === page);
        if(activeLink) activeLink.classList.add('active');

        // prev/nextボタンの状態を更新
        prevBtn.disabled = page === 1;
        nextBtn.disabled = page === totalPages;
    };

    // ページ番号クリック
    pageLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const page = parseInt(link.textContent);
            showPage(page);
        });
    });

    // prevボタンクリック
    prevBtn.addEventListener('click', () => {
        if(currentPage > 1) showPage(currentPage - 1);
    });

    // nextボタンクリック
    nextBtn.addEventListener('click', () => {
        if(currentPage < totalPages) showPage(currentPage + 1);
    });

    // 初期表示
    showPage(1);
});
