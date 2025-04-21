import requests
import json
import os

# Datos de la API
API_KEY = "zpka_ed56a7576f47465095a2f3ee1d08c2ca_56c05972"  # Reemplaza con tu clave API real
URL = "https://heratropic-main-c6ba0ae.d2.zuplo.dev"  # URL de la API

# Función para enviar el video
def send_video(video_path):
    try:
        # Paso 1: Solicitar una URL prefirmada a la API
        print(f"Tamaño del archivo: {round((os.path.getsize(video_path) / (1024 * 1024)), 2)} MB")
        print("Subiendo archivo grande...")

        form_data = {
            "filename": "Dislexia1.mp4",
            "external_vars": json.dumps({})
        }
        headers = {
            "Authorization": f"Bearer {API_KEY}"
        }

        # Solicitud para obtener la URL prefirmada
        presign_response = requests.post(f"{URL}/v1/upload/large", data=form_data, headers=headers)

        if presign_response.status_code != 200:
            print("❌ Error al obtener la URL: ", presign_response.status_code, "-", presign_response.text)
            return None

        # Extraer las URLs de respuesta
        response_json = presign_response.json()
        presigned_url = response_json.get("response", {}).get("upload_url")
        result_url = response_json.get("response", {}).get("result_url")
        video_id = response_json.get("response", {}).get("id")

        if not presigned_url or not result_url or not video_id:
            print("❌ Respuesta inválida del servidor.")
            return None

        print(f"✅ URL prefirmada recibida: {presigned_url}")
        print(f"📁 ID del archivo subido: {video_id}")

        # Paso 2: Subir el video usando la URL prefirmada
        with open(video_path, "rb") as video_file:
            s3_upload_response = requests.put(presigned_url, data=video_file, headers={"Content-Type": "video/mp4"})

        if s3_upload_response.status_code != 200:
            print("❌ Error al subir el video a S3.")
            return None

        print("✅ Video subido con éxito a S3.")
        return video_id

    except Exception as error:
        print("❌ Error durante la subida del video:", error)
        return None

# Ejecución de la función
video_id = send_video("Videos/Dislexia1.mp4")
print(f"El ID del video subido es: {video_id}")
