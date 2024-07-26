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
    window.parent.postMessage({ type: 'gejala', gejala: gejala }, '*');
}

window.addEventListener('message', function(event) {
    if (event.data.type === 'updateMetrics') {
        updateMetrics(event.data.bpm, event.data.spo2, event.data.temp);
    }
});
