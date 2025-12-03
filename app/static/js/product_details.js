// let currentImageIndex = 0;
//         const images = [
//             'https://via.placeholder.com/500x600/333/fff?text=Fur+Parker+1',
//             'https://via.placeholder.com/500x600/444/fff?text=Fur+Parker+2',
//             'https://via.placeholder.com/500x600/555/fff?text=Fur+Parker+3'
//         ];
        
//         function changeImage(direction) {
//             currentImageIndex += direction;
//             if (currentImageIndex < 0) currentImageIndex = images.length - 1;
//             if (currentImageIndex >= images.length) currentImageIndex = 0;
            
//             document.getElementById('mainImage').src = images[currentImageIndex];
//             updateThumbnails();
//         }

//         function selectImage(index) {
//             currentImageIndex = index;
//             document.getElementById('mainImage').src = images[currentImageIndex];
//             updateThumbnails();
//         }

        function updateThumbnails() {
            const thumbnails = document.querySelectorAll('.thumbnail');
            thumbnails.forEach((thumb, index) => {
                thumb.classList.toggle('active', index === currentImageIndex);
            });
        }

        function switchTab(tabIndex) {
            const tabs = document.querySelectorAll('.tab');
            const contents = document.querySelectorAll('.tab-content');
            
            tabs.forEach((tab, index) => {
                tab.classList.toggle('active', index === tabIndex);
            });
            
            contents.forEach((content, index) => {
                content.classList.toggle('active', index === tabIndex);
            });
        }

let currentImageIndex = 0;
let allImages = [];

// 初期化
document.addEventListener('DOMContentLoaded', function() {
    // 
    allImages = document.querySelectorAll('.thumbnail');
    if (allImages.length > 0) {
        selectImage(allImages[0]);
    }
});

// 
function selectImage(thumbnailElement) {
    // 
    allImages.forEach(img => img.classList.remove('active'));
    
    // 
    thumbnailElement.classList.add('active');
    
    // 更新
    const mainImage = document.getElementById('mainImage');
    mainImage.src = thumbnailElement.src;
    
    // 更新
    currentImageIndex = Array.from(allImages).indexOf(thumbnailElement);
}

// 
function changeImage(direction) {
    if (allImages.length === 0) return;
    
    currentImageIndex += direction;
    
    // 
    if (currentImageIndex < 0) {
        currentImageIndex = allImages.length - 1;
    } else if (currentImageIndex >= allImages.length) {
        currentImageIndex = 0;
    }
    
    selectImage(allImages[currentImageIndex]);
}
