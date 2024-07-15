import streamlit as st
import os
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.llms import OpenAI

st.title("AI Health Assistant")

# Konfigurasi kunci API

# Inisialisasi model OpenAI
model = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

# Inisialisasi rantai percakapan dengan memori
conversation = ConversationChain(
    llm=model,
    memory=ConversationBufferMemory()
)

# Inisialisasi riwayat percakapan jika belum ada
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "parts": "Halo. Saya seorang konsultan kesehatan. Bagaimana saya bisa membantu Anda hari ini?"
        }
    ]

# Menampilkan pesan dari riwayat percakapan pada saat aplikasi dijalankan ulang
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["parts"])

# Fungsi untuk memproses input pengguna
def llm_function(query):
    # Memastikan input sesuai dengan yang diharapkan oleh ConversationChain
    response = conversation({"input": query})

    with st.chat_message("assistant"):
        st.markdown(response['response'])

    st.session_state.messages.append(
        {
            "role": "user",
            "parts": query
        }
    )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "parts": response['response']
        }
    )

# Menerima input pengguna
query = st.chat_input("Halo")

if query:
    with st.chat_message("user"):
        st.markdown(query)

    llm_function(query)
