# 顔認識AI体験アプリ（Chat風UI + 2モデル比較）

このアプリは、AI初心者向けに「画像認識AIの進化」を体験できる Web アプリです。  
ユーザーは16枚の顔画像から選び、以下の2つのAIモデルで判定結果を比較できます。

- HOG + SVM（古典的な画像特徴量）
- ResNet18（深層学習によるCNNモデル）

## 🧠 特徴
- ChatGPT風の対話UI
- 日本語・英語など任意の言語で利用可能
- モデルの違いがコメント付きで体験できる

## 🗂 ディレクトリ構成
/backend
predict.py ← Flaskによる推論API
/models
011 - hog_svm_model.pth
021 - resnet18_model.pth
/images
t01.png ~ t16.png ← 入力用画像
/comments
ja.json, en.json ← 画像ごとのコメント
app.py ← Streamlit UI本体
requirements.txt ← 依存ライブラリ


## 🚀 ローカルでの実行方法（開発用）

```bash
# 仮想環境作成 & 有効化（任意）
python -m venv .venv
.venv\Scripts\activate

# ライブラリのインストール
pip install -r requirements.txt

# Flask APIサーバー起動
cd backend
python predict.py

# Streamlitアプリ起動（別ターミナル）
cd ..
streamlit run app.py

#公開URL（Render）
https://your-app-name.onrender.com


