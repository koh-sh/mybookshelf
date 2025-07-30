# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a simple personal book tracking repository called "mybookshelf" (購入した本を一覧化する). The repository contains a single README.md file that serves as a comprehensive catalog of purchased books.

## Architecture & Structure

The repository follows a minimalist approach:

- **README.md**: The primary file containing all book data in markdown table format
- Books are categorized by topic (システム基盤・インフラ, プログラミング・開発, 設計・品質, etc.)
- Each book entry includes: NAME, LANG (language), TYPE (format), STATUS (reading status), and MEMO fields
- Book statuses include: READ, UNREAD, READING
- Book types include: Kindle, Physical, Apple ebook
- Languages are primarily JPN (Japanese) with some ENG (English) books

## Content Management

When working with this repository:

- Books are organized in clearly defined sections with emoji headers
- Table format is strict: `|NAME|LANG|TYPE|STATUS|MEMO|` with alignment `|:---|:---|:---|:---|:---|`
- Status values should be consistent: READ, UNREAD, READING
- Language codes: JPN for Japanese, ENG for English
- Book types: Kindle, Physical, Apple ebook, etc.
- New books should be added to the appropriate category section
- Maintain the existing markdown table structure and formatting

## Development Commands

This repository does not contain any build scripts, package managers, or development dependencies. All operations are performed directly on the README.md file using standard git commands for version control.
