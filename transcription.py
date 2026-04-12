import whisperx
import torch
import numpy as np
import pandas as pd
from collections import Counter
from pyannote.audio import Pipeline
from dotenv import load_dotenv
import os

# ============================================================
# CONFIGURATION
# ============================================================
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN") # Token Hugging Face

if not HF_TOKEN:
    raise ValueError("❌ HF_TOKEN manquant dans le fichier .env !")

AUDIO_FILE = "audio_file.mp3"
OUTPUT_FILE = "transcription_finale.txt"
WHISPER_MODEL = "medium"
LANGUAGE = "fr"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
COMPUTE_TYPE = "float16" if DEVICE == "cuda" else "int8"

print(f"⚙️  Utilisation : {DEVICE.upper()}")

# ============================================================
# ÉTAPE 1 : TRANSCRIPTION
# ============================================================
print("\n📝 Chargement du modèle Whisper...")
model = whisperx.load_model(WHISPER_MODEL, DEVICE, compute_type=COMPUTE_TYPE, language=LANGUAGE)

print("📝 Transcription en cours...")
audio = whisperx.load_audio(AUDIO_FILE)
result = model.transcribe(audio, batch_size=16)
print(f"✅ {len(result['segments'])} segments transcrits")

# ============================================================
# ÉTAPE 2 : ALIGNEMENT (timestamps précis au mot près)
# ============================================================
print("\n🎯 Alignement des timestamps...")
model_a, metadata = whisperx.load_align_model(language_code=LANGUAGE, device=DEVICE)
result = whisperx.align(result["segments"], model_a, metadata, audio, DEVICE)
print("✅ Alignement terminé")

# ============================================================
# ÉTAPE 3 : DIARISATION (qui parle quand)
# ============================================================
print("\n🔍 Identification des locuteurs...")

diarize_pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1",
    token=HF_TOKEN
)

# Convertir l'audio en tenseur pour pyannote
audio_tensor = torch.tensor(audio).unsqueeze(0)
sample_rate = 16000

diarize_segments = diarize_pipeline({
    "waveform": audio_tensor,
    "sample_rate": sample_rate
})

# Extraction de l'annotation depuis DiarizeOutput
annotation = diarize_segments.speaker_diarization

diarize_df = []
for turn, _, speaker in annotation.itertracks(yield_label=True):
    diarize_df.append({
        "start": turn.start,
        "end": turn.end,
        "speaker": speaker
    })

diarize_df = pd.DataFrame(diarize_df)
print(f"✅ {len(diarize_df)} segments de locuteurs détectés")

# Fusion transcription + diarisation
result = whisperx.assign_word_speakers(diarize_df, result)
print("✅ Locuteurs identifiés")

# ============================================================
# ÉTAPE 4 : SAUVEGARDE
# ============================================================
def format_timestamp(seconds):
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"

print(f"\n💾 Sauvegarde dans '{OUTPUT_FILE}'...")

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    current_speaker = None
    for segment in result["segments"]:
        speaker = segment.get("speaker", "Inconnu")
        text = segment.get("text", "").strip()
        start = segment.get("start", 0)

        if not text:
            continue

        if speaker != current_speaker:
            current_speaker = speaker
            f.write(f"\n[{current_speaker} - {format_timestamp(start)}]\n")

        f.write(text + " ")

print(f"✅ Transcription terminée ! Fichier : '{OUTPUT_FILE}'")

# ============================================================
# RÉSUMÉ DES INTERVENANTS
# ============================================================
speaker_counts = Counter(
    seg.get("speaker", "Inconnu")
    for seg in result["segments"]
    if seg.get("text", "").strip()
)

print("\n📊 Résumé des intervenants :")
for speaker, count in speaker_counts.most_common():
    print(f"   {speaker} : {count} interventions")
