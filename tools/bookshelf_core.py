#!/usr/bin/env python3
"""
Bookshelf Core - 共通機能を提供するモジュール
"""
import csv
import os
from typing import List, Dict
from pathlib import Path

# プロジェクトルートディレクトリ
PROJECT_ROOT = Path(__file__).parent.parent

# ファイルパス
DATA_DIR = PROJECT_ROOT / "data"
BOOKS_CSV = DATA_DIR / "books.csv"
README_MD = PROJECT_ROOT / "README.md"

# CSVフィールド名
FIELDNAMES = ['NAME', 'CATEGORY', 'LANG', 'TYPE', 'STATUS', 'MEMO']

# カテゴリ定義（表示順序と絵文字）
CATEGORY_ORDER = [
    ('システム基盤・インフラ', '📚'),
    ('プログラミング・開発', '💻'),
    ('設計・品質', '🏗️'),
    ('運用・SRE・DevOps', '🔧'),
    ('セキュリティ・テスト', '🔒'),
    ('組織・マネジメント', '👥'),
    ('キャリア・スキル', '🚀'),
    ('数学・アルゴリズム', '🧮'),
    ('AI', '🤖'),
    ('学習・資格', '📖'),
]

def load_books() -> List[Dict]:
    """CSVから本のデータを読み込み"""
    try:
        with open(BOOKS_CSV, 'r', encoding='utf-8') as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        return []

def save_books(books: List[Dict]):
    """本のデータをCSVに保存"""
    if not books:
        return
    
    # ディレクトリが存在しない場合は作成
    DATA_DIR.mkdir(exist_ok=True)
    
    with open(BOOKS_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(books)

def find_book_by_name(name_part: str) -> tuple[List[Dict], List[Dict]]:
    """
    名前の部分一致で本を検索
    Returns: (全ての本のリスト, マッチした本のリスト)
    """
    books = load_books()
    matches = [book for book in books if name_part.lower() in book['NAME'].lower()]
    return books, matches

def create_book(name: str, category: str = "", lang: str = "JPN", 
               book_type: str = "Kindle", status: str = "UNREAD", memo: str = "") -> Dict:
    """本のデータ構造を作成"""
    return {
        'NAME': name,
        'CATEGORY': category,
        'LANG': lang,
        'TYPE': book_type,
        'STATUS': status,
        'MEMO': memo
    }

def remove_book_by_name(name_part: str) -> tuple[bool, str]:
    """
    名前の部分一致で本を削除
    Returns: (成功フラグ, メッセージ)
    """
    books, matches = find_book_by_name(name_part)
    
    if not matches:
        return False, f"エラー: '{name_part}' を含む本が見つかりません"
    
    if len(matches) > 1:
        match_list = "\n".join([f"  {i+1}. {book['NAME']}" for i, book in enumerate(matches)])
        return False, f"複数の本が見つかりました:\n{match_list}"
    
    # 本を削除
    book_to_remove = matches[0]
    updated_books = [book for book in books if book['NAME'] != book_to_remove['NAME']]
    save_books(updated_books)
    
    return True, f"削除しました: {book_to_remove['NAME']}"