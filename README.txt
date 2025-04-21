# Proyecto TFG – Pipeline de Análisis de Vídeos con IA

Este proyecto automatiza la subida, análisis y conversión de vídeos de YouTube para generar un dataset en CSV con características de voz, expresión facial, personalidad y más, incluyendo una etiqueta de neurodivergencia (`variable`).

## 🔁 Flujo de scripts

### 1. `subida_masiva.py`
- 📂 Lee todos los vídeos `.mp4` en la carpeta `Videos/`.
- 🚀 Los sube a la API de Heratropic mediante URL prefirmada.
- 🔗 Guarda un CSV `urls_resultado.csv` con el nombre de cada vídeo y su `result_url` correspondiente.

> Requiere: carpeta `Videos/` con vídeos  
> Genera: `urls_resultado.csv`

---

### 2. `descarga_resultados.py`
- 📑 Lee el archivo `urls_resultado.csv`.
- 🔄 Realiza una petición `curl` a cada `result_url` con tu API Key.
- 💾 Guarda la respuesta (formato JSON) en la carpeta `resultados/` usando el nombre del vídeo.

> Requiere: `urls_resultado.csv`  
> Genera: `.json` individuales en `resultados/`

---

### 3. `json_csv.py`
- 📥 Lee todos los `.json` de `resultados/`.
- 📊 Extrae los campos necesarios y los ordena según una cabecera específica.
- ➕ Añade una última columna llamada `variable` (neurodivergencia) deducida del nombre del archivo.
- 🧾 Genera el CSV final `resultados_final.csv`.

> Requiere: carpeta `resultados/` con `.json`  
> Genera: `resultados_final.csv`

---

## 📂 Estructura esperada del proyecto

