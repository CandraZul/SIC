import streamlit as st
import streamlit.components.v1 as components

# HTML + JavaScript code
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0" />
    <title>Reca</title>
    <style>
        /* Add some basic styling */
        body {
            font-family: Arial, sans-serif;
            padding: 20px;
        }
        .card-iot {
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 10px;
            margin: 10px;
            text-align: center;
        }
        .bg-radius {
            border-radius: 5px;
        }
    </style>
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
    <script>
        function updateMetrics(bpm, spo2, temp) {
            document.getElementById('bpm-value').textContent = bpm;
            document.getElementById('spo2-value').textContent = spo2;
            document.getElementById('temp-value').textContent = temp;
            document.getElementById('bpm-span').textContent = bpm;
            document.getElementById('spo2-span').textContent = spo2;
            document.getElementById('temp-span').textContent = temp;
        }

        function submitForm() {
            const gejala = document.getElementById('gejala-user').value;
            // Send the gejala data to Streamlit via postMessage
            window.parent.postMessage({ type: 'gejala', gejala: gejala }, '*');
        }

        window.addEventListener('message', function(event) {
            if (event.data.type === 'updateMetrics') {
                updateMetrics(event.data.bpm, event.data.spo2, event.data.temp);
            }
        });
    </script>
</body>
</html>
"""

# Display the HTML
components.html(html_code, height=800)

# Example of how to send data to the HTML
def send_data_to_html(bpm, spo2, temp):
    components.html(
        f"""
        <script>
            window.postMessage({{type: 'updateMetrics', bpm: {bpm}, spo2: {spo2}, temp: {temp}}}, '*');
        </script>
        """,
        height=0
    )

# Example data to send
send_data_to_html(75, 98, 36.5)
