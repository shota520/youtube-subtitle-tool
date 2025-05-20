import os
import re
import subprocess
import tempfile

def extract_video_id(url):
    match = re.search(r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})", url)
    return match.group(1) if match else None

def clean_vtt_lines(lines):
    text_lines = []
    last_line = ""
    for line in lines:
        line = line.strip()
        if re.match(r"^\d{2}:\d{2}:\d{2}\.\d{3}", line) or "-->" in line:
            continue
        line = re.sub(r"<[^>]+>", "", line)  # タグ除去
        if line and line != last_line:
            text_lines.append(line)
            last_line = line

    paragraph = ""
    result_lines = []
    for line in text_lines:
        if line.endswith(("。", ".", "！", "？", "!", "?")):
            paragraph += line
            result_lines.append(paragraph.strip())
            paragraph = ""
        else:
            paragraph += line + " "
    if paragraph:
        result_lines.append(paragraph.strip())
    return "\n\n".join(result_lines)

def fetch_transcript_ytdlp(url):
    try:
        # プロジェクト内DLtxtフォルダに保存
        subtitles_dir = os.path.join(os.getcwd(), "DLtxt")
        os.makedirs(subtitles_dir, exist_ok=True)

        video_id = extract_video_id(url)
        output_path = os.path.join(subtitles_dir, f"{video_id}.%(ext)s")

        # 日本語＋英語字幕を取得（自動字幕のみ）
        result = subprocess.run(
            [
                "yt-dlp",
                "--write-auto-sub", "--sub-lang", "ja,en.*",
                "--skip-download", "--output", output_path, url
            ],
            capture_output=True, text=True
        )

        if result.returncode != 0:
            return None, f"yt-dlpエラー：{result.stderr}"

        # .vtt ファイルを日本語優先で選定
        vtt_files = sorted(
            [f for f in os.listdir(subtitles_dir) if f.endswith(".vtt") and video_id in f],
            key=lambda name: (".ja" not in name, name)
        )

        if not vtt_files:
            return None, "字幕ファイルが見つかりませんでした。"

        vtt_path = os.path.join(subtitles_dir, vtt_files[0])
        with open(vtt_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        cleaned_text = clean_vtt_lines(lines)

        # ✅ テキスト保存
        txt_path = os.path.join(subtitles_dir, f"{video_id}.txt")
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(cleaned_text)

        # ✅ vtt削除
        import glob
        for f in glob.glob(os.path.join(subtitles_dir, f"{video_id}*.vtt")):
            os.remove(f)

        return cleaned_text, None

    except Exception as e:
        return None, f"字幕取得処理中にエラー：{str(e)}"
