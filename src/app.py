import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
from datetime import datetime
from typing import List, Dict

from .chromadb import VectorStore
from .types import Message, ChatHistory, DocumentMetadata
from .vectorize import TextVectorizer

# Initialize components
vector_store = VectorStore()
vectorizer = TextVectorizer()
chat_model = ChatOpenAI(temperature=0.7)

# Initialize conversation chain
memory = ConversationBufferMemory()
conversation = ConversationChain(
    llm=chat_model,
    memory=memory,
    verbose=True
)

def generate_response(prompt: str, history: List[Message]) -> str:
    try:
        # Search relevant context from vector store
        search_results = vector_store.search(prompt)
        
        # Prepare context
        context = "\n".join(search_results["documents"][0])
        
        # Prepare conversation prompt
        prompt_template = f"""
        Context information: {context}
        
        Current conversation:
        {memory.buffer}
        
        Human: {prompt}
        Assistant: Let me help you with that.
        """
        
        # Generate response
        response = conversation.predict(input=prompt_template)
        
        # Store conversation in vector store
        vector_store.add_texts(
            [f"Human: {prompt}\nAssistant: {response}"],
            [{"timestamp": str(datetime.now())}]
        )
        
        return response
    except Exception as e:
        return f"Error: {str(e)}"

def upload_section():
    st.header("ドキュメントアップロード")
    
    uploaded_file = st.file_uploader("テキストファイルをアップロード", type=['txt'])
    
    col1, col2 = st.columns(2)
    with col1:
        area = st.text_input("エリア名")
        major_category = st.text_input("大カテゴリ")
    with col2:
        sub_category = st.text_input("中カテゴリ")
        source = st.text_input("ソース元")
    
    if uploaded_file and st.button("アップロード"):
        text_content = uploaded_file.getvalue().decode("utf-8")
        
        # テキストを分割してベクトル化
        chunks = vectorizer.split_text(text_content)
        
        # メタデータを作成
        metadata = DocumentMetadata(
            area=area,
            major_category=major_category,
            sub_category=sub_category,
            source=source,
            filename=uploaded_file.name,
            upload_date=datetime.now().isoformat()
        )
        
        # 各チャンクをChromaDBに保存
        for chunk in chunks:
            vector_store.add_document(chunk, metadata)
        
        st.success(f"ファイル '{uploaded_file.name}' を保存しました。")

def area_info_section():
    st.header("エリア情報")
    
    area = st.selectbox("エリアを選択してください", ["川越市", "エリア2", "エリア3"])
    
    if area:
        # エリア情報を取得（ここではダミーデータを使用）
        area_info = {
            "川越市": "エリア1の詳細情報...",
            "エリア2": "エリア2の詳細情報...",
            "エリア3": "エリア3の詳細情報..."
        }
        
        st.write(area_info[area])

def main():
    st.title("AI チャットボット")
    
    # サイドバーにアップロード機能を追加
    with st.sidebar:
        upload_section()
    
    # メインセクションにエリア情報セクションを追加
    area_info_section()
    
    # ...existing code...

if __name__ == "__main__":
    main()
