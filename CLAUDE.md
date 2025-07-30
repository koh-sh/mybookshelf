# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a personal book tracking repository called "mybookshelf" (購入した本を一覧化する). The repository uses a hybrid approach combining CSV data storage with automated README.md generation for optimal usability and maintainability.

## Architecture & Structure

The repository uses a clean separation of data and presentation:

```
mybookshelf/
├── README.md              # Generated display file (beautiful markdown format)
├── CLAUDE.md              # This file - project guidance
├── .gitignore            # Python/IDE file exclusions
├── data/
│   └── books.csv         # Master data store (87+ books)
└── tools/
    ├── bookshelf_core.py # Shared functionality module
    ├── bookshelf         # Main CLI tool (executable)
    ├── extract_books.py  # One-time migration utility
    └── generate_readme.py # README generator
```

### Data Structure

- **Master Data**: `data/books.csv` with fields: NAME, CATEGORY, LANG, TYPE, STATUS, MEMO
- **Display Format**: README.md with categorized markdown tables and emoji headers
- **Categories**: システム基盤・インフラ, プログラミング・開発, 設計・品質, 運用・SRE・DevOps, セキュリティ・テスト, 組織・マネジメント, キャリア・スキル, 数学・アルゴリズム, AI, 学習・資格
- **Book Statuses**: READ, UNREAD, READING
- **Book Types**: Kindle, Physical, Apple ebook
- **Languages**: JPN (Japanese), ENG (English)

## CLI Tool Usage

The main interface is the `bookshelf` CLI tool:

```bash
# Add a new book
./tools/bookshelf add "Book Title" --category "AI" --lang JPN --type Kindle

# Update reading status
./tools/bookshelf start "Book Title"    # UNREAD → READING
./tools/bookshelf finish "Book Title"   # READING → READ

# Remove a book (with safety checks)
./tools/bookshelf remove "Book Title"

# Generate updated README.md
cd tools && python generate_readme.py
```

## Development Workflow

### Adding Books
1. Use `./tools/bookshelf add` command with appropriate parameters
2. Run `python generate_readme.py` to update display
3. Commit both CSV and README changes

### Status Updates
1. Use `./tools/bookshelf start` or `./tools/bookshelf finish`
2. Regenerate README if needed for display updates
3. Commit changes

### Data Management
- **Primary Source**: Always modify `data/books.csv` via CLI tools
- **Display Generation**: Use `generate_readme.py` to create README.md
- **Never manually edit**: README.md (it gets overwritten)
- **Safe Operations**: CLI includes duplicate checking and partial name matching

## Code Architecture

### Core Module (`bookshelf_core.py`)
- Centralized CSV operations (load_books, save_books)
- Path management and constants
- Book data structure creation
- Search and filtering utilities
- Type-safe operations with proper error handling

### CLI Tool (`bookshelf`)
- Argument parsing and command routing
- User interface and error messages
- Business logic for book operations
- Integration with core module functions

### Utilities
- `extract_books.py`: One-time migration from old README format
- `generate_readme.py`: Automated README.md generation with category organization

## Development Commands

### Testing New Features
```bash
# Test CLI functionality
./tools/bookshelf add "Test Book" --category "AI"
./tools/bookshelf start "Test Book"
./tools/bookshelf remove "Test Book"  # Clean up after testing

# Regenerate display
cd tools && python generate_readme.py
```

### Maintenance
- Use `.gitignore` to exclude Python cache files and IDE settings
- All relative paths are managed through `bookshelf_core.py` constants
- Category definitions and emoji mappings are centralized
- Code follows DRY principles with shared functionality

## Important Notes

- **Data Integrity**: CSV is the source of truth, README is generated
- **Safety First**: CLI prevents duplicate additions and requires exact matches for modifications
- **Git Workflow**: Commit both data and display files together
- **Extensibility**: Add new categories by updating `CATEGORY_ORDER` in `bookshelf_core.py`
- **Performance**: Handles 87+ books efficiently with simple file operations

When working with this repository, always use the CLI tools rather than manual file editing to ensure data consistency and proper formatting.