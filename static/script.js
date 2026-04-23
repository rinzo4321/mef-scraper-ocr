function startProcess() {
    const year = document.getElementById('year').value;
    const codes = document.getElementById('codes').value;
    const startCert = document.getElementById('start_cert').value || 1;
    const endCert = document.getElementById('end_cert').value || null;
    const btn = document.getElementById('btn-start');
    const statusArea = document.getElementById('status-area');
    const statusText = document.getElementById('status-text');
    const loader = document.getElementById('loader');

    if (!codes.trim()) {
        alert("Por favor ingresa al menos un código.");
        return;
    }

    btn.disabled = true;
    btn.innerText = "Procesando...";
    statusArea.classList.remove('hidden');
    statusText.innerText = "Iniciando servidor y navegador...";
    loader.classList.remove('hidden');

    fetch('/start_process', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
            year: year, 
            codes: codes,
            start_cert: parseInt(startCert),
            end_cert: endCert ? parseInt(endCert) : null
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            statusText.innerText = data.message + "\nRevisa la ventana del navegador que se abrió.";
        } else {
            statusText.innerText = "Error: " + data.message;
            btn.disabled = false;
            btn.innerText = "Iniciar Proceso";
            loader.classList.add('hidden');
        }
    })
    .catch((error) => {
        console.error('Error:', error);
        statusText.innerText = "Error de comunicación con el servidor.";
        btn.disabled = false;
        btn.innerText = "Iniciar Proceso";
        loader.classList.add('hidden');
    });
}

