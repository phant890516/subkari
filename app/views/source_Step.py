# -----------------------------------------------------------------------------
# ソースステップカウンタ
# Python/HTML/CSS/JavaScript/C++のコード数を出力します。
# トップフォルダのパスを指定すると、それ配下のコードを検索し、カウントします。
# １行の中に命令コードとコメントがある場合
# 命令コード１行+コメントコード1行とカウントする。
# Pythonのprint文でHTMLが出力されている場合、Pythonコードとしてカウントする。
# 他の言語も同様のカウント考え方。
# -----------------------------------------------------------------------------
# 2025/11/21    新規作成                            桝井　隆治
# -----------------------------------------------------------------------------

import os
import sys

# -----------------------------------------------------------------------------
# 内部設定
# -----------------------------------------------------------------------------

# 集計データ -------------------------------------------------------------------
stats = {
    "python":     {"files": 0, "total": 0, "exec": 0, "comment": 0},
    "HTML":       {"files": 0, "total": 0, "exec": 0, "comment": 0},
    "CSS":        {"files": 0, "total": 0, "exec": 0, "comment": 0},
    "JavaScript": {"files": 0, "total": 0, "exec": 0, "comment": 0},
    "C":          {"files": 0, "total": 0, "exec": 0, "comment": 0}, 
    "C++":        {"files": 0, "total": 0, "exec": 0, "comment": 0},
}

# 拡張子の定義 -----------------------------------------------------------------
EXTENSIONS = {
    "python":     [".py"],
    "HTML":       [".html", ".htm"],
    "CSS":        [".css"],
    "JavaScript": [".js"],
    "C++":        [".cpp", ".cc", ".cxx", ".hpp", ".h", ".c"], 
}

# コメント構文の定義 -----------------------------------------------------------
SYNTAX = {
    "python":     ("#",  ['"""', "'''"], ['"""', "'''"]),
    "C++":        ("//", ["/*"], ["*/"]),
    "JavaScript": ("//", ["/*"], ["*/"]),
    "CSS":        (None, ["/*"], ["*/"]),
    "HTML":       (None, ["<!--"], ["-->"]) 
}

# -----------------------------------------------------------------------------
# get_target_folder
# ユーザーに入力を求め、正しいフォルダパスか検証して返す
# -----------------------------------------------------------------------------
def get_target_folder():
    print("集計対象のフォルダパスを貼り付けてください:", end = "" )
    
    # コンソールからユーザー入力を受け取り、前後の空白を削除する
    input_path = input()
    
    # Windowsで「パスのコピー」された時に付与される""を削除去
    input_path = input_path.strip('"').strip("'")
    
    # Macのターミナルで稀に付与される、末尾のスペースを除去
    input_path = input_path.strip()

    # フォルダの存在確認し、パスを返却
    if not os.path.isdir(input_path):
        print(f"\nエラー: 指定されたフォルダが見つかりません。\nパス: {input_path}")
        print("正しいパスを確認して、もう一度実行してください。")
        input("終了するにはEnterキーを押してください...")
        sys.exit()
        
    return input_path

# -----------------------------------------------------------------------------
# count_lines_in_file
# 指定されたファイルの行数をカウントし、(総行数, 実行コード行数, コメント行数) を返す
# 仕様B案に基づき、空白行は総行数に含めない
# -----------------------------------------------------------------------------
def count_lines_in_file(filepath, lang_type):
    total         = 0   # 空行を除いた全行数
    exec_lines    = 0   # 実行コードが含まれる行数
    comment_lines = 0   # コメントが含まれる行数
    
    # 構文定義から「単一行記号」「ブロック開始記号」「ブロック終了記号」を取得
    try:
        single_mark, block_starts, block_ends = SYNTAX[lang_type]
    except ValueError:
        return 0, 0, 0
    
    # ブロックコメントの状態管理用フラグ設定
    in_block = False            # 現在ブロックコメントの内部にいるかどうか
    current_block_ender = None  # 現在のブロックを閉じる記号 (例: "*/" や """)

    # -------------------------------------------------------------------------
    # ステップ開始
    # -------------------------------------------------------------------------
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            
        # ファイル内の各行を1行ずつ取り出してループ処理
        for line in lines:
            # 行の前後の空白・改行を除去、判定を容易にする
            stripped = line.strip()
            
            # 空白行の場合は何もせず、次の行へ
            if not stripped:
                continue
                
            # 有効な行（空行以外）と判定、総コード行数をカウントアップし、
            # 実行コード・コメントコードの判断フラグ初期化
            total += 1  
            is_exec = False
            is_comment = False
            
            # -------------------------------------------------------
            # 現在位置がブロックコメントの中にいる場合
            # -------------------------------------------------------
            if in_block:
                is_comment = True # ブロック内は無条件でコメント行
                
                # 現在行に、ブロックを終了記号（例: */）の包含判定
                if current_block_ender in stripped:
                    in_block = False # ブロック状態を解除
                    
                    # 終了記号より後ろに処理文字があるか判定（ */ x = 1;など）
                    if not stripped.endswith(current_block_ender):
                        is_exec = True # 文字があれば実行コードも含まれるとみなす
                        
                    # 管理用変数をリセット
                    current_block_ender = None

            # -------------------------------------------------------
            # ブロックコメントの外にいる場合（通常の状態）
            # -------------------------------------------------------
            else:
                found_start = False # ブロックコメント開始フラグをOFF
                
                # ブロック開始記号（例: /*）を判定
                for start_mark, end_mark in zip(block_starts, block_ends):
                    # 行の中に開始記号が含まれている場合はコメント開始判定
                    if start_mark in stripped:
                        found_start = True
                        is_comment = True
                        
                        # 開始記号より前に処理コードが存在するか判定し、あるならカウントアップ（例: x = 1; /*）
                        if not stripped.startswith(start_mark):
                            is_exec = True # 文字があれば実行コードも含まれるとみなす
                            
                        # 同一行のでコメントが閉じているかを確認、開始記号より後ろの部分文字列を取得し
                        # 終了記号が格納されているか判定
                        after_start = stripped[stripped.find(start_mark) + len(start_mark):]
                        if end_mark in after_start:
                            # 同じ行で閉じているため、ブロック継続フラグは立てない
                            pass 
                        else:
                            # 閉じていないので、次の行以降もコメントが続くと判断
                            in_block = True
                            current_block_ender = end_mark # 何の記号で閉じるべきかを保存
                        
                        # ブロック開始が見つかったと判断し、その行のチェックは終了
                        break
                
                # 単一コメント行の判定
                if not found_start:
                    # 単一行コメント記号（例: //）が存在し、かつ行内に含まれているか判定
                    if single_mark and single_mark in stripped:
                        is_comment = True
                        
                        # コメント記号が先頭でなければ、その前は実行コードであると判定
                        # 例 : print("hi") # コメント
                        if not stripped.startswith(single_mark):
                            is_exec = True
                    else:
                        # コメント記号が一切ないので、純粋な実行コード行とみなす
                        is_exec = True
            
            # -------------------------------------------------------
            # １行集計完了、処理・コメント行数更新
            # -------------------------------------------------------
            # 実行コードフラグ
            if is_exec:
                exec_lines += 1
            # コメントフラグが
            if is_comment:
                comment_lines += 1
                
    except Exception:
        # 読み込みエラー等が発生した場合は、安全のため0を返す
        return 0, 0, 0

    # 1ファイルの全行処理が終わったら、集計結果を呼び出し元へ返す
    return total, exec_lines, comment_lines

# -----------------------------------------------------------------------------
# main
# アプリケーションエントリーポイント
# -----------------------------------------------------------------------------
def main():
    # フォルダパス取得
    target_folder = get_target_folder()
    
    print(f"\n集計中... 対象: {target_folder}\n")

    # 指定されたフォルダ以下のを再帰探索
    for root, dirs, files in os.walk(target_folder):
        # 発見したファイル一覧分ループ
        for filename in files:
            # ファイル名から拡張子を取得
            # 2つ目の戻り値(拡張子の文字列)のみ取得する為、
            # 戻り値1は捨て変数に入れている。
            _, ext = os.path.splitext(filename)
            target_lang = None

            # 拡張子の判定
            for lang, ext_list in EXTENSIONS.items():
                # 大文字小文字を区別しないよう小文字化して比較
                if ext.lower() in ext_list:
                    target_lang = lang
                    break
            
            # 集計対象の言語を発見した場合、行数カウント
            if target_lang:
                # フルパスを作成
                filepath = os.path.join(root, filename)
                
                # ファイル行数をカウント
                file_total, exec_total, cmt_total = count_lines_in_file(filepath, target_lang)
                
                # 全体の集計データ(stats)に加算する
                stats[target_lang]["files"]   += 1
                stats[target_lang]["total"]   += file_total
                stats[target_lang]["exec"]    += exec_total
                stats[target_lang]["comment"] += cmt_total

    # 全ファイル調査完了、結果を画面に出力して終了 --------------------------------
    print("ファイル名\tファイル数\t総コード数\t実行コード数\tコメント数")
    
    # 表示順序を指定して出力
    order = ["python", "HTML", "CSS", "JavaScript", "C", "C++"]
    for lang in order:
        d = stats[lang]
        print(f"{lang}\t{d['files']}\t{d['total']}\t{d['exec']}\t{d['comment']}")
    print("----------------------------------------------")
    print("\n完了しました。終了します。")

if __name__ == "__main__":
    main()
