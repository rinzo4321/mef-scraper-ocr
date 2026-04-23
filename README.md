# MEF Scraper & CAPTCHA Solver

Este proyecto es un automatizador de consultas para el portal del Ministerio de Economía y Finanzas (MEF) de Perú. Utiliza una red neuronal customizada para resolver CAPTCHAs y extrae información de certificados de Unidades Ejecutoras automáticamente.

## 🚀 Características

- **Web Scraping:** Automatización con Selenium para navegar el portal del MEF.
- **IA OCR:** Modelo CRNN (CNN + LSTM) entrenado con TensorFlow para resolver CAPTCHAs de 5 caracteres.
- **Interfaz Web:** Interfaz simple construida con Flask para facilitar el uso al usuario final.
- **Búsqueda Inteligente:** Capacidad de escanear rangos de certificados y detectar huecos en la numeración (hasta 15 consecutivos).
- **Exportación a Excel:** Genera reportes con formato profesional (fechas y montos detectados automáticamente).

## 🛠️ Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/mef-scraper-ocr.git
   cd mef-scraper-ocr
   ```

2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Ejecuta la aplicación:
   ```bash
   python app.py
   ```

## 📝 Notas
- El modelo de IA (`model.h5`) no está incluido en este repositorio debido a su peso. Debe colocarse en la carpeta `Models/custom_captcha/`.
- Asegúrate de tener Google Chrome instalado para que Selenium funcione correctamente.

---
Desarrollado con Python, Selenium y TensorFlow.
