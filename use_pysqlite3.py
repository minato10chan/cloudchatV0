import pysqlite3
import sys
sys.modules['sqlite3'] = pysqlite3

import streamlit as st

# シークレットキーを読み込む
secret_key = st.secrets["general"]["secret_key"]
openai_api_key = st.secrets["openai"]["OPENAI_API_KEY"]

# ...existing code...
