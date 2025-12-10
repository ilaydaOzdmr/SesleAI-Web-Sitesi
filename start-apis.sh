#!/bin/bash
# Backend API'lerini başlatma scripti (Linux/Mac)

# Environment variables
export W2V_CLASSIFIER_PATH="./backend/models/wav2vec2_model.h5"
export W2V_LABELS_PATH="./backend/models/classes.npy"
export CORS_ORIGINS="${CORS_ORIGINS:-http://localhost:5173,http://127.0.0.1:5173}"

# Logs klasörü oluştur
mkdir -p logs

# Speaker API'yi arka planda başlat
cd backend/api
uvicorn main:app --host 0.0.0.0 --port 8000 > ../../logs/speaker-api.log 2>&1 &
SPEAKER_PID=$!
echo "Speaker API başlatıldı (PID: $SPEAKER_PID)"

# Emotion API'yi arka planda başlat
uvicorn wav2vec_emotion_api:app --host 0.0.0.0 --port 8001 > ../../logs/emotion-api.log 2>&1 &
EMOTION_PID=$!
echo "Emotion API başlatıldı (PID: $EMOTION_PID)"

# PID'leri dosyaya kaydet
echo $SPEAKER_PID > ../../logs/speaker-api.pid
echo $EMOTION_PID > ../../logs/emotion-api.pid

echo "Her iki API de başlatıldı!"
echo "Speaker API: http://localhost:8000"
echo "Emotion API: http://localhost:8001"
echo ""
echo "Durdurmak için: ./stop-apis.sh"


