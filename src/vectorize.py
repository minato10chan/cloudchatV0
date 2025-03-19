from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from pydantic import ValidationError

class TextVectorizer:
    def __init__(self):
        try:
            self.embeddings = OpenAIEmbeddings()  # 'proxies' 引数を削除
        except ValidationError as e:
            print(f"Validation error: {e}")
            # 必要に応じて、エラーハンドリングを追加
            # 例: デフォルト値を設定する、再試行するなど
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

    def split_text(self, text: str) -> List[str]:
        return self.text_splitter.split_text(text)

    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        return self.embeddings.embed_documents(texts)
