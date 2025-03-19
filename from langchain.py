from langchain.embeddings import OpenAIEmbeddings
from pydantic import ValidationError

class TextVectorizer:
    def __init__(self):
        try:
            self.embeddings = OpenAIEmbeddings()
        except ValidationError as e:
            print(f"Validation error: {e}")
            # 必要に応じて、エラーハンドリングを追加
            # 例: デフォルト値を設定する、再試行するなど
