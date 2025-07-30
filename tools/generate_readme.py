#!/usr/bin/env python3
from collections import defaultdict
from typing import List, Dict
from bookshelf_core import load_books, CATEGORY_ORDER, README_MD

def generate_readme() -> None:
    """books.csvから元の形式のREADME.mdを生成"""
    
    # CSVを読み込み
    books = load_books()
    
    # カテゴリ別にグループ化
    categories: defaultdict[str, List[Dict[str, str]]] = defaultdict(list)
    for book in books:
        categories[book['CATEGORY']].append(book)
    
    category_order = CATEGORY_ORDER
    
    # README.md生成
    content: List[str] = []
    content.append("# mybookshelf")
    content.append("")
    content.append("購入した本を一覧化する。")
    content.append("")
    
    for category_name, emoji in category_order:
        if category_name in categories:
            books_in_category = categories[category_name]
            
            content.append(f"## {emoji} {category_name}")
            content.append("")
            content.append("|NAME|LANG|TYPE|STATUS|MEMO|")
            content.append("|:---|:---|:---|:---|:---|")
            
            for book in books_in_category:
                name = book['NAME']
                lang = book['LANG']
                book_type = book['TYPE']
                status = book['STATUS']
                memo = book['MEMO']
                content.append(f"|{name}|{lang}|{book_type}|{status}|{memo}|")
            
            content.append("")
    
    # ファイルに書き出し
    with open(README_MD, 'w', encoding='utf-8') as f:
        f.write('\n'.join(content))
    
    total_books = len(books)
    total_categories = len([cat for cat, _ in category_order if cat in categories])
    print(f"README.md生成完了: {total_categories}カテゴリ、{total_books}冊")

if __name__ == "__main__":
    generate_readme()