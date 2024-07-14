import streamlit as st
import os
import google.generativeai as genai

st.title("Gemini Bot")

os.environ['GOOGLE_API_KEY'] = 'AIzaSyAvtn3iiv_jbb8hGaebF7W9TH3BFuMe4-U'
genai.configure(api_key = os.environ['GOOGLE_API_KEY'])

# Select the model
model = genai.GenerativeModel('gemini-pro')

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.message = [
        {
            "role": "user",
            "content": "Saya ingin kamu memainkan peran sebagai seorang konsultan kesehatan. Jawab tidak tahu jika setelah ini user membahas hal di luar kesehatan."
        },
        {
            "role": "assistant",
            "content": "Okay"
        }
    ]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Process and store Query and Response
def llm_function(query):
    response = model.generate_content(query)

    # Displaying the Assistant Message
    with st.chat_message("assistant"):
        st.markdown(response.text)

    # Storing the User Message
    st.session_state.messages.append(
        {
            "role":"user",
            "content": query
        }
    )

    # Storing the User Message
    st.session_state.messages.append(
        {
            "role":"assistant",
            "content": response.text
        }
    )

# Accept user input
query = st.chat_input("What's up?")

# Calling the Function when Input is Provided
if query:
    # Displaying the User Message
    with st.chat_message("user"):
        st.markdown(query)

    llm_function(query)