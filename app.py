# APIキーの読み込み
from dotenv import load_dotenv
import os
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# コード本体
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
import streamlit as st

def get_expert_answer(input_text, expert_type):
    """
    入力テキストと専門家タイプを受け取り、LLMからの回答を返す関数
    """
    if not input_text:
        return "質問内容が入力されていません。"
    if expert_type == "税金の専門家":
        system_prompt = "あなたは税金の専門家です。質問に対して税金の専門家の観点から回答してください"
    else:
        system_prompt = "あなたは法律の専門家です。質問に対して法律の専門家の観点から回答してください"
    try:
        llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=input_text),
        ]
        result = llm(messages)
        return result.content
    except Exception as e:
        return f"エラーが発生しました: {e}"

st.title("専門家への相談アプリ")
st.markdown(
    """
    ### アプリ概要
    このWebアプリは、税金・法律の専門家に相談できるAIチャットサービスです。

    ### 操作方法
    1. 画面上部で相談したい専門家を選択してください。
    2. 下の入力欄に相談内容を入力してください。
    3. 「実行」ボタンを押すと、専門家AIからの回答が表示されます。
    """
)

selected_item = st.radio(
    "専門家を選択してください。",
    ["税金の専門家", "法律の専門家"]
)

st.divider()

input_message = st.text_input("相談内容を入力してください。")

if st.button("実行"):
    st.divider()
    if not input_message:
        st.error("質問を入力してから「実行」ボタンを押してください。")
    else:
        answer = get_expert_answer(input_message, selected_item)
        st.write("### 回答")
        st.write(answer)
        