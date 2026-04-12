import re

INPUT_FILE = "transcription_finale.txt"
OUTPUT_FILE = "transcription_nommee.txt"

replacements = {
    "SPEAKER_00": "Alice",
    "SPEAKER_01": "Bob",
    "SPEAKER_02": "Charlie",
}

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    content = f.read()

for old, new in replacements.items():
    content = re.sub(rf"\b{old}\b", new, content)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"✅ Fichier renommé : {OUTPUT_FILE}")
