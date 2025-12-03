document.addEventListener('DOMContentLoaded', function() {

    // ------------------------------------
    // 共通関数: エラー表示/クリア
    // ------------------------------------
    function showError(element, message) {
        const errorElem = element.closest('.rfo-form-group').querySelector('.rfo-error');
        if (errorElem) {
            errorElem.textContent = message;
            errorElem.style.display = 'block';  // エラーメッセージを表示
        }
    }

    function clearError(element) {
        const errorElem = element.closest('.rfo-form-group').querySelector('.rfo-error');
        if (errorElem) {
            errorElem.textContent = '';
            errorElem.style.display = 'none';  // エラーメッセージを非表示
        }
    }

    // ------------------------------------
    // 郵便番号から住所を自動入力
    // ------------------------------------
    const postalInput = document.getElementById('postal');
    postalInput.addEventListener('blur', function() {
        const postalVal = this.value.replace(/[^0-9]/g,''); // 数字だけ
        if (postalVal.length === 7) {
            fetch(`https://zipcloud.ibsnet.co.jp/api/search?zipcode=${postalVal}`)
            .then(res => res.json())
            .then(data => {
                if (data.status === 200 && data.results) {
                    const r = data.results[0];

                    const prefectureInput = document.getElementById('prefecture');
                    const prefectureDisplay = document.querySelector('.rfo-prefecture-selected');

                    prefectureDisplay.textContent = r.address1;
                    prefectureInput.value = r.address1;
                    document.getElementById('city').value = r.address2;
                    document.getElementById('address').value = r.address3;
                    document.getElementById('building').focus();
                    clearError(prefectureDisplay);
                } else {
                    console.log('住所が見つかりません');
                }
            })
            .catch(err => console.error(err));
        }
    });

    // ------------------------------------
    // フォーム送信ハンドラ
    // ------------------------------------
    const form = document.getElementById('registerForm');
    form.addEventListener('submit', function(event) {
        let valid = true;
        let firstErrorElement = null;

        const account = document.getElementById('account');
        const lastname = document.getElementById('lastname');
        const firstname = document.getElementById('firstname');
        const lastnameKana = document.getElementById('lastname-kana');
        const firstnameKana = document.getElementById('firstname-kana');
        const birthday = document.getElementById('birthday');
        const postal = document.getElementById('postal');
        const prefectureInput = document.getElementById('prefecture');
        const prefectureDisplay = document.querySelector('.rfo-prefecture-selected');
        const city = document.getElementById('city');
        const address = document.getElementById('address');
        const phone = document.getElementById('phone');

        // ----- 正規表現 -----
        const fullWidthRegex = /^[^\x01-\x7E\xA1-\xDF]+$/; // 全角文字（漢字・ひらがな・カナ）
        const katakanaRegex = /^[ァ-ヶー　]+$/; // 全角カタカナ

        // ----- 未入力＆形式チェック -----
        if (!account.value.trim()) {
            showError(account, 'アカウント名を入力してください');
            valid = false; if (!firstErrorElement) firstErrorElement = account;
        } else { clearError(account); }

        // 姓（全角）
        if (!lastname.value.trim()) {
            showError(lastname, '姓を入力してください');
            valid = false; if (!firstErrorElement) firstErrorElement = lastname;
        } else if (!fullWidthRegex.test(lastname.value)) {
            showError(lastname, '姓は全角で入力してください');
            valid = false; if (!firstErrorElement) firstErrorElement = lastname;
        } else { clearError(lastname); }

        // 名（全角）
        if (!firstname.value.trim()) {
            showError(firstname, '名を入力してください');
            valid = false; if (!firstErrorElement) firstErrorElement = firstname;
        } else if (!fullWidthRegex.test(firstname.value)) {
            showError(firstname, '名は全角で入力してください');
            valid = false; if (!firstErrorElement) firstErrorElement = firstname;
        } else { clearError(firstname); }

        // セイ（全角カタカナ）
        if (!lastnameKana.value.trim()) {
            showError(lastnameKana, 'セイを入力してください');
            valid = false; if (!firstErrorElement) firstErrorElement = lastnameKana;
        } else if (!katakanaRegex.test(lastnameKana.value)) {
            showError(lastnameKana, 'セイは全角カタカナで入力してください');
            valid = false; if (!firstErrorElement) firstErrorElement = lastnameKana;
        } else { clearError(lastnameKana); }

        // メイ（全角カタカナ）
        if (!firstnameKana.value.trim()) {
            showError(firstnameKana, 'メイを入力してください');
            valid = false; if (!firstErrorElement) firstErrorElement = firstnameKana;
        } else if (!katakanaRegex.test(firstnameKana.value)) {
            showError(firstnameKana, 'メイは全角カタカナで入力してください');
            valid = false; if (!firstErrorElement) firstErrorElement = firstnameKana;
        } else { clearError(firstnameKana); }

        if (!birthday.value.trim()) {
            showError(birthday, '生年月日を入力してください');
            valid = false; if (!firstErrorElement) firstErrorElement = birthday;
        } else { clearError(birthday); }

        if (!/^\d{7}$/.test(postal.value.trim())) {
            showError(postal, '郵便番号は7桁で入力してください');
            valid = false; if (!firstErrorElement) firstErrorElement = postal;
        } else { clearError(postal); }

        if (!prefectureInput.value || prefectureInput.value === '選択してください') {
            showError(prefectureDisplay, '都道府県を選択してください');
            valid = false; if (!firstErrorElement) firstErrorElement = prefectureDisplay;
        } else { clearError(prefectureDisplay); }

        if (!city.value.trim()) {
            showError(city, '市区町村を入力してください');
            valid = false; if (!firstErrorElement) firstErrorElement = city;
        } else { clearError(city); }

        if (!address.value.trim()) {
            showError(address, '番地を入力してください');
            valid = false; if (!firstErrorElement) firstErrorElement = address;
        } else { clearError(address); }

        if (!/^\d{10,11}$/.test(phone.value.trim())) {
            showError(phone, '電話番号は10〜11桁で入力してください');
            valid = false; if (!firstErrorElement) firstErrorElement = phone;
        } else { clearError(phone); }

        // ----- 喫煙の有無チェック -----
        const smokingRadios = document.getElementsByName('smoker');
        let smokingChecked = false;
        for (let i = 0; i < smokingRadios.length; i++) {
            if (smokingRadios[i].checked) { smokingChecked = true; break; }
        }
        const radioGroup = document.querySelector('.rfo-radio-group');
        if (!smokingChecked) {
            showError(radioGroup, '喫煙の有無を選択してください');
            valid = false;
            if (!firstErrorElement) firstErrorElement = radioGroup;
        } else { clearError(radioGroup); }

        // ----- エラーがあればスクロールしてフォーカス -----
        if (!valid) {
            event.preventDefault(); // 送信停止
            if (firstErrorElement) {
                firstErrorElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
                if (firstErrorElement.focus) firstErrorElement.focus();
            }
            return false;
        }

        // バリデーションOKの場合は通常送信
        console.log('登録実行:', {
            account: account.value,
            lastname: lastname.value,
            firstname: firstname.value,
            lastnameKana: lastnameKana.value,
            firstnameKana: firstnameKana.value,
            prefecture: prefectureInput.value,
            phone: phone.value,
            postal: postal.value,
            smoking: smokingChecked ? document.querySelector('input[name="smoker"]:checked').value : null
        });
    });

});
