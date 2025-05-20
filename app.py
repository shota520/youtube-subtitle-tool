import os
import streamlit as st
from youtube_utils import extract_video_id, fetch_transcript_ytdlp

st.title("📄 字幕表示ツール")
st.caption("YouTubeの字幕付き動画URLを貼ってください（日本語・英語両対応）")

url = st.text_input("🔗 YouTube動画URL", placeholder="https://www.youtube.com/watch?v=XXXXXXXXXXX")

if st.button("字幕取得") and url:
    with st.spinner("字幕取得中..."):
        transcript_text, error = fetch_transcript_ytdlp(url)
        if error:
            st.error(f"❌ {error}")
        else:
            st.success("✅ 字幕取得成功")
            st.text_area("📋 字幕表示", value=transcript_text, height=300)

            # 保存フォルダとファイル名の準備
            video_id = extract_video_id(url)
            save_dir = "DLtxt"
            os.makedirs(save_dir, exist_ok=True)
            txt_path = os.path.join(save_dir, f"{video_id}.txt")

            # ファイルに保存
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(transcript_text)

            # ダウンロードボタン（保存したファイルを再読み込み）
            with open(txt_path, "rb") as f:
                st.download_button(
                    "💾 字幕をダウンロード",
                    data=f,
                    file_name=f"{video_id}.txt",
                    mime="text/plain"
                )
