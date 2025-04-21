# subida_masiva.py
import os
import json
import requests
import csv

API_KEY = "zpka_ed56a7576f47465095a2f3ee1d08c2ca_56c05972"
URL = "https://heratropic-main-c6ba0ae.d2.zuplo.dev"
VIDEOS_DIR = "Videos"
RESULTS_CSV = "urls_resultado.csv"


def obtener_presigned_url(filename):
    form_data = {
        "filename": filename,
        "external_vars": json.dumps({"id": "1"})
    }
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.post(f"{URL}/v1/upload/large", data=form_data, headers=headers)
    if response.status_code == 200:
        return response.json()["response"]["upload_url"], response.json()["response"]["result_url"]
    else:
        print(f"Error al obtener URL para {filename}: {response.text}")
        return None, None


def subir_video(presigned_url, path_local):
    with open(path_local, "rb") as video_file:
        response = requests.put(presigned_url, data=video_file, headers={"Content-Type": "video/mp4"})
    return response.status_code == 200


def main():
    with open(RESULTS_CSV, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["filename", "result_url"])

        for filename in os.listdir(VIDEOS_DIR):
            if filename.endswith(".mp4"):
                ruta_completa = os.path.join(VIDEOS_DIR, filename)
                upload_url, result_url = obtener_presigned_url(filename)
                if upload_url and result_url:
                    if subir_video(upload_url, ruta_completa):
                        print(f"✅ Subido {filename}")
                        writer.writerow([filename, result_url])
                    else:
                        print(f"❌ Fallo al subir {filename}")

if __name__ == "__main__":
    main()