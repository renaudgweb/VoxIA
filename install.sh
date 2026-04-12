#!/bin/bash
# install.sh - Script d'installation de l'environnement WhisperX

set -e  # Arrêter en cas d'erreur

# ============================================================
# COULEURS
# ============================================================
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# ============================================================
# CONFIGURATION
# ============================================================
VENV_NAME="whisperx-env"

# ============================================================
# FONCTIONS
# ============================================================
ok()   { echo -e "${GREEN}✅ $1${NC}"; }
warn() { echo -e "${YELLOW}⚠️  $1${NC}"; }
err()  { echo -e "${RED}❌ $1${NC}"; exit 1; }

# ============================================================
# ÉTAPE 1 : DÉPENDANCES SYSTÈME
# ============================================================
echo -e "\n📦 Installation des dépendances système..."

sudo apt update -q
sudo apt install -y python3-venv ffmpeg
ok "Dépendances système installées"

# ============================================================
# ÉTAPE 2 : ENVIRONNEMENT VIRTUEL
# ============================================================
echo -e "\n🐍 Création de l'environnement virtuel '$VENV_NAME'..."

if [ -d "$VENV_NAME" ]; then
    warn "L'environnement '$VENV_NAME' existe déjà, on le recrée..."
    rm -rf "$VENV_NAME"
fi

python3 -m venv "$VENV_NAME"
ok "Environnement virtuel créé"

# Activer le venv
source "$VENV_NAME/bin/activate"
ok "Environnement virtuel activé"

# ============================================================
# ÉTAPE 3 : MISE À JOUR DE PIP
# ============================================================
echo -e "\n⬆️  Mise à jour de pip..."
pip install --upgrade pip -q
ok "pip mis à jour"

# ============================================================
# ÉTAPE 4 : INSTALLATION DES PAQUETS
# ============================================================
echo -e "\n📥 Installation de PyTorch (CPU)..."
pip install torch torchvision torchaudio -q
ok "PyTorch installé"

echo -e "\n📥 Installation de WhisperX..."
pip install whisperx -q
ok "WhisperX installé"

echo -e "\n📥 Installation de Pyannote..."
pip install pyannote.audio -q
ok "Pyannote installé"

echo -e "\n📥 Installation de Pandas / Numpy..."
pip install pandas numpy -q
ok "Pandas et Numpy installés"

echo -e "\n📥 Installation de python-dotenv..."
pip install python-dotenv -q
ok "python-dotenv installé"

# Créer le .env s'il n'existe pas
if [ ! -f ".env" ]; then
    echo 'HF_TOKEN=hf_xxx...' > .env
    warn "Fichier .env créé — pensez à y mettre votre vrai token !"
fi

# Créer le .gitignore
if [ ! -f ".gitignore" ]; then
    cat > .gitignore << 'EOF'
.env
whisperx-env/
__pycache__/
*.pyc
*.mp3
*.mp4
transcription_finale.txt
EOF
    ok ".gitignore créé"
fi

# ============================================================
# ÉTAPE 5 : GÉNÉRATION DU requirements.txt
# ============================================================
echo -e "\n📄 Génération du requirements.txt..."
pip freeze > requirements.txt
ok "requirements.txt généré"

# ============================================================
# ÉTAPE 6 : VÉRIFICATION
# ============================================================
echo -e "\n🔍 Vérification de l'installation..."

python3 -c "
import torch
import whisperx
import pyannote.audio
import pandas as pd
import numpy as np
print('  torch     :', torch.__version__)
print('  whisperx  : OK')
print('  pyannote  : OK')
print('  pandas    :', pd.__version__)
print('  numpy     :', np.__version__)
"

ok "Tous les packages sont fonctionnels"

# ============================================================
# FIN
# ============================================================
echo -e "\n${GREEN}🎉 Installation terminée avec succès !${NC}"
echo -e "Pour activer l'environnement plus tard :"
echo -e "  ${YELLOW}source $VENV_NAME/bin/activate${NC}"
echo -e "Pour lancer la transcription :"
echo -e "  ${YELLOW}python3 transcription.py${NC}\n"
