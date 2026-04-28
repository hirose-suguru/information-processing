# CLAUDE.md

## renumber_headings.py

Markdownファイルの見出しに連番を自動付与するスクリプト。

### 使い方

```bash
# information_processing.md に対して実行（デフォルト）
python renumber_headings.py

# 任意のファイルを上書き
python renumber_headings.py <file.md>

# 入力と出力を別ファイルにする
python renumber_headings.py <input.md> <output.md>
```

### 処理内容（4パス）

1. **欠落レベル補完** — `#` の次が `###` のように飛んでいる場合、子孫を1段繰り上げて階層を修正
2. **連番付与** — 全見出しに `1.`, `1.1.`, `1.1.1.` 形式で番号を振り直す
3. **アンカー挿入** — 各見出しの直前に `<a id="one-one"></a>` 形式のHTMLアンカーを挿入
4. **インラインリンク更新** — 番号が変わった見出しへの `[text](#old-id)` リンクを新しいIDとタイトルに自動更新

### アンカーIDの形式

番号の各桁を英単語に変換してハイフンでつなぐ。

| 見出し番号 | アンカーID |
|-----------|-----------|
| `1.` | `one` |
| `1.1.` | `one-one` |
| `5.2.3.` | `five-two-three` |

### モジュール構成

```
renumber_headings.py   # エントリーポイント
modules/
  constants.py         # 正規表現・定数
  helpers.py           # ユーティリティ関数
  passes.py            # 4パスの処理実装
```
