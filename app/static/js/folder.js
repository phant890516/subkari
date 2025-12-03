document.addEventListener('DOMContentLoaded', function() {
    const toggleBtn = document.getElementById('toggle-btn');
    const productItems = document.querySelectorAll('.product-item');
    const toggleIcon = document.getElementById('toggle-icon');
    let isExpanded = false;
   
    if (toggleBtn) {
        toggleBtn.addEventListener('click', function() {
            isExpanded = !isExpanded;
            
            productItems.forEach((item, index) => {
                if (index >= 4) {  // ５番目の商品から
                    if (isExpanded) {
                        item.classList.remove('hidden');
                    } else {
                        item.classList.add('hidden');
                    }
                }
            });
            
            // 更新按鈕文字和圖標
            if (isExpanded) {
                toggleBtn.innerHTML = `<span id="toggle-icon"><img src="/static/img/arrow_up.png" class="object-contain"></span>`;
            } else {
                toggleBtn.innerHTML = `<span id="toggle-icon"><img src="/static/img/arrow_down.png" class="object-contain"></span>`;
            }
        });
    }
});