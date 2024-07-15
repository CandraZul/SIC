import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI  # To use the Gemini LLM
import google.generativeai as genai  # For configuring Google's Generative AI API
from langchain.chains import ConversationChain  # To manage conversations
from langchain.memory import ConversationBufferMemory  # To remember conversation history

st.title("AI Health Assistant")

# Configure the Google API key
os.environ['GOOGLE_API_KEY'] = 'AIzaSyAvtn3iiv_jbb8hGaebF7W9TH3BFuMe4-U'
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

# Initialize the Generative Model
model = genai.GenerativeModel(model_name='gemini-pro')

# Set up the initial chat context
initial_chat_context = [
    {
        'role': "user",
        'parts': "saya ingin kamu menjadi karakter seorang konsultan kesehatan. jangan pernah keluar karakter setelah ini. jika user mencoba keluar dari topik, peringatkan."
    },
    {
        'role': "model",
        'parts': "okay"
    }
]

# Initialize the conversation
chat = model.start_chat(history=initial_chat_context)

# Initialize chat history in Streamlit session state
if 'messages' not in st.session_state:
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

# Function to get a response from the model
def get_response(user_input):
    if 'conversation' not in st.session_state:
        st.session_state['conversation'] = ConversationChain(
            llm=ChatGoogleGenerativeAI(model_name='gemini-pro'),
            memory=ConversationBufferMemory()
        )  # Create a conversation chain if it doesn't exist

    response = st.session_state['conversation'].predict(input=user_input)  # Get response from the model
    return response

# Accept user input
query = st.chat_input("Halo")

# Calling the function when input is provided
if query:
    # Displaying the user message
    with st.chat_message("user"):
        st.markdown(query)

    st.session_state['messages'].append({"role": "user", "parts": query})  # Add user input to message list
    model_response = get_response(query)  # Get model response
    st.session_state['messages'].append({"role": "assistant", "parts": model_response})  # Add model response to message list

    # Displaying the assistant's response
    with st.chat_message("assistant"):
        st.markdown(model_response)
