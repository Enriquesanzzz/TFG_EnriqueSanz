import os
import json
import pandas as pd

carpeta_json = "DumpJSON_TFG"
csv_inicial = "CSV_DEF_REG.csv"
csv_salida = "dataset_con_texto.csv"

# Cargar CSV original
df = pd.read_csv(csv_inicial)

# Añadir columnas nuevas
df["text"] = None
df["translation"] = None

# Recorremos los JSONs
for fname in os.listdir(carpeta_json):
    if fname.endswith(".json"):
        try:
            with open(os.path.join(carpeta_json, fname), "r", encoding="utf-8") as f:
                data = json.load(f)

            # Usamos el 'aid' como identificador
            aid = data.get("response", {}).get("aid", None)
            if not aid:
                print(f"{fname}: campo 'aid' no encontrado.")
                continue

            speech_data = data.get("response", {}).get("data", {}).get("speech", {})
            text = speech_data.get("text", "null")

            translation = data.get("response", {}).get("data", {}).get("translation", "null")

            # Reemplazamos en la fila correspondiente
            df.loc[df["aid"] == aid, "text"] = text
            df.loc[df["aid"] == aid, "translation"] = translation

        except Exception as e:
            print(f"Error con el archivo {fname}: {e}")

# Guardamos resultado final
df.to_csv(csv_salida, index=False, encoding="utf-8")
print(f"\n✅ CSV generado: {csv_salida}")
