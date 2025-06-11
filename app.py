import streamlit as st
from langdetect import detect
import json
import os
from PIL import Image

#起動確認
import streamlit as st

st.title("起動確認中")
st.write("Hello! アプリは動いています！")

# ---------- 初期設定 ----------
st.set_page_config(page_title="AIモデル比較アプリ", layout="wide")

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
        except:
            st.error("言語を判別できませんでした。もう一度入力してください。")
    #st.stop()

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
st.image(image, caption=selected_image, width=300)

# ---------- コメント表示 ----------
image_key = os.path.splitext(selected_image)[0]  # 例: 't01'
comment = comments.get(image_key, "この画像に対応するコメントはありません。")
st.write(f"📝 コメント: {comment}")

# ---------- モデル選択と予測結果 ----------
st.sidebar.title("モデルを選択")
model_name = st.sidebar.radio("使用するモデル", ["HOG+SVM", "ResNet18"])

if st.button("この画像で予測する"):
    # （仮）推論結果のサンプル表示
    st.success(f"✅ モデル [{model_name}] による予測：これは仮の結果です。推論APIと接続予定。")
