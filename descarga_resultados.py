import csv
import os
import subprocess
import json

API_KEY = "zpka_ed56a7576f47465095a2f3ee1d08c2ca_56c05972"
BASE_URL = "https://heratropic-main-c6ba0ae.d2.zuplo.dev"

# Aseguramos que existe la carpeta resultados/
os.makedirs("resultados", exist_ok=True)

# Leemos el CSV
with open("urls_resultado.csv", newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        filename = row["filename"]
        result_url = row["result_url"]
        full_url = f"{BASE_URL}{result_url}"

        output_path = os.path.join("resultados", filename.replace(".mp4", ".json"))

        print(f"📡 Obteniendo resultado para {filename}...")

        try:
            # Ejecutamos el curl como lo harías tú
            command = [
                "curl", "-s", "-X", "GET", full_url,
                "-H", f"Authorization: Bearer {API_KEY}"
            ]
            result = subprocess.run(command, capture_output=True, encoding="utf-8")

            if result.returncode == 0:
                response_text = result.stdout

                # Intentamos parsear para validar que es JSON
                try:
                    data = json.loads(response_text)
                    with open(output_path, "w", encoding="utf-8") as f:
                        json.dump(data, f, indent=4)
                    print(f"✅ Guardado en {output_path}")
                except json.JSONDecodeError:
                    print(f"❌ Respuesta no válida de {filename}")
            else:
                print(f"❌ Error ejecutando curl: {result.stderr}")

        except Exception as e:
            print(f"❌ Fallo general con {filename}: {e}")
