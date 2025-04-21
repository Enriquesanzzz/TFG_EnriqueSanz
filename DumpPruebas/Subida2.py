import requests
import json
import os

# Datos de la API
API_KEY = "zpka_ed56a7576f47465095a2f3ee1d08c2ca_56c05972"
URL = "https://heratropic-main-c6ba0ae.d2.zuplo.dev"

# Ruta relativa del video
video_path = "Videos/Dislexia3.mp4"

# Función para obtener el tamaño del archivo en MB
def obtener_tamano_archivo(filepath):
    return os.path.getsize(filepath) / (1024 * 1024)

# Función para obtener la URL prefirmada (para archivos grandes)
def obtener_presigned_url(filename):
    form_data = {
        "filename": filename,
        "external_vars": json.dumps({"id": "1"})
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    response = requests.post(f"{URL}/v1/upload/large", data=form_data, headers=headers)
    if response.status_code == 200:
        presigned_url = response.json()["response"]["upload_url"]
        result_url = response.json()["response"]["result_url"]
        print(f"✅ URL prefirmada recibida: {presigned_url}")
        print(f"🔗 URL para obtener resultados: {result_url}")  # <-- AÑADIR ESTA LÍNEA
        return presigned_url, result_url
    else:
        print(f"❌ Error al obtener la URL: {response.status_code} - {response.text}")
        return None, None

# Función para subir el video usando la URL prefirmada
def subir_video(presigned_url, video_path):
    try:
        with open(video_path, "rb") as video_file:
            response = requests.put(presigned_url, data=video_file, headers={"Content-Type": "video/mp4"})
            if response.status_code == 200:
                print("✅ Video subido correctamente.")
            else:
                print(f"❌ Error al subir el video: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error durante la subida: {str(e)}")

# Función para obtener los resultados de la API después de subir el vídeo
def obtener_resultados(result_url):
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    response = requests.get(f"{URL}{result_url}", headers=headers)
    if response.status_code == 200:
        data = response.json()
        print("✅ Resultados obtenidos:")
        print(json.dumps(data, indent=4))
    else:
        print(f"❌ Error al obtener resultados: {response.status_code} - {response.text}")

# Proceso completo
try:
    tamano_mb = obtener_tamano_archivo(video_path)
    print(f"📁 Tamaño del archivo: {tamano_mb:.2f} MB")

    if tamano_mb > 5:
        print("🚀 Subiendo archivo grande...")
        upload_url, result_url = obtener_presigned_url(os.path.basename(video_path))
        if upload_url:
            subir_video(upload_url, video_path)
            if result_url:
                obtener_resultados(result_url)
    else:
        print("❗ El archivo es demasiado pequeño para el método de subida de grandes archivos.")
except FileNotFoundError:
    print(f"❌ El archivo '{video_path}' no existe.")
