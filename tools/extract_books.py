#!/usr/bin/env python3
import re
from bookshelf_core import save_books, FIELDNAMES, README_MD

def extract_books_from_readme():
    """現在のREADME.mdから本の情報を抽出してCSVに変換"""
    with open(README_MD, 'r', encoding='utf-8') as f:
        content = f.read()
    
    books = []
    current_category = ""
    
    # カテゴリとテーブル行を抽出
    lines = content.split('\n')
    for line in lines:
        # カテゴリヘッダーを検出
        if line.startswith('## '):
            # 絵文字を除去してカテゴリ名を抽出
            current_category = re.sub(r'^##\s*[^\s]*\s*', '', line).strip()
        
        # テーブル行を検出（|で始まり、NAME以外）
        elif line.startswith('|') and '|NAME|' not in line and '|:---|' not in line and line.count('|') >= 5:
            parts = [part.strip() for part in line.split('|')[1:-1]]  # 最初と最後の空要素を除去
            if len(parts) >= 5 and parts[0]:  # NAMEが空でない
                books.append({
                    'NAME': parts[0],
                    'CATEGORY': current_category,
                    'LANG': parts[1],
                    'TYPE': parts[2],
                    'STATUS': parts[3],
                    'MEMO': parts[4] if len(parts) > 4 else ''
                })
    
    # CSVに保存
    save_books(books)
    print(f"抽出完了: {len(books)}冊の本をdata/books.csvに保存しました")

if __name__ == "__main__":
    extract_books_from_readme()