/**
 * login1.js
 * 本人確認フォーム (identity_verification.html) 用のJavaScript
 * - カスタムデザインされた領域と非表示のファイル入力要素を連動させる
 * - ファイル選択後にラベルにファイル名を表示する
 */

document.addEventListener('DOMContentLoaded', function() {

    // ====================================
    // 1. ファイル入力要素とクリック領域の連動
    // ====================================
    
    // アップロードボックスと対応するinput要素のペアを取得
    const uploadBoxes = document.querySelectorAll('.verification__upload-box');

    uploadBoxes.forEach(function(box) {
        const fileInput = box.querySelector('.verification__file-input');
        
        // input要素が見つからない場合はスキップ
        if (!fileInput) return;

        // --- A. クリック連動処理 ---
        // ボックス全体がクリックされたときのイベント
        box.addEventListener('click', function(e) {
            // クリックが既にファイル入力要素自体に届いていないことを確認
            // （二重にクリックイベントが発火するのを防ぐ）
            if (e.target !== fileInput) {
                 // 非表示のファイル input のクリックイベントをプログラムから発火
                fileInput.click();
            }
        });

        // --- B. ファイル選択後のラベル表示更新 ---
        fileInput.addEventListener('change', function() {
            const label = box.querySelector('.verification__upload-label');
            
            if (label) {
                if (this.files.length > 0) {
                    // ファイルが選択されたら、ファイル名を表示
                    label.textContent = this.files[0].name;
                } else {
                    // ファイルがキャンセルされたら、元のテキストに戻す
                    // 'front_image' と 'back_image' で元のテキストが異なるため、
                    // IDやクラスで識別して元のテキストを設定する必要がありますが、
                    // ここでは簡単な識別で処理します。
                    const defaultText = this.name === 'front_image' ? '表面' : '住所が記載されている場合（裏面）';
                    label.textContent = defaultText;
                }
            }
        });
    });
    
    // 補足: CSSで input[type="file"] を完全に非表示にしていることを前提としています。
    // 例: .verification__file-input { display: none; }
});