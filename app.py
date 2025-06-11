import streamlit as st
from langdetect import detect
import json
import os
from PIL import Image

# ---------- 初期設定 ----------
st.set_page_config(page_title="AIモデル比較アプリ", layout="wide")

# 起動確認
st.title("起動確認中")
st.write("Hello! アプリは動いています！")

# セッション状態の初期化
if "lang" not in st.session_state:
    st.session_state.lang = None
    st.session_state.lang_selected = False

# ---------- 言語選択プロンプト ----------
if not st.session_state.lang_selected:
    st.title("AIモデル体験アプリ")
    user_lang_input = st.text_input("🤖: こんにちは！使いたい言語を教えてください。\n\nHello! What language would you like to use?")

    if user_lang_input:
        try:
            lang_code = detect(user_lang_input)
            st.session_state.lang = lang_code
            st.session_state.lang_selected = True
            st.experimental_rerun()
            st.stop()
        except:
            st.error("言語を判別できませんでした。もう一度入力してください。")

# ---------- 多言語コメントの読み込み ----------
def load_comments(lang_code):
    filepath = f"comments/{lang_code}.json"
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        st.warning("対応するコメントファイルが見つかりませんでした。日本語を使用します。")
        with open("comments/ja.json", "r", encoding="utf-8") as f:
            return json.load(f)

comments = load_comments(st.session_state.lang)

# ---------- 画像選択 UI ----------
st.sidebar.title("画像を選んでください")
image_files = sorted([f for f in os.listdir("images") if f.endswith(".png")])
selected_image = st.sidebar.selectbox("画像ファイルを選択", image_files)

image_path = os.path.join("images", selected_image)
image = Image.open(image_path)

# ---------- モデル名の一覧 ----------
model_names = ["HOG+SVM", "SIFT+SVM", "ResNet18"]

# ---------- 予測ボタン ----------
if st.button("この画像で予測する"):
    st.subheader("🧠 モデル別予測結果")
    cols = st.columns(3)
    for i, model in enumerate(model_names):
        with cols[i]:
            st.image(image, caption=f"{model}", use_column_width=True)
            st.success(f"✅ {model} による予測：仮の結果（ここにAPI結果）")

    # ---------- コメント表示 ----------
    st.subheader("📝 コメント")
    image_key = os.path.splitext(selected_image)[0]
    comment = comments.get(image_key, "この画像に対応するコメントはありません。")
    st.write(comment)
