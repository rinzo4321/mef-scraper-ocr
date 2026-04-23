import os
import sys
import datetime
from flask import Flask, render_template, request, jsonify
import threading
import webbrowser

# Importamos la lógica del scraper
from logic import run_scraper_process

# --- CONFIGURACIÓN DE RUTAS ROBUSTA ---
if getattr(sys, 'frozen', False):
    # SI ESTAMOS EN MODO EJECUTABLE (PyInstaller)
    # 1. Ruta base donde está el .exe (Para Inputs/Outputs)
    EXEC_DIR = os.path.dirname(sys.executable)
    
    # 2. Ruta interna donde están los recursos (Templates, Static, Models)
    # En modo --onedir, suele estar en _internal o en la raíz relativa
    INTERNAL_DIR = os.path.join(EXEC_DIR, '_internal')
    if not os.path.exists(INTERNAL_DIR): # Fallback por si acaso
        INTERNAL_DIR = EXEC_DIR
else:
    # SI ESTAMOS EN MODO DESARROLLO (.py normal)
    EXEC_DIR = os.path.dirname(os.path.abspath(__file__))
    INTERNAL_DIR = EXEC_DIR

# Configurar Flask con rutas explicitas a los recursos estáticos
app = Flask(__name__, 
            template_folder=os.path.join(INTERNAL_DIR, 'templates'),
            static_folder=os.path.join(INTERNAL_DIR, 'static'))

# Carpetas de Usuario (Se crean donde está el .exe)
INPUTS_DIR = os.path.join(EXEC_DIR, 'inputs')
OUTPUTS_DIR = os.path.join(EXEC_DIR, 'outputs')

# Crear carpetas si no existen
os.makedirs(INPUTS_DIR, exist_ok=True)
os.makedirs(OUTPUTS_DIR, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_process', methods=['POST'])
def start_process():
    data = request.json
    year = data.get('year')
    codes_text = data.get('codes')
    start_cert = data.get('start_cert', 1)
    end_cert = data.get('end_cert')
    
    if not year or not codes_text:
        return jsonify({'status': 'error', 'message': 'Faltan datos'}), 400

    # 1. Procesar lista de códigos
    codes_list = [c.strip() for c in codes_text.replace(',', '\n').split('\n') if c.strip()]
    
    if not codes_list:
        return jsonify({'status': 'error', 'message': 'No se detectaron códigos válidos'}), 400

    # 2. Generar nombre de archivo con fecha y hora
    now = datetime.datetime.now()
    timestamp_str = now.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"request_{timestamp_str}.txt"
    filepath = os.path.join(INPUTS_DIR, filename)
    
    # 3. Guardar el TXT (con el rango para registro)
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"YEAR={year}\n")
            f.write(f"RANGE={start_cert}-{end_cert if end_cert else 'MAX'}\n")
            f.write("CODES=\n")
            for code in codes_list:
                f.write(f"{code}\n")
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Error guardando archivo: {str(e)}'}), 500

    # 4. Iniciar el Scraper
    thread = threading.Thread(target=run_scraper_process, args=(codes_list, year, OUTPUTS_DIR, start_cert, end_cert))
    thread.start()

    return jsonify({
        'status': 'success', 
        'message': f'Proceso iniciado. Rango: {start_cert} a {end_cert if end_cert else "Fin"}.',
        'file_saved': filename
    })

if __name__ == '__main__':
    # Abrir navegador automáticamente
    import webbrowser
    threading.Timer(1.5, lambda: webbrowser.open("http://127.0.0.1:5000")).start()
    
    print("Iniciando servidor MEF Scraper...")
    print("Accede en tu navegador a: http://127.0.0.1:5000")
    app.run(debug=False, use_reloader=False)
