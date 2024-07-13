import streamlit as st

def main():
    # Menampilkan judul
    st.title('Health Dashboard')

    # Menampilkan HTML menggunakan st.markdown
    with open('uji.html', 'r') as f:
        html_code = f.read()
    st.markdown(html_code, unsafe_allow_html=True)

if __name__ == '__main__':
    main()