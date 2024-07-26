import streamlit as st
import streamlit.components.v1 as components

# Membaca file CSS
with open('static/styles.css', 'r') as css_file:
    css_content = css_file.read()

# Membaca file JavaScript
with open('static/script.js', 'r') as js_file:
    js_content = js_file.read()

# HTML code with embedded CSS and JS
html_code = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reca</title>
    <style>{css_content}</style>
</head>
<body>
    <header></header>
    <main>
        <article class="d-flex no-wrap" id="iot-value">
            <section class="d-flex card-iot">
                <div class="special-respon">
                    <span class="material-symbols-outlined">ecg_heart</span>
                    <h3>Detak Jantung Per Menit</h3>
                    <h1 id="bpm-value">40</h1>
                </div>
            </section>
            <section class="d-flex card-iot">
                <div class="special-respon">
                    <span class="material-symbols-outlined">spo2</span>
                    <h3>Saturasi Oksigen</h3>
                    <h1 id="spo2-value">90</h1>
                </div>
            </section>
            <section class="d-flex card-iot">
                <div class="special-respon">
                    <span class="material-symbols-outlined">thermostat</span>
                    <h3>Temperature (C)</h3>
                    <h1 id="temp-value">35</h1>
                </div>
            </section>
        </article>
        <article id="input-container">
            <section>
                <p class="bg-radius bg-white" id="c-judul-input">
                    Saran untuk pasien yang memiliki detak jantung per menit: <span id="bpm-span">40</span>, saturasi oksigen: <span id="spo2-span">90</span>, dan temperatur: <span id="temp-span">35</span>
                </p>
            </section>
            <section>
                <form id="form-gejala">
                    <div class="d-flex special-respon">
                        <label for="gejala-user" class="bg-radius bg-white"><i>Masukkan gejala yang kamu alami</i></label>
                        <textarea id="gejala-user" name="gejala-user" placeholder="Ketikkan gejalamu di sini..." class="bg-radius bg-white" cols="50"></textarea>
                    </div>
                    <button type="submit" class="bg-radius" onclick="submitForm()">BERIKAN SARAN</button>
                </form>
            </section>
        </article>
        <article id="ai-result">
            <section id="ai-result-title" class="d-flex">
                <div class="d-flex" id="triple-circle">
                    <div class="circle cc-color"></div>
                    <div class="circle cc-color"></div>
                    <div class="circle cc-color"></div>
                </div>
                <div class="title bg-white">
                    <p>Hasil</p>
                </div>
            </section>
            <section id="ai-result-text" class="bg-radius bg-white"></section>
        </article>
    </main>
    <footer></footer>
    <script>{js_content}</script>
</body>
</html>
"""

# Display the HTML
components.html(html_code, height=1000)
