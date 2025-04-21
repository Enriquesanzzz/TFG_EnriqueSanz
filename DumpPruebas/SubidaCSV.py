import requests
import json

# Datos de la API
API_KEY = "zpka_ed56a7576f47465095a2f3ee1d08c2ca_56c05972"
URL = "https://heratropic-main-c6ba0ae.d2.zuplo.dev"
result_url = "/v1/result/5540c1ae-4b95-46c8-b2bd-c5c68f9d3883"  # tu result_url

# Función recursiva para extraer todos los valores numéricos
def extraer_valores_numericos(data):
    valores = []
    if isinstance(data, dict):
        for v in data.values():
            valores += extraer_valores_numericos(v)
    elif isinstance(data, list):
        for item in data:
            valores += extraer_valores_numericos(item)
    elif isinstance(data, (int, float)):
        valores.append(data)
    return valores

# Función para obtener y mostrar resultados
def obtener_resultados_como_csv(result_url):
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    response = requests.get(f"{URL}{result_url}", headers=headers)
    if response.status_code == 200:
        data = response.json()
        print("✅ Resultado completo en formato diccionario:")
        print(json.dumps(data, indent=4))
        
        # Extraer solo la parte útil (response)
        response_data = data.get("response", {})
        valores_numericos = extraer_valores_numericos(response_data)

        print("\n📋 Valores numéricos separados por comas:")
        print(",".join(str(v) for v in valores_numericos))

    else:
        print(f"❌ Error al obtener resultados: {response.status_code} - {response.text}")

# Llamada
obtener_resultados_como_csv(result_url)
