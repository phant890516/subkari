
// 銀行のバリデーション
function validateBank() {
    const select = document.getElementById('bank');
    const error = document.getElementById('bankError');
    
    if (select.value === '') {
        select.classList.add('error');
        error.classList.add('show');
        return false;
    } else {
        select.classList.remove('error');
        error.classList.remove('show');
        return true;
    }
}

// 支店コードのバリデーション
function validateBranchCode() {
    const input = document.getElementById('branchCode');
    const error = document.getElementById('branchCodeError');
    
    // 数字のみ許可
    input.value = input.value.replace(/[^0-9]/g, '');
    
    if (input.value === '' || input.value.length !== 3) {
        input.classList.add('error');
        error.classList.add('show');
        return false;
    } else {
        input.classList.remove('error');
        error.classList.remove('show');
        return true;
    }
}

// 口座番号のバリデーション
function validateAccountNumber() {
    const input = document.getElementById('accountNumber');
    const error = document.getElementById('accountNumberError');
    
    // 数字のみ許可
    input.value = input.value.replace(/[^0-9]/g, '');
    
    if (input.value === '' || input.value.length !== 11) {
        input.classList.add('error');
        error.classList.add('show');
        return false;
    } else {
        input.classList.remove('error');
        error.classList.remove('show');
        return true;
    }
}

// 口座名義（セイ）のバリデーション
function validateAccountNameSei() {
    const input = document.getElementById('accountNameSei');
    const error = document.getElementById('accountNameSeiError');
    
    if (input.value.trim() === '') {
        input.classList.add('error');
        error.classList.add('show');
        return false;
    } else {
        input.classList.remove('error');
        error.classList.remove('show');
        return true;
    }
}

// 口座名義（メイ）のバリデーション
function validateAccountNameMei() {
    const input = document.getElementById('accountNameMei');
    const error = document.getElementById('accountNameMeiError');
    
    if (input.value.trim() === '') {
        input.classList.add('error');
        error.classList.add('show');
        return false;
    } else {
        input.classList.remove('error');
        error.classList.remove('show');
        return true;
    }
}

// フォーム送信
function handleSubmit(event) {
    // event.preventDefault();
    
    // const isBankValid = validateBank();
    // const isBranchCodeValid = validateBranchCode();
    // const isAccountNumberValid = validateAccountNumber();
    // const isAccountNameSeiValid = validateAccountNameSei();
    // const isAccountNameMeiValid = validateAccountNameMei();
    
    // if (isBankValid && isBranchCodeValid && isAccountNumberValid && 
    //     isAccountNameSeiValid && isAccountNameMeiValid) {
    //     alert('口座を登録しました');
    //     // ここで実際の登録処理を行う
    // }
}
