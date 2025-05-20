# 🎬 YouTube字幕取得ツール（API不要）

YouTube動画の字幕（日本語／英語）を自動で取得し、テキストとして保存・活用できるPythonアプリです。  
**OpenAI APIなど一切不要**。ローカル完結で動作します。
取得した字幕はプロンプト設計することで要約や記事作成などに使えます。

---

## 🛠 機能一覧

- YouTube URLを入力 → 字幕を取得
- 日本語字幕優先（英語字幕にも対応）
- `.vtt` → プレーンテキストに変換して表示
- `.txt`形式で保存＆ダウンロード
- 実行ごとにゴミファイルを自動削除
- 完全ローカル動作、APIキー不要

---

## 💻 使用技術

- Python 3.x
- [Streamlit](https://streamlit.io/)（簡易UI）
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)（字幕の取得）
- subprocess（外部コマンド実行）

---

## 🚀 使い方

## 環境構築

- pip install -r requirements.txt
- pip install -U yt-dlp

## アプリ起動
- streamlit run app.py

---

🔮 展開例

- Whisper連携：字幕がない動画にも対応
- ChatGPT連携：自動要約機能
- CSV / PDF形式での出力
- マルチ動画一括処理（フォルダ指定）

---

📝 ライセンス
MIT License
