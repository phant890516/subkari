
let isEditing = false;

// Edit button functionality
const editButton = document.getElementById('editButton');
const deleteButtons = document.querySelectorAll('.delete-button');
const radioButtons = document.querySelectorAll('input[type="radio"]');

// editButton.addEventListener('click', function() {
//     isEditing = !isEditing;
    
//     if (isEditing) {
//         editButton.textContent = '完了する';
//         deleteButtons.forEach(button => button.classList.add('show'));
//         radioButtons.forEach(radio => radio.disabled = true);
//     } else {
//         editButton.textContent = '編集する';
//         deleteButtons.forEach(button => button.classList.remove('show'));
//         radioButtons.forEach(radio => radio.disabled = false);
//     }
// });

// Delete bank functionality
// function deleteBank(id) {
//     const bankItem = document.querySelector(`.bank-item[data-id="${id}"]`);
//     if (bankItem) {
//         bankItem.remove();
//     }
// }

// Add bank functionality
// const addBankButton = document.getElementById('addBankButton');
// const errorModal = document.getElementById('errorModal');
// const modalOkButton = document.getElementById('modalOkButton');

// addBankButton.addEventListener('click', function() {
//     const bankItems = document.querySelectorAll('.bank-item');
    
//     if (bankItems.length >= 3) {
//         errorModal.classList.add('show');
//     } else {
//         // 新しい銀行追加のロジック
//         console.log('新しい銀行を追加');
//         alert('新しい銀行登録画面へ遷移します');
//     }
// });

// Close modal
modalOkButton.addEventListener('click', function() {
    errorModal.classList.remove('show');
});

// Close modal when clicking outside
errorModal.addEventListener('click', function(e) {
    if (e.target === errorModal) {
        errorModal.classList.remove('show');
    }
});