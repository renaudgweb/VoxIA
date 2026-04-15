<p align="center">
  <img src="assets/logo.png" alt="VoxIA logo" width="200"/>
</p>

# 🎙️ VoxIA — Transcription intelligente avec WhisperX

**VoxIA** est un outil de transcription automatique de réunions audio/vidéo avec identification des locuteurs (diarisation).

Basé sur :
- WhisperX (transcription rapide et précise)
- pyannote.audio (diarisation des intervenants)

---

## ✨ Fonctionnalités

- 📝 Transcription audio → texte
- 🎯 Alignement précis des timestamps
- 🧑‍🤝‍🧑 Identification automatique des locuteurs
- ⚡ Utilisable en local (CPU ou GPU)
- 🔐 Traitement local des données (aucun envoi externe)

---

## 📋 Prérequis

- Ubuntu / Debian
- Python 3.10+
- Connexion internet (pour télécharger les modèles)
- Un compte [Hugging Face](https://huggingface.co) (gratuit)

---

## 🔑 Étape 1 : Créer un token Hugging Face

1. Créez un compte sur [https://huggingface.co](https://huggingface.co)
2. Allez dans **Settings > Access Tokens** :
   👉 [https://hf.co/settings/tokens](https://huggingface.co/settings/tokens)
3. Cliquez sur **"New token"**
4. Donnez-lui un nom (ex: `whisperx`) et choisissez le rôle **"Read"**
5. Copiez le token généré (commence par `hf_...`)

---

## ✅ Étape 2 : Accepter les conditions des modèles pyannote

> ⚠️ Cette étape est **obligatoire**, même avec un token valide.

### Modèle de diarisation
1. Allez sur 👉 [https://hf.co/pyannote/speaker-diarization-3.1](https://huggingface.co/pyannote/speaker-diarization-3.1)
2. Remplissez le formulaire :
   - **Company/university** : `Personal` (ou votre employeur)
   - **Website** : laissez vide ou mettez `https://github.com`
3. Cochez **"I agree to the terms"**
4. Cliquez sur **"Accept"**

### Modèle de segmentation
1. Allez sur 👉 [https://hf.co/pyannote/segmentation-3.0](https://huggingface.co/pyannote/segmentation-3.0)
2. Répétez les mêmes étapes

---

## ⚙️ Étape 3 : Configurer le token

Créez un fichier `.env` à la racine du projet :

```bash
echo 'HF_TOKEN=hf_xxx...' > .env
```

Remplacez `hf_xxx...` par votre vrai token Hugging Face.

---

## 🚀 Étape 4 : Lancer l'installation

```bash
# Rendre le script exécutable
chmod +x install.sh

# Lancer l'installation
./install.sh
```

Le script va automatiquement :
- Installer `python3-venv` et `ffmpeg`
- Créer l'environnement virtuel `whisperx-env`
- Installer tous les packages Python nécessaires
- Générer le `requirements.txt`
- Vérifier que tout fonctionne

---

## 🎬 Étape 5 : Préparer votre fichier audio

Extrayez la piste audio de votre vidéo avec ffmpeg :

```bash
ffmpeg -i reunion.mp4 -ar 16000 -ac 1 -c:a pcm_s16le audio.wav
```

Ou si vous avez déjà un MP3 :

```bash
# Vérifier que le fichier est lisible
ffmpeg -i reunion.mp3
```

Placez votre fichier audio dans le dossier du projet et mettez à jour `AUDIO_FILE` dans `transcription.py` si nécessaire.

---

## ▶️ Étape 6 : Lancer la transcription

```bash
# Activer l'environnement virtuel
source whisperx-env/bin/activate

# Lancer le script
python3 transcription.py
```

Vous devriez voir défiler :

```
⚙️  Utilisation : CPU
📝 Chargement du modèle Whisper...
📝 Transcription en cours...
✅ 342 segments transcrits
🎯 Alignement des timestamps...
✅ Alignement terminé
🔍 Identification des locuteurs...
✅ Locuteurs identifiés
💾 Sauvegarde dans 'transcription_finale.txt'...
✅ Transcription terminée !

📊 Résumé des intervenants :
   SPEAKER_00 : 128 interventions
   SPEAKER_01 : 97 interventions
   SPEAKER_02 : 54 interventions
```

---

## 📄 Résultat

Le fichier `transcription_finale.txt` contiendra :

```
[SPEAKER_00 - 00:00]
Bonjour à tous, on va commencer la réunion aujourd'hui.

[SPEAKER_01 - 00:52]
Oui tout à fait, le premier point concerne le budget.

[SPEAKER_00 - 01:30]
Merci. Est-ce que quelqu'un a des questions ?
```

---

## ✏️ Renommer les locuteurs

Une fois la transcription générée, éditez et relancez ce script :

```python
# rename.py
replacements = {
    "SPEAKER_00": "Alice",
    "SPEAKER_01": "Bob",
    "SPEAKER_02": "Charlie",
}

with open("transcription_finale.txt", "r", encoding="utf-8") as f:
    content = f.read()

for old, new in replacements.items():
    content = content.replace(old, new)

with open("transcription_nommee.txt", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Fichier renommé sauvegardé !")
```

```bash
python3 rename.py
```

---

## 📦 Packages installés

| Package | Rôle |
|---------|------|
| `torch` | Moteur de calcul (IA) |
| `whisperx` | Transcription audio → texte |
| `pyannote.audio` | Identification des locuteurs |
| `pandas` | Manipulation des données |
| `numpy` | Calcul numérique |
| `python-dotenv` | Gestion du token HF |

---

## 🗂️ Structure du projet

```
transcription/
├── whisperx-env/            # Environnement virtuel (ignoré par git)
├── reunion.mp3              # Fichier audio source
├── transcription.py         # Script principal
├── rename.py                # Script de renommage des locuteurs
├── install.sh               # Script d'installation
├── requirements.txt         # Dépendances Python
├── .env                     # Token Hugging Face (ignoré par git)
├── .gitignore               # Fichiers ignorés par git
└── README.md                # Ce fichier
```

---

## ⏱️ Estimation des temps de traitement (CPU)

Pour une réunion d'1 heure :

| Modèle | Temps estimé |
|--------|-------------|
| `small` | ~20-30 min |
| `medium` | ~40-60 min |
| `large` | ~90-120 min |

> Le modèle `medium` offre le meilleur compromis qualité/vitesse pour le français.

---

## 🐛 Erreurs fréquentes

| Erreur | Cause | Solution |
|--------|-------|----------|
| `ModuleNotFoundError` | Venv non activé | `source whisperx-env/bin/activate` |
| `FileNotFoundError` | Mauvais dossier | `cd` vers le bon dossier |
| `403 Forbidden` | Conditions HF non acceptées | Voir Étape 2 |
| `401 Unauthorized` | Token HF invalide | Vérifier le `.env` |
| `ffmpeg not found` | ffmpeg manquant | `sudo apt install ffmpeg` |
| Circular import whisperx | Fichier nommé `whisperx.py` | Renommer en `transcription.py` |

---

## 📝 Notes

- Le token Hugging Face ne doit **jamais** être commité dans git
- Le fichier `.env` est automatiquement ignoré par `.gitignore`
- WhisperX ne distingue pas les locuteurs par leur nom, uniquement par `SPEAKER_00`, `SPEAKER_01`, etc.
- Pour de meilleurs résultats, utilisez un fichier audio de bonne qualité (peu de bruit de fond)
