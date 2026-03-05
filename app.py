import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# .envファイルから環境変数を読み込む
load_dotenv()

# OpenAIクライアントの初期化
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def get_ai_response(system_prompt, user_input):
    """OpenAI APIを呼び出して回答を取得する関数"""
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        temperature=0.5
    )
    return completion.choices[0].message.content

# アプリのタイトル
st.title("聞きたいことに答えます（料理・観光）")

st.write("##### 動作モード1: 料理のレシピ")
st.write("料理のレシピを教えてくれます。")
st.write("##### 動作モード2: 観光地の紹介")
st.write("観光地を紹介してくれます。")

# 動作モードの選択
selected_item = st.radio(
    "動作モードを選択してください。",
    ["料理のレシピ", "観光地の紹介"]
)

st.divider()

# 選択されたモードによって入力フォームのラベルを変更
if selected_item == "料理のレシピ":
    input_message = st.text_input(label="知りたい料理名を記載してください (例: カレーライス)")
else:
    input_message = st.text_input(label="紹介してほしい観光地を記載してください (例: 京都)")

# 実行ボタンが押された時の処理
if st.button("実行"):
    st.divider()

    if input_message:
        # AIが考えている間に表示するスピナー（くるくる回るアイコン）
        with st.spinner("AIが考え中です..."):
            
            # モードに応じて、AIに与える役割（システムプロンプト）を変える
            if selected_item == "料理のレシピ":
                system_prompt = "あなたはプロの料理研究家です。ユーザーが指定した料理の美味しい作り方、必要な材料、そして調理のコツを分かりやすく教えてください。"
            else:
                system_prompt = "あなたは旅行ガイドです。ユーザーが指定した観光地の魅力、おすすめスポット、アクセス方法、注意点などを分かりやすく魅力的に紹介してください。"
            
            try:
                # AIから回答を取得
                response = get_ai_response(system_prompt, input_message)
                
                # 回答を画面に表示
                st.write(f"### 【回答】")
                st.write(response)

            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
                st.error("APIキーが正しく設定されているか確認してください。")
    else:
        st.error("テキストを入力してから「実行」ボタンを押してください。")
