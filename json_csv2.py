import os
import json
import csv

json_folder = "resultados"
output_csv = "resultados_final.csv"

cabecera = [
    "created_at", "aid", "extension", "format", "duration", "FILE_STORED", "FACIAL_ANALYSED",
    "VOICE_ANALYSED", "VOICE_TRANSCRIBED", "BIOMETRICS_EXTRACTED", "SPEECH_ANALYSED", "PERSONALITY_ANALYSED",
    "FACES_EXTRACTED", "id", "angry_facial", "disgust_facial", "fear_facial", "happy_facial", "sad_facial",
    "surprise_facial", "neutral_facial", "most_frequent_dominant_emotion", "dominant_emotion_counts_surprise",
    "average_face_confidence", "extraversion", "neuroticism", "agreeableness", "conscientiousness", "openness",
    "survival", "creativity", "self_esteem", "compassion", "communication", "imagination", "awareness",
    "stress_high", "stress_medium", "stress_low", "helplessness_high", "helplessness_medium", "helplessness_low",
    "self_efficacy_medium", "self_efficacy_low", "self_efficacy_high", "depression_high", "depression_medium",
    "depression_low", "voice_mean", "voice_sd", "voice_median", "voice_mode", "voice_Q25", "voice_Q75", "voice_IQR",
    "voice_skewness", "voice_kurtosis", "voice_mean_note", "voice_median_note", "voice_mode_note", "voice_Q25_note",
    "voice_Q75_note", "voice_rmse", "pitch", "tone", "sad_voice", "disgust_voice", "fearful_voice", "neutral_voice",
    "happy_voice", "angry_voice", "calm_voice", "language", "surprised_voice", "no_speech_prob", "entropy",
    "tense_past", "tense_present", "tense_future", "sentiment_polarity", "sentiment_subjectivity", "variable"
]

def get_value(obj, *keys):
    for key in keys:
        if not isinstance(obj, dict):
            return "null"
        obj = obj.get(key, {})
    return obj if isinstance(obj, (int, float, str)) else "null"

def detectar_variable(nombre_archivo):
    nombre = nombre_archivo.lower()
    if "adhd" in nombre or "tdah" in nombre:
        return "TDAH"
    elif "autismo" in nombre or "asperger" in nombre:
        return "Autismo"
    elif "dislexia" in nombre:
        return "Dislexia"
    elif "dispraxia" in nombre:
        return "Dispraxia"
    return "Desconocido"

with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(cabecera)

    for filename in os.listdir(json_folder):
        if filename.endswith(".json"):
            ruta = os.path.join(json_folder, filename)
            try:
                with open(ruta, "r", encoding="utf-8") as f:
                    data = json.load(f)["response"]

                video = data.get("original_file", {})
                status = data.get("status", {})
                traits = data.get("data", {}).get("traits", {})
                facial = data.get("data", {}).get("facial", {}).get("average_emotions", {})
                face_info = data.get("data", {}).get("facial", {})
                voice = data.get("data", {}).get("voice", {}).get("frequencies", {})
                if not isinstance(voice, dict):
                    voice = {}
                voice_emotions = data.get("data", {}).get("voice", {}).get("emotions", {})
                if not isinstance(voice_emotions, dict):
                    voice_emotions = {}
                speech = data.get("data", {}).get("speech", {})
                if not isinstance(speech, dict):
                    speech = {}
                tense = speech.get("tense", {})
                if not isinstance(tense, dict):
                    tense = {}
                sentiment = speech.get("sentiment", {})
                if not isinstance(sentiment, dict):
                    sentiment = {}

                row = [
                    data.get("created_at", "null"),
                    data.get("aid", "null"),
                    video.get("extension", "null"),
                    video.get("format", "null"),
                    video.get("duration", "null"),
                    status.get("FILE_STORED", "null"),
                    status.get("FACIAL_ANALYSED", "null"),
                    status.get("VOICE_ANALYSED", "null"),
                    status.get("VOICE_TRANSCRIBED", "null"),
                    status.get("BIOMETRICS_EXTRACTED", "null"),
                    status.get("SPEECH_ANALYSED", "null"),
                    status.get("PERSONALITY_ANALYSED", "null"),
                    status.get("FACES_EXTRACTED", "null"),
                    data.get("external_vars", {}).get("id", "null"),
                    facial.get("angry", "null"),
                    facial.get("disgust", "null"),
                    facial.get("fear", "null"),
                    facial.get("happy", "null"),
                    facial.get("sad", "null"),
                    facial.get("surprise", "null"),
                    facial.get("neutral", "null"),
                    face_info.get("most_frequent_dominant_emotion", "null"),
                    face_info.get("dominant_emotion_counts", {}).get("surprise", "null"),
                    face_info.get("average_face_confidence", "null"),
                    traits.get("extraversion", "null"),
                    traits.get("neuroticism", "null"),
                    traits.get("agreeableness", "null"),
                    traits.get("conscientiousness", "null"),
                    traits.get("openness", "null"),
                    get_value(traits, "survival"),
                    get_value(traits, "creativity"),
                    get_value(traits, "self_esteem"),
                    get_value(traits, "compassion"),
                    get_value(traits, "communication"),
                    get_value(traits, "imagination"),
                    get_value(traits, "awareness"),
                    get_value(traits, "stress", "high"),
                    get_value(traits, "stress", "medium"),
                    get_value(traits, "stress", "low"),
                    get_value(traits, "helplessness", "high"),
                    get_value(traits, "helplessness", "medium"),
                    get_value(traits, "helplessness", "low"),
                    get_value(traits, "self_efficacy", "medium"),
                    get_value(traits, "self_efficacy", "low"),
                    get_value(traits, "self_efficacy", "high"),
                    get_value(traits, "depression", "high"),
                    get_value(traits, "depression", "medium"),
                    get_value(traits, "depression", "low"),
                    voice.get("mean", "null"),
                    voice.get("sd", "null"),
                    voice.get("median", "null"),
                    voice.get("mode", "null"),
                    voice.get("Q25", "null"),
                    voice.get("Q75", "null"),
                    voice.get("IQR", "null"),
                    voice.get("skewness", "null"),
                    voice.get("kurtosis", "null"),
                    voice.get("mean_note", "null"),
                    voice.get("median_note", "null"),
                    voice.get("mode_note", "null"),
                    voice.get("Q25_note", "null"),
                    voice.get("Q75_note", "null"),
                    voice.get("rmse", "null"),
                    get_value(data, "data", "voice", "pitch"),
                    get_value(data, "data", "voice", "tone"),
                    voice_emotions.get("sad", "null"),
                    voice_emotions.get("disgust", "null"),
                    voice_emotions.get("fearful", "null"),
                    voice_emotions.get("neutral", "null"),
                    voice_emotions.get("happy", "null"),
                    voice_emotions.get("angry", "null"),
                    voice_emotions.get("calm", "null"),
                    speech.get("language", "null"),
                    voice_emotions.get("surprised", "null"),
                    speech.get("no_speech_prob", "null"),
                    speech.get("entropy", "null"),
                    tense.get("past", "null"),
                    tense.get("present", "null"),
                    tense.get("future", "null"),
                    sentiment.get("polarity", "null"),
                    sentiment.get("subjectivity", "null"),
                    detectar_variable(filename)
                ]

                writer.writerow(row)
                print(f"✅ Fila añadida para {filename}")

            except Exception as e:
                print(f"❌ Error procesando {filename}: {e}")
