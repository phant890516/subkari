document.addEventListener('DOMContentLoaded', function() {
    
 
    const productData = document.getElementById('app').dataset.product
    ? JSON.parse(document.getElementById('app').dataset.product)
    : null;
    if (productData) {
        // 編輯模式：將資料存進 sessionStorage
        sessionStorage.setItem("name", productData.name);
        sessionStorage.setItem("rental", productData.rentalFlg ? "true" : "false");
        sessionStorage.setItem("purchase", productData.purchaseFlg ? "true" : "false");
        sessionStorage.setItem("rentalPrice", productData.rentalPrice || '');
        sessionStorage.setItem("rentalPeriod", productData.rentalPeriod || '');
        sessionStorage.setItem("purchasePrice", productData.purchasePrice || '');
        sessionStorage.setItem("smoking", productData.smokingFlg ? "yes" : "no");
        sessionStorage.setItem("color", productData.color);
        sessionStorage.setItem("category1",productData.for);
        sessionStorage.setItem("category2",productData.category_id);
        sessionStorage.setItem("brand",productData.brand_id);
        sessionStorage.setItem("explanation", productData.explanation || '');
        sessionStorage.setItem("returnLocation", productData.returnAddress || '');
    }
    //このページ入る同時に、画像を表示する（あった場合）
            loadUploadedImages();
    //session資料回復
            loadFromSessionStorage()
    //sizeデータ取得
            fetch('/seller/get_size_selected')
                .then(res => res.json())
                .then(size => {
                    console.log("Session size資料：", size);
                });
    //cleanデータ取得
            fetch('/seller/get_clean_selected')
                .then(res => res.json())
                .then(cleanNotes => {
                    console.log("Session cleanNotes資料：", cleanNotes);
                });
        });
 
 
// 価格トグル
const rentalCheckbox = document.querySelector('.rentalCheckbox');
const purchaseCheckbox = document.querySelector('.purchaseCheckbox');
const rentalPriceSection = document.getElementById('rentalPriceSection');
const purchasePriceSection = document.getElementById('purchasePriceSection');
const rentalPurchaseError = document.getElementById('rentalPurchaseError');
 
// レンタル可能チェックボックス
rentalCheckbox.addEventListener('change', function() {
    const existingSection = document.getElementById('rentalPriceSection');
    const existingPeriod = document.getElementById('rental_period');
     
    if (this.checked) {
        // 存在しない場合のみ作成
        if (!existingSection) {
            createRentalPriceSection();         
        }
        if(!existingPeriod){
            createRentalPeriod();
        }
    } else {
        // 削除
        if (existingSection) {
            existingSection.remove();
        }
        if(existingPeriod){
            existingPeriod.remove();
        }
    }
    // validateSelection();
});
 
// 購入可能チェックボックス
purchaseCheckbox.addEventListener('change', function() {
    const existingSection = document.getElementById('purchasePriceSection');
    
    if (this.checked) {
        // 存在しない場合のみ作成
        if (!existingSection) {
            createPurchasePriceSection();
        }
    } else {
        // 削除
        if (existingSection) {
            existingSection.remove();
        }
    }
    // validateSelection();
});
 
// レンタル価格セクション作成
function createRentalPriceSection() {
    const newSection = document.createElement('div');
    newSection.id = 'rentalPriceSection';
    newSection.className = 'flex flex-col gap-2';
    newSection.innerHTML = `
        <div class="price-input-wrapper">
        <input type="number" id="rentalPrice" name="rentalPrice" placeholder="0" min="0" class="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:border-blue-500">
        <span class="text-red-500 text-sm hidden" id="rentalPriceError">レンタル価格を入力してください</span>
        </div>
        `;
    
    const rentalLabel = rentalCheckbox.closest('label');
    rentalLabel.after(newSection);
    
    document.getElementById('rentalPrice').focus();
}
// レンタル期間作成
function createRentalPeriod() {
    const newSection = document.createElement('div');
    newSection.id = 'rental_period';
    newSection.className = 'flex flex-col gap-2';
    newSection.innerHTML = `
                    <label class="block text-sm font-semibold mb-2">
                       レンタル期間 <span class="text-red-500">*</span>
                    </label>
                    <select name="period" id="rentalPeriod" class="w-full px-4 py-2 border border-[#9a9a9a] rounded focus:outline-none focus:border-blue-500">
                        <option value="4" selected>4</option>
                        <option value="7">7</option>
                        <option value="14">14</option>
                    </select>
                    <span class="text-red-500 text-sm hidden" id="rentalPeriodError">レンタル期間を選択してください</span>

        `;
    
    const rentalLabel = rentalCheckbox.closest('label');
    rentalLabel.after(newSection);
    
    document.getElementById('rentalPeriod').focus();
}
 
// 購入価格セクション作成
function createPurchasePriceSection() {
    const newSection = document.createElement('div');
    newSection.id = 'purchasePriceSection';
    newSection.className = 'flex flex-col gap-2';
    newSection.innerHTML = `
        <div class="price-input-wrapper">
        <input type="number" id="purchasePrice" name="purchasePrice" placeholder="0" min="0" class="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:border-blue-500">
        <span class="text-red-500 text-sm hidden" id="purchasePriceError">購入価格を入力してください</span>
        </div>
        `;
    
    const purchaseLabel = purchaseCheckbox.closest('label');
    purchaseLabel.after(newSection);
    
    document.getElementById('purchasePrice').focus();
}
 
//画像表示
function loadUploadedImages() {
    const saved = sessionStorage.getItem('uploadedImages');
    //アップロードした画像があった場合
    if (saved) {
        const images = JSON.parse(saved);
        console.log('Loaded images:', images);
        // ここで images を使用
        displayFirstImage(images[0]);
    }
}
//画像フィールドで表示 画像アップロード提示フィールドを隠す
function displayFirstImage(image) {
    const displayArea = document.getElementById('imageDisplayArea');
    const noImageArea = document.getElementById('noImageArea');
    const displayImage = document.getElementById('displayImage');
    
    if (displayArea && displayImage) {
        displayImage.src = image.src;  // Base64 データURLを設定
        displayArea.classList.remove('hidden');
        
        if (noImageArea) {
            noImageArea.classList.add('hidden');
        }
    }
}
 
//sessionに記録の関数//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
function saveToSessionStorage(){
    //資料
    const productName = document.getElementById("name").value;
    const rental = document.getElementById("rental").checked;
    const purchase = document.getElementById("purchase").checked;
    const rentalPrice = document.getElementById("rentalPrice")?.value || '';
    const rentalPeriod = document.getElementById("rentalPeriod")?.value || '';
    const purchasePrice = document.getElementById("purchasePrice")?.value || '';
    const smokingValue = document.querySelector('input[name="smoking"]:checked').value;
    const color = document.getElementById("color").value;
    const category1 = document.getElementById("category1").value;
    const category2 = document.getElementById("category2").value;
    const brand = document.getElementById("brand").value;
    const explanation = document.getElementById("explanation").value;
    const returnLocation = document.querySelector('input[name="returnLocation"]').value;
    const rentalCheckbox = document.querySelector('.rentalCheckbox');
    const purchaseCheckbox = document.querySelector('.purchaseCheckbox');
    const rentalPriceSection = document.getElementById('rentalPriceSection');
    const purchasePriceSection = document.getElementById('purchasePriceSection');
    const rentalPurchaseError = document.getElementById('rentalPurchaseError');   
///////////////// Session保存//////////////////////////////////////////////////////////////////
    console.log("session saved");
 
    sessionStorage.setItem("name", productName);
 
    if (!rental) {
    sessionStorage.removeItem("rentalPrice");
    sessionStorage.removeItem("rentalPeriod");
    sessionStorage.setItem("rental", "false");
    } else {
        sessionStorage.setItem("rental", "true");
        sessionStorage.setItem("rentalPrice", rentalPrice);
        sessionStorage.setItem("rentalPeriod",rentalPeriod);
    }
 
    if (!purchase) {
        sessionStorage.removeItem("purchasePrice");
        sessionStorage.setItem("purchase", "false");
    } else {
        sessionStorage.setItem("purchase", "true");
        sessionStorage.setItem("purchasePrice",purchasePrice);
    }
 
    sessionStorage.setItem("smoking", smokingValue);
    sessionStorage.setItem("color", color);
    sessionStorage.setItem("category1", category1);
    sessionStorage.setItem("category2", category2);
    sessionStorage.setItem("brand", brand);
    sessionStorage.setItem("explanation", explanation);
    sessionStorage.setItem("returnLocation", returnLocation);
   
}
 
 
// Session恢復////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
function loadFromSessionStorage() {
    console.log("sessionStorageからデータを復元");
 
    // 商品名
    const name = sessionStorage.getItem("name");
    if (name) document.getElementById("name").value = name;
 
    // レンタル・購入
    const rental = sessionStorage.getItem("rental") === "true";
    const purchase = sessionStorage.getItem("purchase") === "true";
    const rentalCheckbox = document.getElementById("rental");
    const purchaseCheckbox = document.getElementById("purchase");
    if (rentalCheckbox) rentalCheckbox.checked = rental;
    if (purchaseCheckbox) purchaseCheckbox.checked = purchase;
 
    // レンタル価格
    const rentalPrice = sessionStorage.getItem("rentalPrice");
    const rentalPeriod = sessionStorage.getItem("rentalPeriod");
    if (rental) {
        if (!document.getElementById("rentalPrice")) {
            createRentalPriceSection(); // 動的に生成
            
        }
        document.getElementById("rentalPrice").value = rentalPrice;
        
        if (!document.getElementById("rentalPeriod")) {
            createRentalPeriod();// 動的に生成
            console.log("createRentalPeriod called");
        }
        const element = document.getElementById("rentalPeriod");
        console.log("element found:", !!element);
        console.log("setting value to:", rentalPeriod);
        element.value = rentalPeriod;
        console.log("actual value now:", element.value);
    }

    // 購入価格
    const purchasePrice = sessionStorage.getItem("purchasePrice");
    if (purchasePrice) {
        if (!document.getElementById("purchasePrice")) {
            createPurchasePriceSection();
        }
        document.getElementById("purchasePrice").value = purchasePrice;
    }
 
    // 喫煙
    const smoking = sessionStorage.getItem("smoking");
    if (smoking) {
        const smokingRadio = document.querySelector(`input[name="smoking"][value="${smoking}"]`);
        if (smokingRadio) smokingRadio.checked = true;
    }
 
    // 系統カラー
    const color = sessionStorage.getItem("color");
    if (color) document.getElementById("color").value = color;
 
    // カテゴリー1・2
    const category1 = sessionStorage.getItem("category1");
    if (category1) document.getElementById("category1").value = category1;
 
    const category2 = sessionStorage.getItem("category2");
    if (category2) document.getElementById("category2").value = category2;
 
    // ブランド
    const brand = sessionStorage.getItem("brand");
    if (brand) document.getElementById("brand").value = brand;
 
    // 商品説明
    const explanation = sessionStorage.getItem("explanation");
    if (explanation) document.getElementById("explanation").value = explanation;
 
    // 返却場所
    const returnLocation = sessionStorage.getItem("returnLocation");
    if (returnLocation) {
        const el = document.querySelector('input[name="returnLocation"]');
        if (el) el.value = returnLocation;
    }
    console.log("sessionStorageからの復元完了");
}
 
//他の資料をsessionStorage裡面保存 その後size画面遷移/////////////////////////////////////////////////////////////////////////////////////////
function goToSize(sizeUrl){
    saveToSessionStorage();
    window.location.href = sizeUrl;
}
//他の資料をsessionStorage裡面保存 その後clean画面遷移/////////////////////////////////////////////////////////////////////////////////////////
function goToClean(sizeUrl){
    saveToSessionStorage();
    window.location.href = sizeUrl;
}
 
// フォーム検証
function validateForm() {
    saveToSessionStorage();
    let isValid = true;
    let rentalflag = false;
    // 商品名
    const productName = document.getElementById('name').value.trim();
    if (!productName) {
        document.getElementById('productNameError').classList.remove('hidden');
        isValid = false;
    } else {
        document.getElementById('productNameError').classList.add('hidden');
    }
 
    // レンタル・購入
    const rental = document.getElementById('rental').checked;
    const purchase = document.getElementById('purchase').checked;
    const rentalPrice = document.getElementById('rentalPrice')?.value || '';
    const rentalPeriod = document.getElementById('rentalPeriod')?.value || '';
    const purchasePrice = document.getElementById('purchasePrice')?.value || '';

    if (!rental && !purchase) {
        document.getElementById('rentalPurchaseError').classList.remove('hidden');
        isValid = false;
        console.log("レンタルと購入エラー");
    } else {
        document.getElementById('rentalPurchaseError').classList.add('hidden');
    }
    if(rental){
        rentalflag = true;
        if(!rentalPrice){
        document.getElementById('rentalPriceError').classList.remove('hidden');
        isValid = false;
        console.log("レンタル価格エラー");
        }
        else{
        document.getElementById('rentalPriceError').classList.add('hidden');
        }
        if(!rentalPeriod){
        document.getElementById('rentalPeriodError').classList.remove('hidden');
        isValid = false;
        console.log("レンタル期間エラー");    
        }
        else{
        document.getElementById('rentalPeriodError').classList.add('hidden');
        }
    }
    // else {
    // document.getElementById('rentalPriceError').classList.add('hidden');
    // document.getElementById('rentalPeriodError').classList.add('hidden');
    // }

    if(purchase){
        if(!purchasePrice){
        document.getElementById('purchasePriceError').classList.remove('hidden');
        isValid = false;
        console.log("購入エラー");
        }
        else{
        document.getElementById('purchasePriceError').classList.add('hidden');
        }
    }
    // else {
    // document.getElementById('purchasePriceError').classList.add('hidden');
    // }
 
    // 系統カラー
    const color = document.getElementById('color').value.trim();
    if (!color) {
        document.getElementById('colorError').classList.remove('hidden');
        isValid = false;
        console.log("カラーエラー");
    } else {
        document.getElementById('colorError').classList.add('hidden');
    }
 
    // カテゴリー1
    const category1 =document.getElementById('category1').value;
    if (!category1) {
        document.getElementById('category1Error').classList.remove('hidden');
        isValid = false;
        console.log("カテゴリ１エラー");
    } else {
        document.getElementById('category1Error').classList.add('hidden');
    }
 
    // カテゴリー2
    const category2 = document.getElementById('category2').value;
    if (!category2) {
        document.getElementById('category2Error').classList.remove('hidden');
        isValid = false;
        console.log("カテゴリ２エラー");
    } else {
        document.getElementById('category2Error').classList.add('hidden');
    }
     // brand
    const brand = document.getElementById('brand').value;
    if (!brand) {
        document.getElementById('brandError').classList.remove('hidden');
        isValid = false;
        console.log("ブランドエラー");
    } else {
        document.getElementById('brandError').classList.add('hidden');
    }
    // サイズ
    const sizeDisplay = document.getElementById('sizeDisplay').innerText.trim();
    if (sizeDisplay === '未選択') {
        document.getElementById('sizeError').classList.remove('hidden');
        isValid = false;
        console.log("サイズエラー");
    } else {
        document.getElementById('sizeError').classList.add('hidden');
    }
 
    // 洗濯表示
    const washingDisplay = document.getElementById('washingDisplay').innerText.trim();
    if (washingDisplay === '未選択') {
        document.getElementById('washingError').classList.remove('hidden');
        isValid = false;
        console.log("洗濯エラー");
    } else {
        document.getElementById('washingError').classList.add('hidden');
    }
 
    // 返却場所
    const returnLocation = document.getElementById('returnLocation').value.trim();
    if (!returnLocation && rentalflag ){
        document.getElementById('returnLocationError').classList.remove('hidden');
        isValid = false;
        console.log("返却場所エラー");
        
    } else {
        document.getElementById('returnLocationError').classList.add('hidden');
    }
    
    return isValid;
}
 

///////////////////////////////////////////////////////画像の形式変換の関数///////////////////////////////////////////////////////////////////////////
function base64ToFile(base64Data, filename) {
  const arr = base64Data.split(',');
  const mime = arr[0].match(/:(.*?);/)[1];
  const bstr = atob(arr[1]);
  let n = bstr.length;
  const u8arr = new Uint8Array(n);
  while (n--) u8arr[n] = bstr.charCodeAt(n);
  return new File([u8arr], filename, { type: mime });
}
 
/**
* フォーム送信
*/

/**
* フォーム送信
*/
function submitForm() {
    // バリデーション
    if (!validateForm()) {
        console.log("未入力項目存在.")
        return;
    }
 
    // sessionStorage から画像を取得
    const uploadedImages = JSON.parse(sessionStorage.getItem('uploadedImages') || '[]');
    
    // if (uploadedImages.length === 0) {
    //     alert('最低1つの画像をアップロードしてください');
    //     return;
    // }
    // console.log('=== 画像の格式確認 ===');
    // console.log('uploadedImages:', uploadedImages);
    // console.log('最初の画像:', uploadedImages[0]);
 
    // 全部のデータ変数
    const formData = new FormData();
 
     // ===== 画像 →　formData =====
        uploadedImages.forEach((imageData, index) => {
            try {
                const base64String = imageData.src;
 
                // Base64　転換　→　File
                const file = base64ToFile(base64String, `product_image_${index}.png`);
                formData.append('images', file);  // keyは'images'，複数あり
                console.log(`画像${index}FormDataに追加`);
            } catch (error) {
                console.error(`画像${index}形式変換失敗:`, error);
            }
        });
 
    //  sessionStorage 取得
    const productData = {
        name: sessionStorage.getItem("name"),
        rental: sessionStorage.getItem("rental") === "true",
        purchase: sessionStorage.getItem("purchase") === "true",
        rentalPrice: sessionStorage.getItem("rentalPrice") || null,
        rentalPeriod: sessionStorage.getItem("rentalPeriod") || null,
        purchasePrice: sessionStorage.getItem("purchasePrice") || null,
        smoking: sessionStorage.getItem("smoking") === "yes", // "yes" OR "no"
        color: sessionStorage.getItem("color"),
        category1: sessionStorage.getItem("category1"),
        category2: sessionStorage.getItem("category2"),
        brand: sessionStorage.getItem("brand"),
        explanation: sessionStorage.getItem("explanation"),
        returnLocation: sessionStorage.getItem("returnLocation"),
    };
 
    //すべてのデータ　→　formData
    formData.append('productData', JSON.stringify(productData));
 
    console.log('=== 準備完了 ===');
    console.log('画像の枚数:', uploadedImages.length);
    console.log('商品名:', productData.name);
    console.log('バックエンドに送る');
    console.log('=== 檢查 returnLocation ===');
    console.log('sessionStorage returnLocation:', sessionStorage.getItem("returnLocation"));
    console.log('productData:', productData);
    console.log('formData 內容:', Object.fromEntries(formData));
    fetch('/seller/format/save-product', {
        method: 'POST',
        body:formData
        // headers: {
        //     'Content-Type': 'application/json',
        // },
        // body: JSON.stringify(productData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Success:', data);
            alert('出品成功しました。');
            // 成功後　sessionStorageのデータすべて消す
            sessionStorage.clear();
            window.location.href="/seller/seller";
        } else {
            alert('失敗: ' + data.message);
        }
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('catch失敗');
    });
 
 
}
// 更新のフォーム送信
function submitUpdateForm() {
    // バリデーション
    if (!validateForm()) {
        console.log("未入力項目存在.")
        return;
    }
 
    // sessionStorage から画像を取得
    const uploadedImages = JSON.parse(sessionStorage.getItem('uploadedImages') || '[]');
    
    // if (uploadedImages.length === 0) {
    //     alert('最低1つの画像をアップロードしてください');
    //     return;
    // }
    // console.log('=== 画像の格式確認 ===');
    // console.log('uploadedImages:', uploadedImages);
    // console.log('最初の画像:', uploadedImages[0]);
 
    // 全部のデータ変数
    const formData = new FormData();
 
     // ===== 画像 →　formData =====
        uploadedImages.forEach((imageData, index) => {
            try {
                const base64String = imageData.src;
 
                // Base64　転換　→　File
                const file = base64ToFile(base64String, `product_image_${index}.png`);
                formData.append('images', file);  // keyは'images'，複数あり
                console.log(`画像${index}FormDataに追加`);
            } catch (error) {
                console.error(`画像${index}形式変換失敗:`, error);
            }
        });
 
    //  sessionStorage 取得
    const productData = {
        name: sessionStorage.getItem("name"),
        rental: sessionStorage.getItem("rental") === "true",
        purchase: sessionStorage.getItem("purchase") === "true",
        rentalPrice: sessionStorage.getItem("rentalPrice") || null,
        rentalPeriod: sessionStorage.getItem("rentalPeriod") || null,
        purchasePrice: sessionStorage.getItem("purchasePrice") || null,
        smoking: sessionStorage.getItem("smoking") === "yes", // "yes" OR "no"
        color: sessionStorage.getItem("color"),
        category1: sessionStorage.getItem("category1"),
        category2: sessionStorage.getItem("category2"),
        brand: sessionStorage.getItem("brand"),
        explanation: sessionStorage.getItem("explanation"),
        returnLocation: sessionStorage.getItem("returnLocation"),
    };
 
    //すべてのデータ　→　formData
    formData.append('productData', JSON.stringify(productData));
 
    console.log('=== 準備完了 ===');
    console.log('画像の枚数:', uploadedImages.length);
    console.log('商品名:', productData.name);
    console.log('バックエンドに送る');
    console.log('=== 檢查 returnLocation ===');
    console.log('sessionStorage returnLocation:', sessionStorage.getItem("returnLocation"));
    console.log('productData:', productData);
    console.log('formData 內容:', Object.fromEntries(formData));
    fetch('/seller/format/update-product', {
        method: 'POST',
        body:formData
        // headers: {
        //     'Content-Type': 'application/json',
        // },
        // body: JSON.stringify(productData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Success:', data);
            alert('出品成功しました。');
            // 成功後　sessionStorageのデータすべて消す
            sessionStorage.clear();
            window.location.href="/seller/seller";
        } else {
            alert('失敗: ' + data.message);
        }
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('catch失敗');
    });
 
}

// 下書き保存
function saveDraft() {
    console.log("save draft");
    
    saveToSessionStorage();
    // sessionStorage から画像を取得
    const uploadedImages = JSON.parse(sessionStorage.getItem('uploadedImages') || '[]');
    // 全部のデータ変数
    const formData = new FormData();
     // ===== 画像 →　formData =====
        uploadedImages.forEach((imageData, index) => {
            try {
                const base64String = imageData.src;
 
                // Base64　転換　→　File
                const file = base64ToFile(base64String, `product_image_${index}.png`);
                formData.append('images', file);  // keyは'images'，複数あり
                console.log(`画像${index}FormDataに追加`);
            } catch (error) {
                console.error(`画像${index}形式変換失敗:`, error);
            }
        });
 
    //  sessionStorage 取得
    const productData = {
        name: sessionStorage.getItem("name") || null,
        rental: sessionStorage.getItem("rental") === "true",
        purchase: sessionStorage.getItem("purchase") === "true",
        rentalPrice: sessionStorage.getItem("rentalPrice") || null,
        purchasePrice: sessionStorage.getItem("purchasePrice") || null,
        rentalPeriod: sessionStorage.getItem("rentalPeriod") || null,
        smoking: sessionStorage.getItem("smoking") === "yes", // "yes" OR "no"
        color: sessionStorage.getItem("color") || null,
        category1: sessionStorage.getItem("category1") || null,
        category2: sessionStorage.getItem("category2") || null,
        brand: sessionStorage.getItem("brand") || null,
        explanation: sessionStorage.getItem("explanation") || null,
        returnLocation: sessionStorage.getItem("returnLocation") || null,
    };
 
    //すべてのデータ　→　formData
    formData.append('productData', JSON.stringify(productData));
 
    console.log('=== 準備完了 ===');
    console.log('画像の枚数:', uploadedImages.length);
    console.log('商品名:', productData.name);
    console.log('バックエンドに送る');
    console.log('=== 檢查 returnLocation ===');
    console.log('sessionStorage returnLocation:', sessionStorage.getItem("returnLocation"));
    console.log('productData:', productData);
    console.log('formData 內容:', Object.fromEntries(formData));
    fetch('/seller/format/save-product-draft', {
        method: 'POST',
        body:formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Success:', data);
            alert('下書きに保存しました。');
            // 成功後　sessionStorageのデータすべて消す
            sessionStorage.clear();
            window.location.href="/seller/seller/draft";
        } else {
            alert('失敗: ' + data.message);
        }
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('catch失敗');
    });
 
    // window.location.href = url;
}
//キャンセル
function backToSeller(url){
    window.location.href=`${url}`;
}
 
 
// 既に出品中の商品まだ編集する
function editProduct(productId) {
    window.location.href = `/seller/update/${productId}`;
}
 
// 編輯モード
const isEditMode = document.body.getAttribute('data-edit-mode') === 'true';
const productId = document.body.getAttribute('data-product-id');
 
const endpoint = isEditMode ? '/seller/format/update-product' : '/seller/format/save-product';
 
//削除POP
function deleteProduct(productId) {
    // 提示
    if (confirm('本当に削除しますか？')) {
        // 「確認」後執行
        fetch(`/seller/format/delete-product/${productId}`, {
            method: 'DELETE',
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('商品を削除しました');
                // reload
                window.location.reload();
            } else {
                alert('削除失敗: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('エラーが発生しました');
        });
    }
    // 
}
 