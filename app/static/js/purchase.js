
// let selectedPaymentMethod = 'card1';

// let selectedAddress = 'address1';
// let cardToDelete = null;
// let addressToDelete = null;





// Pythonから渡された全ての住所データをJSON形式でJSの配列に格納
    //: tojson と safe フィルタに加えて、default('[]') を追加
    // 目的: 
    // 1. |tojson: PythonオブジェクトをJSON形式に変換
    // 2. |default('[]'): address_listがNoneやUndefinedの場合、空の配列 [] を代入してJSの構文エラーを防ぐ
    // 3. |safe: Jinja2がJSON文字列をエスケープしないようにし、JSで正しくパースできるようにする
    // const addressDataList = {{ address_list | tojson | default('[]') }};

    // 【代替案】: address_list が None の場合に先にデフォルト値を設定し、その後で tojson を適用する
    // const addressDataList = {{ address_list | default([]) | tojson | safe }};
    // // 現在選択されている住所のインデックス（0, 1, 2, ...）を保持
    // // 初期値として、最初の住所（0番目）を選択状態とします。
    // let selectedAddressIndex = 0; 
    
    // // ページロード時: 住所リストが存在すれば、初期表示（0番目の住所）をメイン画面に反映
    // document.addEventListener('DOMContentLoaded', () => {
    //     if (addressDataList.length > 0) {
    //         updateShippingInfo(selectedAddressIndex);
    //     }
    // });

console.log(addressDataList);
console.log(cardInfoList);


/**
 * 隠しフォームフィールドを現在の選択状態に合わせて更新する
 */
function updateHiddenFormFields() {
    // 1. 支払い方法 (ID: hidden_payment_method)
    // selectedPaymentMethod は 'card-ID', 'conveni', 'paypay' の形式
    const paymentMethodInput = document.getElementById('hidden_payment_method');
    const creditcardsIdInput = document.getElementById('hidden_creditcards_id');


    if (paymentMethodInput) {
        // 支払い方法は 'card-ID' 形式のまま渡します
        if(selectedPaymentMethod.startsWith('card') && creditcardsIdInput){
            // 'card-ID' 形式から ID 部分を抽出して hidden_creditcards_id にセット
            const cardId = selectedPaymentMethod.substring(4); // 'card' の後ろの部分を取得
            creditcardsIdInput.value = cardId;
            paymentMethodInput.value = 'クレジットカード';
        } else if (selectedPaymentMethod === 'conveni') {
            paymentMethodInput.value = 'コンビニ支払い';
        } else if (selectedPaymentMethod === 'paypay') {
            paymentMethodInput.value = 'PayPay';
        } else {
            // エラー処理: 未知の支払い方法
            console.error('未知の支払い方法が選択されました:', selectedPaymentMethod);
        }
    }

    // 2. 配送先住所 ID (ID: hidden_address_index)
    // 修正: selectedAddressIndex ではなく selectedAddressId を使う
    const addressIdInput = document.getElementById('hidden_address_index'); // フォーム名が index のままであればそのまま使用
    if (addressIdInput) {
        addressIdInput.value = selectedAddressId; 
    }

    // 3. 置き配の指定 (ID: hidden_delivery_location) は変更なし
    const deliveryLocationInput = document.getElementById('hidden_delivery_location');
    if (deliveryLocationInput) {
        deliveryLocationInput.value = selectedDeliveryLocation;
    }
}





// /**
//  * 選択された住所のインデックスに基づいて、メイン画面の配送先情報を更新する
//  * @param {number} index - 選択された住所データの配列インデックス (0, 1, 2, ...)
//  */

// function updateShippingInfo(index) {
//     const shippingInfoElement = document.getElementById('selectedAddress');
    
//     // インデックスが有効で、データが存在することを確認
//     if (index >= 0 && index < addressDataList.length) {
//         const selectedAddr = addressDataList[index];
        
//         // HTML文字列を生成
//         let htmlContent = `
//             〒${selectedAddr.zip}<br>
//             ${selectedAddr.pref} ${selectedAddr.address1} ${selectedAddr.address2}<br>
//         `;
        
//         // address3 が存在する場合のみ追加
//         if (selectedAddr.address3) {
//             htmlContent += `${selectedAddr.address3}`;
//         }
        
//         // メイン画面の内容を更新
//         shippingInfoElement.innerHTML = htmlContent;

//         // グローバル変数に新しいインデックスを保存
//         selectedAddressIndex = index;

//     } else if (addressDataList.length === 0) {
//         // 住所データが一つもない場合の表示
//          shippingInfoElement.innerHTML = '<p>配送先の住所が登録されていません。「変更する」ボタンから登録してください。</p>';
//     }
// }





/**
 * 選択された住所のIDに基づいて、メイン画面の配送先情報を更新する
 * @param {string|number} addressId - 選択された住所のID (例: 'address-101')
 */

function updateShippingInfo(addressId) {
    const shippingInfoElement = document.getElementById('selectedAddress');
    let htmlContent = '';

    // 1. IDからDB ID (数値) を抽出
    // console.log('ADDRESSID',addressId);
    let dbId;
    if (typeof addressId === 'string' && addressId.includes('-')) {
        // 'address-1' の形式から抽出
        dbId = parseInt(addressId.split('-')[1]);
    } else {
        // 直接数値
        dbId = parseInt(addressId);
    }
    
    // console.log('DB ID:', dbId);
    // console.log('ADDRESS LIST:', addressDataList);
    // const dbId = parseInt(addressId);
    // console.log(dbId); 
    // 2. 配列内を検索して住所オブジェクトを見つける
    // console.log('ADDRESSLIST',addressDataList);
    const selectedAddr = addressDataList.find(addr => addr.id === dbId); // ★ find メソッドで ID を検索
    
    // インデックスが有効で、データが存在することを確認
    if (selectedAddr) {
        
        // HTML文字列を生成
        let htmlContent = `<div>
            <div class="zip">〒${selectedAddr.zip}</div>
            <div class="address">${selectedAddr.pref} ${selectedAddr.address1} ${selectedAddr.address2}</div>
            `;
        
        // address3 が存在する場合のみ追加
        if (selectedAddr.address3) {
            htmlContent += `<div>${selectedAddr.address3}</div>`;
        }
        htmlContent += `</div>`;
        selectedAddressId = dbId; // グローバル変数に新しい住所IDを保存
        // メイン画面の内容を更新
        shippingInfoElement.innerHTML = htmlContent;

        // console.log("selectedAddr選択された");
        // console.log(selectedAddr);
        

    } else if (addressDataList.length === 0) {
        // 住所データが一つもない場合の表示
         shippingInfoElement.innerHTML = '<p>配送先の住所が登録されていません。「変更する」ボタンから登録してください。</p>';
    }
    else {
        // IDが不正、または見つからなかったがリストは空ではない場合のフォールバック
        htmlContent = '<p>エラー: 選択された住所情報が見つかりませんでした。</p>';
        console.error(`住所ID ${dbId} はリストに見つかりませんでした。`);
    }
    // メイン画面の要素を更新
}







function openPaymentModal(event) {
    event.preventDefault();
    document.getElementById('paymentModal').classList.add('active');
}

function closePaymentModal() {
    document.getElementById('paymentModal').classList.remove('active');
}

function editPaymentMethods(event) {
    event.preventDefault();
    document.getElementById('paymentModal').classList.remove('active');
    document.getElementById('paymentEditModal').classList.add('active');
}

function closePaymentEditModal() {
    document.getElementById('paymentEditModal').classList.remove('active');
}

function completePaymentEdit(event) {
    event.preventDefault();
    closePaymentEditModal();
    document.getElementById('paymentModal').classList.add('active');
}

function selectPayment(method) {
     selectedPaymentMethod = method;

     // paymentModalとpaymentEditModalの両方のラジオボタンの状態を同期させる
     //原因はここ
    // document.querySelectorAll('#paymentModal .radio-btn, #paymentEditModal .radio-btn').forEach(btn => {
    // btn.classList.remove('selected');

    // ラジオボタンの選択状態を切り替える (既存のロジック)
    document.querySelectorAll('[id^="radio-card"], [id^="radio-edit-card"]').forEach(btn => {
        btn.classList.remove('selected');

    });
    if (methodId.startsWith('card')) {
        // インデックスの抽出を 'card' の直後から行う
        const indexStr = methodId.substring(4); // 'card' (4文字) の後の文字列を取得
        const cardId = parseInt(indexStr);
        //cardIdに対応するデータが何番目かを特定する
        // let methodindex = cardInfoList.findIndex(c => c.id === cardId);
        // console.log("methodindex",methodindex);

        const radioBtn = document.getElementById('radio' + cardId);
        const editRadioBtn = document.getElementById('radio-edit' + cardId);

        if (radioBtn) radioBtn.classList.add('selected');
        if (editRadioBtn) editRadioBtn.classList.add('selected');
    }else if (method === 'conveni' || method === 'paypay') {
        const radioBtn = document.getElementById('radio-' + method);
        const editRadioBtn = document.getElementById('radio-edit-' + method);

        if (radioBtn) radioBtn.classList.add('selected');
        if (editRadioBtn) editRadioBtn.classList.add('selected');
    }
    
    // const radioBtn = document.getElementById('radio-' + method);
    // const editRadioBtn = document.getElementById('radio-edit-' + method);

    // if (radioBtn) radioBtn.classList.add('selected');
    // if (editRadioBtn) editRadioBtn.classList.add('selected');
}

//////
//////
//////
// //下参考コード必ず消す
// function selectAddress(addressId) {
//     // 例: addressId が 'address-0' の場合、インデックス 0 を抽出
//     const dbId = parseInt(addressId.split('-')[1]);
//     console.log("選択されたDB ID:", dbId);
//     // const indexStr = addressId;
//     // console.log("indexStr",indexStr);
    
//     // const index = parseInt(indexStr);
//     // console.log("index",index);
    
//     // ラジオボタンの選択状態を切り替える (既存のロジック)
//     document.querySelectorAll('[id^="radio-address"], [id^="radio-edit-address"]').forEach(btn => {
//         btn.classList.remove('selected');
//     });
    
//     // 通常用と編集用の両方のラジオボタンを選択状態にする
//     const radioBtn = document.getElementById('radio-' + addressId);
//     const editRadioBtn = document.getElementById('radio-edit-' + addressId);
//     if (radioBtn) radioBtn.classList.add('selected');
//     if (editRadioBtn) editRadioBtn.classList.add('selected');

//     // DBのID
//     // const dbId = addressDataList.findIndex(addr => addr.address1 === addressId);
//     console.log("dbId",dbId);

//     updateShippingInfo(addressId); // DB ID
// }
//////
//////
//////



/**
 * 選択された支払い方法 (card-X, conveni, paypay) に基づいてメイン画面を更新する
 * @param {string} methodId - 選択された支払い方法のID (例: 'card-0', 'conveni')
 */
function updatePaymentInfo(methodId) {
    const paymentInfoDisplay = document.getElementById('selectedPaymentInfo');
    const paymentSummaryValueElement = document.getElementById('payment-summary-value');
    let htmlContent = '';
    let summaryText = '';

    // エラー保護: payment-summary-value が見つからない場合のエラー回避
    if (!paymentSummaryValueElement) {
        console.error("エラー: 'payment-summary-value' 要素が見つかりません。HTMLを確認してください。");
        return; 
    }

    if (methodId.startsWith('card')) {
        // インデックスの抽出を 'card' の直後から行う
        const indexStr = methodId.substring(4); // 'card' (4文字) の後の文字列を取得
        const cardId = parseInt(indexStr);
        // const index = parseInt(indexStr);

        
        // cardInfoList を使用してカード情報を取得
        if (cardInfoList) { 
            // 2. ★修正: find() メソッドを使って、IDが一致するカードオブジェクトを検索★
            const card = cardInfoList.find(c => c.id === cardId)
            // console.log("選択されたカード情報:", card);            
            // カード番号の下4桁を取得 (DBから取得した `number` フィールドを使用)
            const lastFour = card.number.slice(-4);
            
            htmlContent = `
                <div class="payMethod">クレジットカード決済</div><br>
                <div class="masked-card" id="selectedCard">************${lastFour} (${card.expiry})</div>
            `;
            summaryText = 'クレジットカード';

            // グローバル変数を更新
            selectedPaymentMethod = methodId; 
        }
    } else {
        // 静的な支払い方法 (conveni, paypay)
        if (methodId === 'conveni') {
            summaryText = 'コンビニ支払い';
        } else if (methodId === 'paypay') {
            summaryText = 'PayPay';
        } else {
            summaryText = '支払い方法未選択'; 
        }
        
        htmlContent = summaryText;
        selectedPaymentMethod = methodId;
    }

    // メイン画面の要素を更新
    paymentInfoDisplay.innerHTML = htmlContent;
    paymentSummaryValueElement.textContent = summaryText; 
}







// 既存の selectPayment 関数も、選択後にメイン画面を更新するように修正
function selectPayment(methodId) {
    // ... (既存のラジオボタン切り替えロジック) ...
    
    // メイン画面の支払い情報を更新
    updatePaymentInfo(methodId);
    
    // グローバル変数 selectedPaymentMethod を更新
    selectedPaymentMethod = methodId; 

     // paymentModalとpaymentEditModalの両方のラジオボタンの状態を同期させる
     //原因はここ
    document.querySelectorAll('#paymentModal .radio-btn, #paymentEditModal .radio-btn').forEach(btn => {
    btn.classList.remove('selected');

    // ラジオボタンの選択状態を切り替える (既存のロジック)
    // document.querySelectorAll('[id^="radio-card"], [id^="radio-edit-card"]').forEach(btn => {
    //     btn.classList.remove('selected');

    });
    if (methodId.startsWith('card')) {
        // インデックスの抽出を 'card' の直後から行う
        const indexStr = methodId.substring(4); // 'card' (4文字) の後の文字列を取得
        const cardId = parseInt(indexStr);
        //cardIdに対応するデータが何番目かを特定する
        // let methodindex = cardInfoList.findIndex(c => c.id === cardId);
        // console.log("methodindex",methodindex);

        const radioBtn = document.getElementById('radio-card' + cardId);
        const editRadioBtn = document.getElementById('radio-edit-card' + cardId);
        
        // console.log('選択された支払い', radioBtn);
        // console.log('選択された支払い編集', editRadioBtn);
        
        if (radioBtn) radioBtn.classList.add('selected');
        if (editRadioBtn) editRadioBtn.classList.add('selected');
    }else if (methodId === 'conveni' || methodId === 'paypay') {
        const radioBtn = document.getElementById('radio-' + methodId);
        const editRadioBtn = document.getElementById('radio-edit-' + methodId);

        if (radioBtn) radioBtn.classList.add('selected');
        if (editRadioBtn) editRadioBtn.classList.add('selected');
    }
}





function confirmDeleteCard(event, cardId) {
    event.stopPropagation();
    cardToDelete = cardId;
    document.getElementById('deleteConfirmModal').classList.add('active');
}

function closeDeleteConfirm() {
    document.getElementById('deleteConfirmModal').classList.remove('active');
    cardToDelete = null;
}

function executeDelete() {
    if (cardToDelete) {
        alert('カード ' + cardToDelete + ' が削除されました');
        cardToDelete = null;
    }
    if (addressToDelete) {
        alert('住所 ' + addressToDelete + ' が削除されました');
        addressToDelete = null;
    }
    closeDeleteConfirm();
    closePaymentEditModal();
    closeAddressEditModal();
}

function editCard(event, cardId) {
    event.preventDefault();
    event.stopPropagation();
    alert('カード編集画面へ遷移します');
}

function goToCardRegister() {
    closePaymentModal();
    closePaymentEditModal();
    document.getElementById('cardRegisterPage').style.display = 'block';
    document.body.style.overflow = 'hidden';
}

function closeCardRegister() {
    document.getElementById('cardRegisterPage').style.display = 'none';
    document.body.style.overflow = 'auto';
}

function openAddressModal(event) {
    event.preventDefault();
    document.getElementById('addressModal').classList.add('active');
}

function closeAddressModal() {
    document.getElementById('addressModal').classList.remove('active');
}

function editAddresses(event) {
    event.preventDefault();
    document.getElementById('addressModal').classList.remove('active');
    document.getElementById('addressEditModal').classList.add('active');
}

function closeAddressEditModal() {
    document.getElementById('addressEditModal').classList.remove('active');
}

function completeAddressEdit(event) {
    event.preventDefault();
    closeAddressEditModal();
    document.getElementById('addressModal').classList.add('active');
}

// function selectAddress(addressId) {
//     selectedAddress = addressId;
    
//     document.querySelectorAll('[id^="radio-address"], [id^="radio-edit-address"]').forEach(btn => {
//         btn.classList.remove('selected');
//     });
    
//     const radioBtn = document.getElementById('radio-' + addressId);
//     const editRadioBtn = document.getElementById('radio-edit-' + addressId);
//     if (radioBtn) radioBtn.classList.add('selected');
//     if (editRadioBtn) editRadioBtn.classList.add('selected');
// }


function selectAddress(addressId) {
    // 例: addressId が 'address-0' の場合、インデックス 0 を抽出
    const dbId = parseInt(addressId.split('-')[1]);
    // console.log("選択されたDB ID:", dbId);
    // const indexStr = addressId;
    // console.log("indexStr",indexStr);
    
    // const index = parseInt(indexStr);
    // console.log("index",index);
    
    // ラジオボタンの選択状態を切り替える (既存のロジック)
    document.querySelectorAll('[id^="radio-address"], [id^="radio-edit-address"]').forEach(btn => {
        btn.classList.remove('selected');
    });
    
    // 通常用と編集用の両方のラジオボタンを選択状態にする
    const radioBtn = document.getElementById('radio-' + addressId);
    const editRadioBtn = document.getElementById('radio-edit-' + addressId);
    if (radioBtn) radioBtn.classList.add('selected');
    if (editRadioBtn) editRadioBtn.classList.add('selected');

    // DBのID
    // const dbId = addressDataList.findIndex(addr => addr.address1 === addressId);
    // console.log("dbId",dbId);

    updateShippingInfo(addressId); // DB ID
}

// function updateAddress() {
//     const selectedAddressElement = document.getElementById('selectedAddress');
    
//     const addresses = {
//         'address1': 'HAL 大阪（ハル オオサカ）<br>〒530-0001<br>大阪府 大阪市 北区 梅田3丁目3−1',
//         'address2': 'HAL 東京（ハル トウキョウ）<br>〒160-0023<br>東京都新宿区西新宿1丁目7−3',
//         'address3': 'HAL 名古屋（ハル ナゴヤ）<br>〒450-0002<br>愛知県名古屋市中村区名駅4丁目27−1'
//     };
    
//     selectedAddressElement.innerHTML = addresses[selectedAddress];
//     closeAddressModal();
//     closeAddressEditModal();
// }

function confirmDeleteAddress(event, addressId) {
    event.stopPropagation();
    addressToDelete = addressId;
    document.getElementById('deleteConfirmModal').classList.add('active');
}

function addNewAddress() {
    alert('新しい住所登録画面へ遷移します');
}

function openDeliveryLocationModal(event) {
    event.preventDefault();
    document.getElementById('deliveryLocationModal').classList.add('active');
}

function closeDeliveryLocationModal() {
    document.getElementById('deliveryLocationModal').classList.remove('active');
}

function selectDeliveryLocation(location) {
    selectedDeliveryLocation = location;
    
    document.querySelectorAll('#deliveryLocationModal .radio-btn').forEach(btn => {
        btn.classList.remove('selected');
    });
    
    const locationMap = {
        '玄関前': 'door',
        '宅配ボックス': 'box',
        'ガスメーターボックス': 'gas',
        '自転車のカゴ': 'bicycle',
        '車庫': 'garage',
        '建物内受付/管理人': 'reception',
        '選択しない': 'none'
    };
    
    const radioId = 'radio-' + locationMap[location];
    const radioBtn = document.getElementById(radioId);
    if (radioBtn) {
        radioBtn.classList.add('selected');
    }

    
}

function updateDeliveryLocation() {
    document.getElementById('selectedDeliveryLocation').textContent = selectedDeliveryLocation;
    closeDeliveryLocationModal();
}

function confirmPurchase() {
    alert('購入が確定されました。ありがとうございます！');
}

function openSecurityHelp() {
    document.getElementById('securityHelpModal').classList.add('active');
}

function closeSecurityHelp() {
    document.getElementById('securityHelpModal').classList.remove('active');
}

function registerNewCard(e) {
    e.preventDefault();
    const cardNumber = document.getElementById('newCardNumber').value;
    const cardExpiry = document.getElementById('newCardExpiry').value;
    const securityCode = document.getElementById('newSecurityCode').value;

    if (!cardNumber || !cardExpiry || !securityCode) {
        alert('すべての項目を入力してください');
        return;
    }

    alert('クレジットカードが登録されました');
    closeCardRegister();
    
    // フォームをリセット
    document.getElementById('newCardNumber').value = '';
    document.getElementById('newCardExpiry').value = '';
    document.getElementById('newSecurityCode').value = '';
}

// カード番号の自動フォーマット
document.addEventListener('DOMContentLoaded', function() {
    const cardNumberInput = document.getElementById('newCardNumber');
    if (cardNumberInput) {
        cardNumberInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\s/g, '');
            let formattedValue = value.match(/.{1,4}/g)?.join(' ') || value;
            e.target.value = formattedValue;
        });
    }

    const cardExpiryInput = document.getElementById('newCardExpiry');
    if (cardExpiryInput) {
        cardExpiryInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length >= 2) {
                value = value.slice(0, 2) + '/' + value.slice(2, 4);
            }
            e.target.value = value;
        });
    }
});

// モーダル外クリックで閉じる
document.querySelectorAll('.modal').forEach(modal => {
    modal.addEventListener('click', function(e) {
        if (e.target === this) {
            this.classList.remove('active');
        }
    });
});



// 修正後: フォームの submit イベントにリスナーを登録する
const purchaseForm = document.getElementById('purchaseForm');

// purchaseForm 要素が存在することを確認する（nullチェック）
if (purchaseForm) {
    purchaseForm.addEventListener('submit', function(e) {
        updateHiddenFormFields(); // 送信前に最新の選択状態を反映
        console.log('Hidden prodcut ID:', document.getElementById('hidden_product_id').value);        
        console.log('Hidden Payment Method:', document.getElementById('hidden_payment_method').value);
        console.log('Hidden Creditcards ID:', document.getElementById('hidden_creditcards_id').value);
        console.log('Hidden Address Index:', document.getElementById('hidden_address_index').value);
        console.log('Hidden Delivery Location:', document.getElementById('hidden_delivery_location').value);
        
        // e.preventDefault(); // デバッグを続ける場合は有効にし、本番ではコメントアウトまたは削除
    });
} else {
    console.error("エラー: ID 'purchaseForm' を持つ要素がDOMに見つかりません。");
}