import streamlit as st
import time

# Inisialisasi atau dapatkan nilai val dari session state
if 'val' not in st.session_state:
    st.session_state.val = 0

st.title("percobaan")

placeholder = st.metric(label="value", value=0)
text = st.text_area("tulis sesuatu")
button = st.button("submit")
output = st.empty()

while(True):
    placeholder.metric(label="value", value = st.session_state.val)
    st.session_state.val += 1

    # Cek apakah tombol submit ditekan
    if button:
        output.write(f"Teks yang Anda masukkan: {text}")
    time.sleep(1)