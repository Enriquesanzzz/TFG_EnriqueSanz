import requests
import json

# Datos de la API
API_KEY = "Zpka_ed56a7576f47465095a2f3ee1d08c2ca_56c05972"
URL = "https://heratropic-main-c6ba0ae.d2.zuplo.dev"

# Ruta relativa del video (dentro de la carpeta del TFG)
video_path = "Videos/Autismo1.mp4"

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
        print(f"✅ URL de subida recibida: {presigned_url}")
        return presigned_url, result_url
    else:
        print(f"❌ Error al obtener la URL: {response.status_code} - {response.text}")
        return None, None

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
upload_url, result_url = obtener_presigned_url("Autismo1.mp4")
if upload_url:
    subir_video(upload_url, video_path)

if result_url:
    obtener_resultados(result_url)