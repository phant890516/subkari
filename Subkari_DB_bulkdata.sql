-- --------------------------------------------------------------
-- テストデータをいれてからbulkデータを実行してください             --
-- --------------------------------------------------------------
--アカウントのバルクデータ
-- 一時的にデリミタ（文の終端記号）を変更
DELIMITER $$

CREATE PROCEDURE sp_insert_test_data_all()
BEGIN
  DECLARE i INT DEFAULT 1;
  DECLARE v_account_id INT;
  DECLARE v_logout_time DATETIME;
  DECLARE v_created_time TIMESTAMP;

  WHILE i <= 100 DO
  
    -- 1. アカウントテーブルへの挿入 (created_atを6ヶ月以内に設定)
    
    -- 6ヶ月以内（約180日）のランダムな日時を生成
    SET v_created_time = DATE_SUB(NOW(), INTERVAL FLOOR(RAND() * 180) DAY);

    INSERT INTO `m_account` (
      `username`, `fullName`, `birthday`, `tel`, `mail`, `smoker`, 
      `introduction`, `money`, 
      `created_at`, -- ★条件追加：デフォルト値を使わず明示的に指定
      `status`, `updaterId`, `password`, 
      `identifyImg`, `apiFavoriteAnnounce`, `apiFollowAnnounce`, 
      `apiSystemAnnounce`, `mailFavoriteAnnounce`, `mailFollowAnnounce`, 
      `mailSystemAnnounce`, `autoLogin`
    ) 
    VALUES (
      CONCAT('testuser', i),
      CONCAT('テスト', i, ' 太郎'),
      DATE_SUB('2004-01-01', INTERVAL FLOOR(RAND() * 8000) DAY),
      CONCAT('080-1111-', LPAD(i, 4, '0')),
      CONCAT('testuser', i, '@example.com'),
      FLOOR(RAND() * 2),
      CONCAT('ユーザー', i, 'の自己紹介文です。'),
      FLOOR(RAND() * 100000),
      v_created_time, -- ★条件追加：生成した日時を設定
      ELT(FLOOR(1 + RAND() * 5), '未確認','本人確認済み','凍結','削除','強制削除'),
      NULL,
      'hashed_password_placeholder_12345',
      CONCAT('/uploads/identify/user', i, '.jpg'),
      FLOOR(RAND() * 2),
      FLOOR(RAND() * 2),
      1,
      FLOOR(RAND() * 2),
      FLOOR(RAND() * 2),
      1,
      FLOOR(RAND() * 2)
    );

    -- 2. ログインテーブルへの挿入 (最終ログアウトを2ヶ月以内に設定)

    -- 今挿入したアカウントのIDを取得
    SET v_account_id = LAST_INSERT_ID();
    
    -- 2ヶ月以内（約60日）のランダムなログアウト日時を生成
    SET v_logout_time = DATE_SUB(NOW(), INTERVAL FLOOR(RAND() * 60) DAY);

    INSERT INTO `t_login` (
      `account_id`,
      `loginDatetime`, -- ログアウトの1時間前にログインしたことにする
      `logoutDatetime`, -- ★条件追加：2ヶ月以内
      `notice`,
      `flag`
    )
    VALUES (
      v_account_id,
      DATE_SUB(v_logout_time, INTERVAL 1 HOUR), -- ログアウトの1時間前
      v_logout_time, -- 2ヶ月以内の日時
      FLOOR(RAND() * 2),
      FLOOR(RAND() * 2)
    );

    SET i = i + 1;
  END WHILE;
  
END$$

-- デリミタを元に戻す
DELIMITER ;


-- ストアドプロシージャの実行
CALL sp_insert_test_data_all();

-- ストアドプロシージャの削除
DROP PROCEDURE sp_insert_test_data_all;






-- 商品のバルクデータ   


-- 一時的にデリミタ（文の終端記号）を変更
DELIMITER $$

CREATE PROCEDURE sp_insert_test_products()
BEGIN
  DECLARE i INT DEFAULT 1;
  DECLARE v_upload_date DATE;
  DECLARE v_account_id INT;
  DECLARE v_brand_id INT;
  DECLARE v_category_id INT;

  WHILE i <= 100 DO
  
    -- 条件：作成日付（upload）を6ヶ月以内に設定
    SET v_upload_date = DATE_SUB(CURDATE(), INTERVAL FLOOR(RAND() * 180) DAY);
    
    -- 外部キー用のランダムIDを生成
    SET v_account_id = FLOOR(1 + RAND() * 100); -- 既存のaccount (1-100)
    
    -- ★修正点：ブランド件数 (12件) に合わせる
    SET v_brand_id = FLOOR(1 + RAND() * 12); -- 既存のbrand (1-12)
    
    -- ★修正点：カテゴリ件数 (4件) に合わせる
    SET v_category_id = FLOOR(1 + RAND() * 4); -- 既存のcategory (1-4)

    INSERT INTO `m_product` (
      `img`, `name`, `purchasePrice`, `rentalPrice`, `size`,
      `upload`, -- ★条件
      `showing`, `draft`, 
      `updateDate`,
      `purchaseFlg`, `rentalFlg`,
      `explanation`, 
      `account_id`, -- ★外部キー
      `brand_id`, -- ★外部キー
      `category_id`, -- ★外部キー
      `cleanNotes`, `smokingFlg`
    ) 
    VALUES (
      CONCAT('/products/img_', i, '.jpg'),
      CONCAT('テスト商品', i),
      FLOOR(5000 + RAND() * 20000), -- 購入価格 (5000〜24999)
      FLOOR(500 + RAND() * 2000), -- レンタル価格 (500〜2499)
      ELT(FLOOR(1 + RAND() * 4), 'S', 'M', 'L', 'Free'), -- サイズ
      v_upload_date, -- ★6ヶ月以内の日付
      ELT(FLOOR(1 + RAND() * 3), '公開', '非公開', '非表示'), -- ENUMからランダム
      FLOOR(RAND() * 2), -- draft (0 or 1)
      NOW(), -- updateDate (とりあえず現在日時)
      FLOOR(RAND() * 2), -- purchaseFlg
      FLOOR(RAND() * 2), -- rentalFlg
      CONCAT('これはテスト商品', i, 'の説明文です。とても良い状態です。'),
      v_account_id,
      v_brand_id,
      v_category_id,
      'クリーニング済みです。',
      FLOOR(RAND() * 2) -- smokingFlg (0 or 1)
    );
    
    SET i = i + 1;
  END WHILE;
  
END$$

-- デリミタを元に戻す
DELIMITER ;

-- ストアドプロシージャの実行
CALL sp_insert_test_products();

-- ストアドプロシージャの削除
DROP PROCEDURE sp_insert_test_products;


