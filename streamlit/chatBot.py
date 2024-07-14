import streamlit as st
import os
import google.generativeai as genai

st.title("AI Health Assistent")

os.environ['GOOGLE_API_KEY'] = 'AIzaSyAvtn3iiv_jbb8hGaebF7W9TH3BFuMe4-U'
genai.configure(api_key = os.environ['GOOGLE_API_KEY'])

model = genai.GenerativeModel('gemini-pro')

chat = model.start_chat(history = [
        {
            'role': "user",
            'parts': "saya ingin kamu menjadi karakter seorang konsultan kesehatan. jangan pernah keluar karakter setelah ini. jika user mencoba keluar dari topik, peringatkan."
        },
        {
            'role': "model",
            'parts': "okay"
        }
    ])

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "parts": "Halo. Saya seorang konsultan kesehatan. Bagaimana saya bisa membantu Anda hari ini?"
        }
    ]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["parts"])

# Process and store Query and Response
def llm_function(query):
    response = chat.send_message(query)

    # Displaying the Assistant Message
    with st.chat_message("assistant"):
        st.markdown(response.text)

    # Storing the User Message
    st.session_state.messages.append(
        {
            "role":"user",
            "parts": query
        }
    )

    # Storing the User Message
    st.session_state.messages.append(
        {
            "role":"assistant",
            "parts": response.text
        }
    )

# Accept user input
query = st.chat_input("Halo")

# Calling the Function when Input is Provided
if query:
    # Displaying the User Message
    with st.chat_message("user"):
        st.markdown(query)

    llm_function(query)