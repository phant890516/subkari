drop database if exists db_subkari;

-- データベース作成
create database db_subkari
default character set utf8;

use db_subkari



-- テーブル作成 
-- アカウントテーブル ------------------------------
CREATE TABLE `m_account` (
  `id` INT AUTO_INCREMENT NOT NULL,
  `username` VARCHAR(12) NOT NULL,
  `birthday` DATE NOT NULL,
  `tel` VARCHAR(20) NOT NULL,
  `mail` VARCHAR(255) NOT NULL,
  `smoker` boolean NOT NULL,
  `introduction` TEXT  ,
  `money` INT,
  `created_at` timestamp default current_timestamp,
  `updateDate` timestamp default current_timestamp on update current_timestamp,
  `status` ENUM('未確認','本人確認済み','凍結','削除','強制削除') NOT NULL,
  `updaterId` INT,
  `password` VARCHAR(255) NOT NULL,
  `identifyfrontImg` varchar(255) NOT NULL,
  `identifybackImg` VARCHAR(255) NOT NULL,
  `apiFavoriteAnnounce` boolean,
  `apiFollowAnnounce` boolean,
  `apiSystemAnnounce` boolean,
  `mailFavoriteAnnounce` boolean,
  `mailFollowAnnounce` boolean,
  `mailSystemAnnounce` boolean,
  `autoLogin` boolean,
  `lastName` VARCHAR(50) NOT NULL,
  `firstName` VARCHAR(50) NOT NULL,
  `lastNameKana` VARCHAR(50) NOT NULL,
  `firstNameKana` VARCHAR(50) NOT NULL,
  `profileImage` VARCHAR(255) NOT NULL,


  
  PRIMARY KEY (`id`)
);

-- 住所テーブル -----------------------------------
CREATE TABLE `m_address` (
  `id` INT AUTO_INCREMENT NOT NULL,
  `account_id` INT NOT NULL,
  `zip` CHAR(7) NOT NULL,
  `pref` VARCHAR (10) NOT NULL,
  `address1` VARCHAR(20) NOT NULL,
  `address2` VARCHAR(20) NOT NULL,
  `address3` VARCHAR(40) NULL,
  
  PRIMARY KEY (`id`,`account_id`),
  FOREIGN KEY (`account_id`)
    REFERENCES `m_account`(`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE
);

-- ブランドテーブル -------------------------------------
CREATE TABLE `m_brand` (
  `id` INT AUTO_INCREMENT NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  
  PRIMARY KEY (`id`)
);

-- カテゴリテーブル -------------------------------------
CREATE TABLE `m_category` (
  `id` INT AUTO_INCREMENT NOT NULL,
  `name` VARCHAR(255) NOT NULL,

  PRIMARY KEY (`id`)
);

-- 商品テーブル ------------------------------------
CREATE TABLE `m_product` (
  `id` INT AUTO_INCREMENT NOT NULL,
  `name` VARCHAR(255) ,
  `purchasePrice` INT NULL,
  `rentalPrice` INT NULL,
  `size` VARCHAR(255) ,
  `color` ENUM('ブラック','ホワイト','イエロー','グレー','ブラウン','グリーン','ブルー','パープル','シルバー','ピンク','レッド','オレンジ')  NULL,
  `for` ENUM('ユニセックス','レディース') ,
  `upload` DATE ,
  `showing` ENUM('公開','非公開','非表示') ,
  `draft` boolean ,
  `updateDate` DATETIME ,
  `purchaseFlg` boolean ,
  `rentalFlg` boolean ,
  `explanation` TEXT ,
  `account_id` INT ,
  `brand_id` INT ,
  `category_id` INT ,
  `cleanNotes` TEXT ,
  `smokingFlg` boolean ,
  `returnAddress` varchar(255) ,
  `condition` ENUM('取引可','取引中','売却済み'),
  `rentalPeriod` INT,


  PRIMARY KEY (`id`),
  FOREIGN KEY (`brand_id`)
    REFERENCES `m_brand`(`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  FOREIGN KEY (`category_id`)
    REFERENCES `m_category`(`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  FOREIGN KEY (`account_id`)
    REFERENCES `m_account`(`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE
);



--商品写真テーブル ------------------------------------
CREATE TABLE `m_productImg` (
  `id` INT AUTO_INCREMENT NOT NULL,
  `product_id` INT NOT NULL,
  `img` VARCHAR(255) NOT NULL,
  
  PRIMARY KEY (`id`),
  FOREIGN KEY (`product_id`)
    REFERENCES `m_product`(`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE
);


-- 洗濯表示テーブル --------------------------------------------
CREATE TABLE `m_cleanSign` (
  `id` INT AUTO_INCREMENT NOT NULL,
  `cleanName` VARCHAR(255) NOT NULL,
  `cleanImg` VARCHAR(255),
  `cleanDetail` TEXT,
  
  PRIMARY KEY (`id`)
);


-- 管理者アカウントテーブル --------------------------------
CREATE TABLE `m_adminAccount` (
  `id` INT AUTO_INCREMENT NOT NULL,
  `fullName` VARCHAR(100) NOT NULL,
  `level` ENUM('administrator','operator') NOT NULL,
  `created_at` timestamp default current_timestamp ,
  `lastLogin` timestamp default current_timestamp on update current_timestamp,
  `password` VARCHAR(255) NOT NULL,
  
  PRIMARY KEY (`id`)
);


-- コンテンツテーブル ---------------------------------
CREATE TABLE `m_admin_contents` (
  `id` INT AUTO_INCREMENT NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  `content_detail` TEXT NOT NULL,                      
  `created_at` timestamp default current_timestamp ,
  `updated_at` timestamp default current_timestamp on update current_timestamp,
  
  
  PRIMARY KEY (`id`)
);



-- トップステーブル --------------------------------
CREATE TABLE `m_topsSize` (
  `product_id` INT NOT NULL,
  `shoulderWidth` DECIMAL(5,2) NOT NULL,
  `bodyWidth` DECIMAL(5,2) NOT NULL,
  `sleeveLength` DECIMAL(5,2) NOT NULL,
  `bodyLength` DECIMAL(5,2) NOT NULL,
  `notes` VARCHAR(255) ,

  PRIMARY KEY (`product_id`),
  FOREIGN KEY (`product_id`)
    REFERENCES `m_product`(`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE
);

-- ボトムステーブル --------------------------------
CREATE TABLE `m_bottomsSize` (
  `product_id` INT NOT NULL,
  `hip` DECIMAL(5,2) NOT NULL,
  `totalLength` DECIMAL(5,2) NOT NULL,
  `rise` DECIMAL(5,2) NOT NULL,
  `inseam` DECIMAL(5,2) NOT NULL,
  `waist` DECIMAL(5,2) NOT NULL,
  `thighWidth` DECIMAL(5,2) NOT NULL,
  `hemWidth` DECIMAL(5,2) NOT NULL,
  `skirtLength` DECIMAL(5,2) NOT NULL,
  `notes` VARCHAR(255),

  PRIMARY KEY (`product_id`),
  FOREIGN KEY (`product_id`)
    REFERENCES `m_product`(`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE
);

-- ログインテーブル --------------------------------
CREATE TABLE `t_login` (
  `id` INT AUTO_INCREMENT NOT NULL,
  `account_id` INT NOT NULL,
  `loginDatetime` DATETIME NULL,
  `logoutDatetime` DATETIME NULL,
  `notice` boolean,
  `flag` boolean ,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`account_id`)
    REFERENCES `m_account`(`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE
);

-- 管理者ログインテーブル --------------------------------
CREATE TABLE `t_adminLogin` (
  `id` INT AUTO_INCREMENT NOT NULL,
  `adminAccount_id` INT NOT NULL,
  `loginDatetime` DATETIME,
  `logoutDatetime` DATETIME,
  `flag` tinyint not null,

  PRIMARY KEY (`id`),
  FOREIGN KEY (`adminAccount_id`)
    REFERENCES `m_adminAccount`(`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE
);
-- レンタル期間テーブル ---------------------------------------
-- CREATE TABLE `t_rentalPeriod` (
--   `id` INT AUTO_INCREMENT NOT NULL,
--   `product_id` INT NOT NULL,
--   `rentalPeriod` ENUM('4日','7日','14日')  NOT NULL,

--   PRIMARY KEY (`id`),
--   FOREIGN KEY (`product_id`)
--     REFERENCES `m_product`(`id`)
--     ON DELETE RESTRICT ON UPDATE CASCADE
-- );

-- お気に入りテーブル --------------------------------
CREATE TABLE `t_favorite` (
  `id` INT AUTO_INCREMENT NOT NULL,
  `account_id` INT NOT NULL,
  `product_id` INT,
  `brand_id` INT,
  `resisterTime` timestamp default current_timestamp ,
  
  PRIMARY KEY (`id`),
  FOREIGN KEY (`account_id`)
    REFERENCES `m_account`(`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  FOREIGN KEY (`product_id`)
    REFERENCES `m_product`(`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  FOREIGN KEY (`brand_id`)
    REFERENCES `m_brand`(`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE
);

-- 振り込みテーブル --------------------------------
CREATE TABLE `t_transfer` (
  `id` INT AUTO_INCREMENT NOT NULL,
  `account_id` INT NOT NULL,
  `bankName` VARCHAR(100) NOT NULL,
  `accountType` VARCHAR(20) NOT NULL,
  `branchCode` CHAR(3) NOT NULL,
  `accountNumber` VARCHAR(20) NOT NULL,
  `accountHolder` VARCHAR(20) NOT NULL,
  
  PRIMARY KEY (`id`),
  FOREIGN KEY (`account_id`)
    REFERENCES `m_account`(`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE
);

-- クレジットカードテーブル --------------------------------
CREATE TABLE `t_creditCard` (
  `id` INT AUTO_INCREMENT NOT NULL,
  `account_id` INT NOT NULL,
  `number` VARCHAR(20) NOT NULL,
  `expiry` CHAR(5) NOT NULL,                             
  `holderName` VARCHAR(100) NOT NULL,
  
  PRIMARY KEY (`id`),
  FOREIGN KEY (`account_id`)
    REFERENCES `m_account`(`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE
);

-- 取引テーブル ---------------------------------
CREATE TABLE `t_transaction` (
  `id` INT AUTO_INCREMENT NOT NULL,
  `product_id` INT NOT NULL,
  `customer_id` INT NOT NULL,
  `seller_id` INT NOT NULL,
  `status` ENUM('支払い待ち','発送待ち','配達中','到着','レンタル中','クリーニング期間','返送待ち','返送中','取引完了') NOT NULL,
  `situation` ENUM('購入','レンタル') NOT NULL,
  `paymentMethod` ENUM('クレジットカード','PayPay','コンビニ払い') NOT NULL,
  `date` timestamp default current_timestamp ,
  `paymentDeadline` DATETIME NOT NULL,
  `shippingAddress` VARCHAR(255) NOT NULL,
  `shippingPhoto` VARCHAR(255),
  `shippingFlg` boolean NOT NULL,
  `receivedPhoto` VARCHAR(255),
  `receivedFlg` boolean NOT NULL,
  `cleaningPhoto` VARCHAR(255),
  `cleaningFlg` boolean NOT NULL,
  `rentalPeriod` INT,
  `creditcard_id` INT ,

  PRIMARY KEY (`id`),
  FOREIGN KEY (`product_id`)
    REFERENCES `m_product`(`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  FOREIGN KEY (`customer_id`)
    REFERENCES `m_account`(`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  FOREIGN KEY (`seller_id`)
    REFERENCES `m_account`(`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  FOREIGN KEY (`creditcard_id`)
    REFERENCES `t_creditcard`(`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE
);
-- 履歴テーブル --------------------------------
CREATE TABLE `t_history` (
  `id` INT AUTO_INCREMENT NOT NULL,
  `account_id` INT NOT NULL,
  `transaction_id` INT,
  `product_id` INT,
  `datetime` timestamp default current_timestamp,

  PRIMARY KEY (`id`),
  FOREIGN KEY (`account_id`)
    REFERENCES `m_account`(`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  FOREIGN KEY (`transaction_id`)
    REFERENCES `t_transaction`(`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  FOREIGN KEY (`product_id`)
    REFERENCES `m_product`(`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE
);

-- コメントテーブル --------------------------------
CREATE TABLE `t_comments` (
  `id` INT AUTO_INCREMENT NOT NULL,
  `account_id` INT NOT NULL,
  `content` TEXT NOT NULL,
  `createdDate` timestamp default current_timestamp ,
  `product_id` INT ,
  
  PRIMARY KEY (`id`),
  FOREIGN KEY (`account_id`)
    REFERENCES `m_account`(`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  FOREIGN KEY (`product_id`)
    REFERENCES `m_product`(`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE
);

-- コネクションテーブル --------------------------------
CREATE TABLE `t_connection` (
  `id` INT AUTO_INCREMENT NOT NULL,
  `execution_id` INT NOT NULL,
  `target_id` INT NOT NULL,
  `Datetime` timestamp default current_timestamp ,
  `type` ENUM('フォロー', 'ブロック') NOT NULL,

  PRIMARY KEY (`id`),
  FOREIGN KEY (`execution_id`)
    REFERENCES `m_account`(`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  FOREIGN KEY (`target_id`)
    REFERENCES `m_account`(`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE
);


-- アラートテーブル --------------------------------
CREATE TABLE `t_alert` (
  `id` INT AUTO_INCREMENT NOT NULL,
  `product_id` INT,
  `content` TEXT ,
  `category` ENUM ('通報','警告') ,
  `reportDate` datetime , 
  `comment_id` INT,
  `sender_id` INT,
  `recipient_id` INT,
  `transaction_id` INT,
  `adminAccount_id` INT,
  `manageDate` DATETIME,
  `reportMemo` TEXT,
  `situation` ENUM('未対応','対応中','対応済み'),
  `reportType` ENUM('商品','ユーザー','取引','その他'),
  PRIMARY KEY (`id`),
  FOREIGN KEY (`sender_id`)
    REFERENCES `m_account`(`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  FOREIGN KEY (`comment_id`)
    REFERENCES `t_comments`(`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  FOREIGN KEY (`transaction_id`)
    REFERENCES `t_transaction`(`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  FOREIGN KEY (`adminAccount_id`)
    REFERENCES `m_adminAccount`(`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  FOREIGN KEY (`recipient_id`)
    REFERENCES `m_account`(`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE
);





-- 取引メッセージ ------------------------------------
CREATE TABLE `t_message` (
  `id` INT AUTO_INCREMENT NOT NULL,
  `sender_id` INT NOT NULL,
  `recipient_id` INT NOT NULL,
  `transaction_id` INT NOT NULL,
  `content` VARCHAR(255) NOT NULL,
  `sendingTime` timestamp default current_timestamp ,
  `readStatus` boolean NOT NULL,

  PRIMARY KEY (`id`),
  FOREIGN KEY (`sender_id`)
    REFERENCES `m_account`(`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  FOREIGN KEY (`recipient_id`)
    REFERENCES `m_account`(`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  FOREIGN KEY (`transaction_id`)
    REFERENCES `t_transaction`(`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE
);


-- 評価テーブル ---------------------------------------
CREATE TABLE `t_evaluation` (
  `id` INT AUTO_INCREMENT NOT NULL,
  `transaction_id` INT NOT NULL,
  `score` INT NOT NULL,
  `comment` TEXT ,
  `evaluationTime` timestamp default current_timestamp ,
  `productCheck` boolean NOT NULL,
  `recipient_id` INT NOT NULL,

  

  PRIMARY KEY (`id`),
  FOREIGN KEY (`transaction_id`)
    REFERENCES `t_transaction`(`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (`recipient_id`)
    REFERENCES `m_account`(`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE
);


-- 洗濯テーブル --------------------------------------------
CREATE TABLE `t_clean` (
  `product_id` INT NOT NULL,
  `cleanSign_id` INT NOT NULL,

  PRIMARY KEY (`product_id`,`cleanSign_id`),
  FOREIGN KEY (`product_id`)
    REFERENCES `m_product`(`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (`cleanSign_id`)
    REFERENCES `m_cleanSign`(`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE
);


-- お問い合わせテーブル ------------------------------------------
CREATE TABLE `t_inquiry` (
  `id` INT AUTO_INCREMENT NOT NULL,
  `sender_id` INT NOT NULL,
  `content` TEXT NOT NULL,
  `timeSent` timestamp default current_timestamp ,
  `product_id` INT,
  `adminAccount_id` INT,
  `replyDetail` TEXT NOT NULL,
  `replyDate` DATETIME ,
  `situation` ENUM('未対応','対応中','対応済み'),

  PRIMARY KEY (`id`),
  FOREIGN KEY (`sender_id`)
    REFERENCES `m_account`(`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  FOREIGN KEY (`product_id`)
    REFERENCES `m_product`(`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  FOREIGN KEY (`adminAccount_id`)
    REFERENCES `m_adminAccount`(`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE
);



-- タイムテーブル ------------------------------------------

CREATE TABLE `t_time` (
  `id` INT AUTO_INCREMENT NOT NULL,
  `account_id` INT NOT NULL,
  `login_id` INT NULL,
  `comments_id` INT NULL,
  `alert_id` INT NULL,
  `product_id` INT NULL,
  `message_id` INT NULL,
  `inquiry_id` INT NULL,
  `transaction_id` INT NULL,
  `transaction_status` ENUM('支払い待ち','発送待ち','配達中','到着','レンタル中','クリーニング期間','取引完了') NULL,
  `evaluation_id` INT NULL,
  `product_change` ENUM('料金変更','取引状態遷移','コメント') NULL,

  `created_at`
  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

  PRIMARY KEY (`id`),
  FOREIGN KEY (`account_id`)
    REFERENCES `m_account`(`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,

  FOREIGN KEY (`login_id`)
    REFERENCES `t_login`(`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,

      FOREIGN KEY (`comments_id`)
    REFERENCES `t_comments`(`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,

      FOREIGN KEY (`alert_id`)
    REFERENCES `t_alert`(`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,

      FOREIGN KEY (`product_id`)
    REFERENCES `m_product`(`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,

      FOREIGN KEY (`message_id`)
    REFERENCES `t_message`(`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,

      FOREIGN KEY (`inquiry_id`)
    REFERENCES `t_inquiry`(`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,

          FOREIGN KEY (`transaction_id`)
    REFERENCES `t_transaction`(`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE,

          FOREIGN KEY (`evaluation_id`)
    REFERENCES `t_evaluation`(`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE
);


--  トリガー作成 ----------------------------------------------------------------



-- トリガー作成: t_loginに新しい行が挿入された後にt_timeにデータを挿入するトリガー
-- 文末記号を ; から // に変更します
DELIMITER //

CREATE TRIGGER trg_after_insert_login
    AFTER INSERT ON t_login
    FOR EACH ROW
BEGIN
    -- t_timeテーブルに、今挿入された行の情報をINSERTします
    INSERT INTO t_time (
        account_id,  -- ログインした人のID
        login_id     -- 関連するt_loginのID
    )
    VALUES (
        NEW.account_id,  -- 今t_loginに挿入された行の account_id
        NEW.id           -- 今t_loginに挿入された行の id (主キー)
    );
END;
//

-- 文末記号を // から ; に戻します
DELIMITER ;


-- トリガー作成: t_commentsに新しい行が挿入された後にt_timeにデータを挿入するトリガー
-- 文末記号を ; から // に変更します
DELIMITER //

CREATE TRIGGER `trg_notify_favorite_users_on_comment`
AFTER INSERT ON `t_comments`
FOR EACH ROW
BEGIN
    
    -- t_timeテーブルにデータを挿入する
    -- INSERT ... SELECT 構文を使用し、
    -- t_favoriteテーブルから「NEW.product_id（今回コメントがついた商品ID）」を
    -- お気に入り登録している全ての「account_id」を取得し、その人たちの分の行を挿入する
    
    INSERT INTO `t_time` (
        `account_id`,       -- お気に入り登録している人のID
        `comments_id`,      -- 新しく挿入されたコメントのID
        `product_id`,       -- コメントがついた商品のID
        `product_change`    -- 変更の種類
    )
    SELECT
        tf.account_id,      -- お気に入り登録しているユーザーのID
        NEW.id,             -- 挿入された新しいコメントのID
        NEW.product_id,     -- コメントされた商品のID
        'コメント'            -- 変更種別
    FROM
        `t_favorite` AS tf
    WHERE
        tf.product_id = NEW.product_id  -- コメントされた商品IDと一致するお気に入りを探す
        
        -- （推奨）コメントした本人には通知しない場合
        AND tf.account_id != NEW.account_id;

END//

-- 文末記号を // から ; に戻します
DELIMITER ;



-- トリガー作成: m_productの価格が変更された後にt_timeにデータを挿入するトリガー
-- デリミタ（文の終わりを示す記号）を ; から $$ に一時的に変更します
DELIMITER $$

CREATE TRIGGER `trg_product_price_change`
AFTER UPDATE ON `m_product`
FOR EACH ROW
BEGIN

    -- 変更前(OLD)と変更後(NEW)の価格を比較します
    -- (NULL<=>NULL は TRUE になるため、NOT (<=>) で NULL <-> 値 の変更も検知します)
    
    IF NOT (NEW.purchasePrice <=> OLD.purchasePrice) OR 
       NOT (NEW.rentalPrice <=> OLD.rentalPrice) THEN
        
        -- purchasePrice または rentalPrice のどちらかが変更されていた場合、
        -- t_time テーブルにデータを挿入します
        
        INSERT INTO `t_time` (
            `account_id`,       -- 商品の所有者のID (t_timeでNOT NULLのため)
            `product_id`,       -- 変更された商品のID
            `product_change`    -- 変更内容
        )
        VALUES (
            NEW.account_id,     -- m_product の account_id を設定
            NEW.id,             -- 変更された商品のID
            '料金変更'
        );
        
    END IF;
    
END$$

-- デリミタを $$ から ; に戻します
DELIMITER ;


-- トリガー作成: t_transactionのstatusが変更された後にt_timeにデータを挿入するトリガー
-- デリミタ（文の終わりを示す記号）を ; から $$ に一時的に変更します
DELIMITER $$

CREATE TRIGGER `trg_transaction_status_change`
AFTER UPDATE ON `t_transaction`
FOR EACH ROW
BEGIN

    -- 変更前(OLD)と変更後(NEW)のstatusが異なる場合のみ実行
    IF OLD.status != NEW.status THEN
    
        -- 【1】購入者 (customer_id) の t_time テーブルに挿入
        INSERT INTO `t_time` (
            `account_id`,       -- 購入者のID
            `transaction_id`,   -- 変更があった取引のID
            `transaction_status`, -- ★ 変更前のステータス
            `product_change`    -- 変更内容
        )
        VALUES (
            NEW.customer_id,    -- 更新後の行の customer_id
            NEW.id,             -- 更新された取引の ID
            OLD.status,         -- ★ 変更前の status
            '取引状態遷移'
        );
        
        -- 【2】販売者 (seller_id) の t_time テーブルにも挿入
        -- (もし購入者と販売者が同じIDの場合は、重複挿入を避ける)
        IF NEW.customer_id != NEW.seller_id THEN
            INSERT INTO `t_time` (
                `account_id`,       -- 販売者のID
                `transaction_id`,   -- 変更があった取引のID
                `transaction_status`, -- ★ 変更前のステータス
                `product_change`    -- 変更内容
            )
            VALUES (
                NEW.seller_id,      -- 更新後の行の seller_id
                NEW.id,             -- 更新された取引の ID
                OLD.status,         -- ★ 変更前の status
                '取引状態遷移'
            );
        END IF;
        
    END IF;
    
END$$

-- デリミタを $$ から ; に戻します
DELIMITER ;

-- トリガー作成: t_messageに新しい行が挿入された後にt_timeにデータを挿入するトリガー
-- デリミタ（文の終わりを示す記号）を ; から $$ に一時的に変更します
DELIMITER $$

CREATE TRIGGER `trg_message_to_timeline`
AFTER INSERT ON `t_message`
FOR EACH ROW
BEGIN
    
    -- t_message に新しい行が挿入されたら、
    -- そのメッセージの「受信者(recipient_id)」の t_time テーブルにレコードを挿入します
    
    INSERT INTO `t_time` (
        `account_id`,       -- ★ メッセージ受信者のID
        `message_id`,       -- 新しいメッセージのID
        `transaction_id`    -- 関連する取引のID
    )
    VALUES (
        NEW.recipient_id,   -- 挿入されたメッセージの受信者ID
        NEW.id,             -- 挿入されたメッセージのID
        NEW.transaction_id  -- 挿入されたメッセージの取引ID
    );

END$$

-- デリミタを $$ から ; に戻します
DELIMITER ;


-- トリガー作成: t_inquiryのadminAccount_idがNULLからNOT NULLに更新された後にt_timeにデータを挿入するトリガー
-- デリミタを $$ に変更
DELIMITER $$

CREATE TRIGGER `trg_inquiry_admin_assigned_update`
AFTER UPDATE ON `t_inquiry`
FOR EACH ROW
BEGIN
    -- adminAccount_id が NULL から NOT NULL に変更されたかチェック
    -- (更新前のOLDがNULL かつ 更新後のNEWがNULLでない)
    IF OLD.adminAccount_id IS NULL AND NEW.adminAccount_id IS NOT NULL THEN
    
        -- 送信者 (sender_id) の t_time テーブルに挿入
        INSERT INTO `t_time` (
            `account_id`,   -- 送信者のID
            `inquiry_id`,
            `product_id`
        )
        VALUES (
            NEW.sender_id,  -- t_time.account_id = t_inquiry.sender_id
            NEW.id,
            NEW.product_id
        );
        
    END IF;
END$$


-- デリミタを ; に戻す
DELIMITER ;

-- トリガー作成: t_evaluationに新しい行が挿入された後にt_timeにデータを挿入するトリガー
-- デリミタ（文の終わりを示す記号）を ; から $$ に一時的に変更します
DELIMITER $$

CREATE TRIGGER `trg_evaluation_to_timeline`
AFTER INSERT ON `t_evaluation`
FOR EACH ROW
BEGIN
    
    -- t_evaluation に新しい行が挿入されたら、
    -- その評価の「受信者(recipient_id)」の t_time テーブルにレコードを挿入します
    
    INSERT INTO `t_time` (
        `account_id`,       -- ★ 評価「された」人 (受信者) のID
        `evaluation_id`,    -- 新しい評価のID
        `transaction_id`    -- 関連する取引のID
    )
    VALUES (
        NEW.recipient_id,   -- 挿入された評価の受信者ID
        NEW.id,             -- 挿入された評価のID
        NEW.transaction_id  -- 挿入された評価の取引ID
    );

END$$

-- デリミタを $$ から ; に戻します
DELIMITER ;


-- トリガー作成: t_alertに新しい行が挿入された後にt_timeにデータを挿入するトリガー
-- デリミタ（文の終わりを示す記号）を ; から $$ に一時的に変更します
DELIMITER $$

CREATE TRIGGER `trg_alert_warning_to_timeline`
AFTER INSERT ON `t_alert`
FOR EACH ROW
BEGIN
    
    -- 挿入された行（NEW）の category が '警告' 
    -- かつ、t_time の必須カラム account_id に相当する recipient_id が NULL でないことをチェック
    
    IF NEW.category = '警告' AND NEW.recipient_id IS NOT NULL THEN
    
        -- 条件を満たした場合、t_time テーブルにデータを挿入
        INSERT INTO `t_time` (
            `account_id`,   -- 警告の対象となったアカウントID (受信者)
            `alert_id`      -- 挿入された t_alert の ID
        )
        VALUES (
            NEW.recipient_id, -- t_alert テーブルの recipient_id
            NEW.id            -- t_alert テーブルの id
        );
        
    END IF;
    
END$$

-- デリミタを $$ から ; に戻します
DELIMITER ;




--  ビュー作成 ----------------------------------------------------------------
CREATE VIEW v_notice AS 
SELECT
    -- (1) 主役となる t_time のカラム
    ttm.created_at,  -- (並び替えの基準)
    ttm.transaction_status,
    ttm.product_change,

    -- (2) t_transaction (取引) のカラム
    ttr.date AS transaction_date,
    ttr.paymentDeadline,
    ttr.rentalPeriod,
    
    -- (3) t_alert (アラート) のカラム
    ta.category AS alert_category,
    
    -- (4) m_product (商品) のカラム
    mp.purchasePrice,
    mp.rentalPrice,
    
    -- (5) m_account (ユーザー) のカラム
    ma.id AS user_account_id,
    
    -- (6) どのイベントかを識別するためのID (デバッグ・処理分岐用)
    ttm.id AS time_id,
    ttm.transaction_id,
    ttm.alert_id,
    ttm.comments_id,
    ttm.product_id

FROM
    t_time AS ttm  -- (A) 主役のテーブル

-- (B) ユーザー情報を結合
LEFT JOIN
    m_account AS ma ON ttm.account_id = ma.id

-- (C) 取引情報を結合
LEFT JOIN
    t_transaction AS ttr ON ttm.transaction_id = ttr.id

-- (D) アラート情報を結合 (t_time の alert_id が t_alert の id を参照すると仮定)
LEFT JOIN
    t_alert AS ta ON ttm.alert_id = ta.id

-- (E) コメント情報を結合 (前回のテーブル定義より)
LEFT JOIN
    t_comments AS tc ON ttm.comments_id = tc.id

-- (F) 商品情報を結合 (※最重要ポイント)
LEFT JOIN
    m_product AS mp ON ttm.product_id = mp.id
WHERE
    -- (G) 特定のユーザーの通知一覧を指定
    ttm.account_id = 123  -- (例: ログイン中のユーザーIDが123)

ORDER BY
    -- (H) 時系列順 (新しい順) に並び替え
    ttm.created_at DESC
;


-- ダッシュボード ---------------------------------------------------
-- 今週の新規ユーザー数  
create view v_weekly_new_users
 as
select  count(*) as 今週の新規ユーザー数
from m_account
where datediff(date_sub(curdate(),interval(weekday(curdate())) day),created_at)<7
;

-- 新規ユーザー数先週比 
create view v_compare_1_week_ago_new_users
as
SELECT
  ROUND(

    SUM(CASE WHEN YEARWEEK(created_at, 1) = YEARWEEK(CURDATE(), 1) THEN 1 ELSE 0 END)

    / NULLIF(SUM(CASE WHEN YEARWEEK(created_at, 1) = YEARWEEK(CURDATE(), 1) - 1 THEN 1 ELSE 0 END), 0)

    * 100, 1

  ) AS 先週比

FROM m_account;

-- WL
create view v_weekly_listing
as
select  count(*) as 今週の出品数
from m_product
where datediff(date_sub(curdate(),interval(weekday(curdate())) day),upload)<7
;

-- WL先週比  qqq
create view v_compare_1_week_ago_listing
as
SELECT
  ROUND(

    SUM(CASE WHEN YEARWEEK(upload, 1) = YEARWEEK(CURDATE(), 1) THEN 1 ELSE 0 END)

    / NULLIF(SUM(CASE WHEN YEARWEEK(upload, 1) = YEARWEEK(CURDATE(), 1) - 1 THEN 1 ELSE 0 END), 0)

    * 100, 1

  ) AS 先週比
from m_product
;

-- WAU 
create view v_weekly_active_users
as
select  count(*) as 今週のアクティブユーザー数
from t_login
where datediff(date_sub(curdate(),interval(weekday(curdate())) day),loginDatetime)<7
;

-- MAU 
create view v_monthly_active_users
as
select 
date_format(loginDatetime,'%Y-%m') as  month,count(distinct account_id) as MAU
from t_login
where loginDatetime>=date_format(date_sub(curdate(),interval 6 month),'%Y-%m-01')
group by month
order by month; 



-- 通報未対応 
create view v_alert_unchecked
as
select count(*) as 未対応通報
from t_alert
where category='通報' and situation = '未対応'
;
-- お問い合わせ未対応 
create view v_inquiry_unchecked
as
select count(*)
from t_inquiry
where situation = '未対応'
;
-- 本人確認依頼 00
create view v_identify_offer
as
select count(*)
from m_account
where  status='未確認'
;



-- 地域別ユーザー数 
create view v_region_new_users
as
SELECT
  DATE_FORMAT(created_at, '%Y-%m') AS month,
  SUM(CASE WHEN region = '北海道' THEN 1 ELSE 0 END) AS 北海道,
  SUM(CASE WHEN region = '東北' THEN 1 ELSE 0 END) AS 東北,
  SUM(CASE WHEN region = '関東' THEN 1 ELSE 0 END) AS 関東,
  SUM(CASE WHEN region = '中部' THEN 1 ELSE 0 END) AS 中部,
  SUM(CASE WHEN region = '近畿' THEN 1 ELSE 0 END) AS 近畿,
  SUM(CASE WHEN region = '中国' THEN 1 ELSE 0 END) AS 中国,
  SUM(CASE WHEN region = '四国' THEN 1 ELSE 0 END) AS 四国,
  SUM(CASE WHEN region = '九州' THEN 1 ELSE 0 END) AS 九州
FROM (
  SELECT
    a.id,
    a.created_at,
    CASE
      WHEN addr.pref = '北海道' THEN '北海道'
      WHEN addr.pref IN ('青森県','岩手県','宮城県','秋田県','山形県','福島県') THEN '東北'
      WHEN addr.pref IN ('茨城県','栃木県','群馬県','埼玉県','千葉県','東京都','神奈川県') THEN '関東'
      WHEN addr.pref IN ('新潟県','富山県','石川県','福井県','山梨県','長野県','岐阜県','静岡県','愛知県') THEN '中部'
      WHEN addr.pref IN ('三重県','滋賀県','京都府','大阪府','兵庫県','奈良県','和歌山県') THEN '近畿'
      WHEN addr.pref IN ('鳥取県','島根県','岡山県','広島県','山口県') THEN '中国'
      WHEN addr.pref IN ('徳島県','香川県','愛媛県','高知県') THEN '四国'
      WHEN addr.pref IN ('福岡県','佐賀県','長崎県','熊本県','大分県','宮崎県','鹿児島県','沖縄県') THEN '九州'
      ELSE '不明'
    END AS region
  FROM
    m_account a
    INNER JOIN m_address addr ON a.id = addr.account_id
  WHERE a.status not in('削除','強制削除') and
  created_at >= DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL 6 MONTH), '%Y-%m-01')
) AS region_data
GROUP BY
  DATE_FORMAT(created_at, '%Y-%m')
ORDER BY
  month;


-- 年代別新規ユーザー数 
create view v_age_group_new_users
as
SELECT
  DATE_FORMAT(a.created_at, '%Y-%m') AS month,
  SUM(CASE WHEN TIMESTAMPDIFF(YEAR, a.birthday, CURDATE()) < 20 THEN 1 ELSE 0 END) AS "0〜19歳",
  SUM(CASE WHEN TIMESTAMPDIFF(YEAR, a.birthday, CURDATE()) BETWEEN 20 AND 29 THEN 1 ELSE 0 END) AS "20代",
  SUM(CASE WHEN TIMESTAMPDIFF(YEAR, a.birthday, CURDATE()) BETWEEN 30 AND 39 THEN 1 ELSE 0 END) AS "30代",
  SUM(CASE WHEN TIMESTAMPDIFF(YEAR, a.birthday, CURDATE()) BETWEEN 40 AND 49 THEN 1 ELSE 0 END) AS "40代",
  SUM(CASE WHEN TIMESTAMPDIFF(YEAR, a.birthday, CURDATE()) BETWEEN 50 AND 59 THEN 1 ELSE 0 END) AS "50代",
  SUM(CASE WHEN TIMESTAMPDIFF(YEAR, a.birthday, CURDATE()) >= 60 THEN 1 ELSE 0 END) AS "60代以上"
FROM
  m_account a
where status not in("削除","強制削除")
  AND a.created_at >= DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL 6 MONTH), '%Y-%m-01')
GROUP BY
  month
ORDER BY
  month;

