import google.generativeai as genai
import os

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


def promptAI(prompt):
    result = chat.send_message(prompt)
    response = result.text
    # text = response.text
    return response

# promptAI(charac)
while(True):
    prompt = input("You: ")
    print("Gemini: ", promptAI(prompt))


