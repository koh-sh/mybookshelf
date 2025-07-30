#!/usr/bin/env python3
"""
Bookshelf CLI 自動テストスクリプト
"""
import subprocess
import sys
from pathlib import Path
from typing import Tuple, List
import csv

# テスト設定
TEST_BOOK_NAME = "テスト用書籍_自動テスト"
TEST_CATEGORY = "AI"
TEST_LANG = "JPN"  
TEST_TYPE = "Kindle"

# パス設定
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
BOOKSHELF_CMD = SCRIPT_DIR / "bookshelf"
BOOKS_CSV = PROJECT_ROOT / "data" / "books.csv"
README_MD = PROJECT_ROOT / "README.md"

class TestResult:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors: List[str] = []
    
    def add_pass(self, test_name: str):
        self.passed += 1
        print(f"✅ PASS: {test_name}")
    
    def add_fail(self, test_name: str, error: str):
        self.failed += 1
        self.errors.append(f"{test_name}: {error}")
        print(f"❌ FAIL: {test_name} - {error}")
    
    def summary(self):
        total = self.passed + self.failed
        print(f"\n📊 テスト結果サマリー")
        print(f"   合計: {total} テスト")
        print(f"   成功: {self.passed}")
        print(f"   失敗: {self.failed}")
        
        if self.failed > 0:
            print(f"\n❌ 失敗したテスト:")
            for error in self.errors:
                print(f"   - {error}")
        
        return self.failed == 0

def run_command(cmd: List[str]) -> Tuple[int, str, str]:
    """コマンドを実行して結果を返す"""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=SCRIPT_DIR)
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return 1, "", str(e)

def count_books_in_csv() -> int:
    """CSVファイルの本の数を数える（ヘッダー除く）"""
    try:
        with open(BOOKS_CSV, 'r', encoding='utf-8') as f:
            return sum(1 for _ in csv.DictReader(f))
    except FileNotFoundError:
        return 0

def book_exists_in_csv(book_name: str) -> bool:
    """CSVファイルに指定の本が存在するかチェック"""
    try:
        with open(BOOKS_CSV, 'r', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                if row['NAME'] == book_name:
                    return True
    except FileNotFoundError:
        pass
    return False

def get_book_status_from_csv(book_name: str) -> str:
    """CSVファイルから本のステータスを取得"""
    try:
        with open(BOOKS_CSV, 'r', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                if row['NAME'] == book_name:
                    return row['STATUS']
    except FileNotFoundError:
        pass
    return ""

def book_exists_in_readme(book_name: str) -> bool:
    """README.mdに指定の本が存在するかチェック"""
    try:
        with open(README_MD, 'r', encoding='utf-8') as f:
            content = f.read()
            return book_name in content
    except FileNotFoundError:
        return False

def cleanup_test_data():
    """テストデータをクリーンアップ"""
    print("🧹 テストデータをクリーンアップ中...")
    run_command([str(BOOKSHELF_CMD), "remove", TEST_BOOK_NAME])
    
    # README再生成
    run_command(["python", "generate_readme.py"])

def test_cli_help(result: TestResult):
    """CLIヘルプ表示テスト"""
    returncode, stdout, stderr = run_command([str(BOOKSHELF_CMD), "--help"])
    
    if returncode == 0 and "Bookshelf CLI Tool" in stdout:
        result.add_pass("CLIヘルプ表示")
    else:
        result.add_fail("CLIヘルプ表示", f"ヘルプが正常に表示されない: {stderr}")

def test_add_book(result: TestResult):
    """本追加テスト"""
    returncode, stdout, stderr = run_command([
        str(BOOKSHELF_CMD), "add", TEST_BOOK_NAME,
        "--category", TEST_CATEGORY,
        "--lang", TEST_LANG,
        "--type", TEST_TYPE
    ])
    
    if returncode == 0 and f"追加しました: {TEST_BOOK_NAME}" in stdout:
        if book_exists_in_csv(TEST_BOOK_NAME):
            result.add_pass("本の追加")
        else:
            result.add_fail("本の追加", "CSVにデータが追加されていない")
    else:
        result.add_fail("本の追加", f"追加コマンドが失敗: {stderr}")

def test_duplicate_add(result: TestResult):
    """重複追加エラーテスト"""
    returncode, stdout, _ = run_command([
        str(BOOKSHELF_CMD), "add", TEST_BOOK_NAME,
        "--category", TEST_CATEGORY
    ])
    
    if "は既に登録されています" in stdout:
        result.add_pass("重複追加エラー検出")
    else:
        result.add_fail("重複追加エラー検出", f"重複エラーが検出されない: stdout={stdout}, returncode={returncode}")

def test_start_reading(result: TestResult):
    """読書開始テスト"""
    returncode, stdout, stderr = run_command([
        str(BOOKSHELF_CMD), "start", TEST_BOOK_NAME
    ])
    
    if returncode == 0 and "READING" in stdout:
        if get_book_status_from_csv(TEST_BOOK_NAME) == "READING":
            result.add_pass("読書開始(UNREAD→READING)")
        else:
            result.add_fail("読書開始(UNREAD→READING)", "CSVのステータスが更新されていない")
    else:
        result.add_fail("読書開始(UNREAD→READING)", f"ステータス更新が失敗: {stderr}")

def test_finish_reading(result: TestResult):
    """読書完了テスト"""
    returncode, stdout, stderr = run_command([
        str(BOOKSHELF_CMD), "finish", TEST_BOOK_NAME
    ])
    
    if returncode == 0 and "READ" in stdout:
        # 注意: finishコマンドは "read" (小文字) にセットしているが、CSVでは "READ" として保存される仕様を確認
        actual_status = get_book_status_from_csv(TEST_BOOK_NAME)
        if actual_status.upper() == "READ":
            result.add_pass("読書完了(READING→READ)")
        else:
            result.add_fail("読書完了(READING→READ)", f"CSVのステータスが正しくない: {actual_status}")
    else:
        result.add_fail("読書完了(READING→READ)", f"ステータス更新が失敗: {stderr}")

def test_nonexistent_book(result: TestResult):
    """存在しない本の操作テスト"""
    nonexistent_book = "存在しない本_テスト"
    returncode, stdout, _ = run_command([
        str(BOOKSHELF_CMD), "start", nonexistent_book
    ])
    
    if "を含む本が見つかりません" in stdout:
        result.add_pass("存在しない本エラー検出")
    else:
        result.add_fail("存在しない本エラー検出", f"エラーが正しく検出されない: stdout={stdout}, returncode={returncode}")

def test_generate_readme(result: TestResult):
    """README生成テスト"""
    returncode, stdout, stderr = run_command(["python", "generate_readme.py"])
    
    if returncode == 0 and "README.md生成完了" in stdout:
        if book_exists_in_readme(TEST_BOOK_NAME):
            result.add_pass("README生成")
        else:
            result.add_fail("README生成", "READMEにテスト用書籍が含まれていない")
    else:
        result.add_fail("README生成", f"README生成が失敗: {stderr}")

def test_remove_book(result: TestResult):
    """本削除テスト"""
    returncode, stdout, stderr = run_command([
        str(BOOKSHELF_CMD), "remove", TEST_BOOK_NAME
    ])
    
    if returncode == 0 and f"削除しました: {TEST_BOOK_NAME}" in stdout:
        if not book_exists_in_csv(TEST_BOOK_NAME):
            result.add_pass("本の削除")
        else:
            result.add_fail("本の削除", "CSVからデータが削除されていない")
    else:
        result.add_fail("本の削除", f"削除コマンドが失敗: {stderr}")

def test_cleanup_verification(result: TestResult):
    """クリーンアップ検証テスト"""
    # README再生成してクリーンアップ
    run_command(["python", "generate_readme.py"])
    
    csv_clean = not book_exists_in_csv(TEST_BOOK_NAME)
    readme_clean = not book_exists_in_readme(TEST_BOOK_NAME)
    
    if csv_clean and readme_clean:
        result.add_pass("テストデータクリーンアップ")
    else:
        issues: List[str] = []
        if not csv_clean:
            issues.append("CSV")
        if not readme_clean:
            issues.append("README")
        result.add_fail("テストデータクリーンアップ", f"データが残存: {', '.join(issues)}")

def test_extract_books(result: TestResult):
    """extract_books.py実行テスト"""
    returncode, stdout, stderr = run_command(["python", "extract_books.py"])
    
    if returncode == 0 and "抽出完了" in stdout:
        result.add_pass("extract_books.py実行")
    else:
        result.add_fail("extract_books.py実行", f"抽出処理が失敗: {stderr}")

def main():
    print("🚀 Bookshelf CLI 自動テスト開始\n")
    
    # 事前チェック
    if not BOOKSHELF_CMD.exists():
        print(f"❌ エラー: {BOOKSHELF_CMD} が見つかりません")
        sys.exit(1)
    
    # 初期状態の記録
    initial_book_count = count_books_in_csv()
    print(f"📊 テスト開始時の書籍数: {initial_book_count}")
    
    # テスト実行前にクリーンアップ（万が一残存データがある場合）
    cleanup_test_data()
    
    result = TestResult()
    
    try:
        # 基本機能テスト
        print("\n🔧 基本機能テスト")
        test_cli_help(result)
        test_add_book(result)
        test_duplicate_add(result)
        test_start_reading(result)
        test_finish_reading(result)
        test_generate_readme(result)
        test_remove_book(result)
        
        # エラーハンドリングテスト
        print("\n🚨 エラーハンドリングテスト")
        test_nonexistent_book(result)
        
        # データ整合性テスト
        print("\n🔍 データ整合性テスト")
        test_cleanup_verification(result)
        
        # ユーティリティテスト
        print("\n🛠️ ユーティリティテスト")
        test_extract_books(result)
        
    except KeyboardInterrupt:
        print("\n\n⚠️ テストが中断されました")
        cleanup_test_data()
        sys.exit(1)
    
    finally:
        # 最終クリーンアップ
        cleanup_test_data()
    
    # 最終状態の確認
    final_book_count = count_books_in_csv()
    print(f"📊 テスト完了時の書籍数: {final_book_count}")
    
    if initial_book_count != final_book_count:
        result.add_fail("データ整合性", f"書籍数が変化: {initial_book_count} → {final_book_count}")
    
    # 結果サマリー
    success = result.summary()
    
    if success:
        print("\n🎉 全てのテストが成功しました！")
        sys.exit(0)
    else:
        print("\n💥 一部のテストが失敗しました")
        sys.exit(1)

if __name__ == "__main__":
    main()