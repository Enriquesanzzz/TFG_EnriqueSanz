import requests
import json
import csv

# Datos de la API
API_KEY = "zpka_ed56a7576f47465095a2f3ee1d08c2ca_56c05972"
URL = "https://heratropic-main-c6ba0ae.d2.zuplo.dev"
video_id = "394ea0bd-1455-4c65-bf55-c740fe8ec82f"  # Sustituye con el ID del video obtenido

# Función para obtener los resultados del análisis
def obtener_resultados(video_id):
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    response = requests.get(f"{URL}/v1/result/{video_id}", headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error al obtener resultados: {response.status_code} - {response.text}")
        return None

# Función para guardar los resultados en un archivo CSV
def guardar_csv(data, filename="resultados.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        
        # Escribir la cabecera (nombres de las columnas)
        header = ["emotion", "value", "agreeableness", "conscientiousness", "openness", "survival",
                  "compassion", "communication", "imagination", "awareness", "creativity", "self_esteem", 
                  "stress_high", "stress_medium", "stress_low", "depression_high", "depression_medium", 
                  "depression_low", "self_efficacy_high", "self_efficacy_medium", "self_efficacy_low"]
        writer.writerow(header)
        
        # Obtener valores del JSON
        response = data.get("response", {})
        status = response.get("status", {})
        traits = response.get("data", {}).get("traits", {})
        emotions = response.get("data", {}).get("emotions", {})
        
        # Extraer emociones
        emotion_values = [emotions.get(emotion, 0) for emotion in ["happy", "sad", "angry", "calm", "disgust", "fear", "surprised", "neutral"]]
        
        # Extraer rasgos de personalidad
        personality_values = [
            traits.get("agreeableness", 0), traits.get("conscientiousness", 0), traits.get("openness", 0), traits.get("survival", 0),
            traits.get("compassion", 0), traits.get("communication", 0), traits.get("imagination", 0), traits.get("awareness", 0), 
            traits.get("creativity", 0), traits.get("self_esteem", 0)
        ]
        
        # Extraer métricas de estrés, depresión y autoeficacia
        stress = traits.get("stress", {})
        depression = traits.get("depression", {})
        self_efficacy = traits.get("self_efficacy", {})

        stress_values = [stress.get(level, 0) for level in ["high", "medium", "low"]]
        depression_values = [depression.get(level, 0) for level in ["high", "medium", "low"]]
        self_efficacy_values = [self_efficacy.get(level, 0) for level in ["high", "medium", "low"]]

        # Unir todos los valores en una fila
        row = emotion_values + personality_values + stress_values + depression_values + self_efficacy_values
        writer.writerow(row)

    print(f"✅ Resultados guardados en {filename}")

# Obtener los resultados de la API
data = obtener_resultados(video_id)

# Guardar en CSV si se obtuvieron resultados
if data:
    guardar_csv(data)
