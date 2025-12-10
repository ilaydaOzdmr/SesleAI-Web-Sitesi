# Backend API'lerini başlatma scripti (Windows PowerShell)

# Environment variables
$env:W2V_CLASSIFIER_PATH = "C:\Users\MONSTER\Desktop\sesleAI Proje Web Sitesi\backend\models\wav2vec2_model.h5"
$env:W2V_LABELS_PATH = "C:\Users\MONSTER\Desktop\sesleAI Proje Web Sitesi\backend\models\classes.npy"
$env:CORS_ORIGINS = if ($env:CORS_ORIGINS) { $env:CORS_ORIGINS } else { "http://localhost:5173,http://127.0.0.1:5173" }

# Logs klasörü oluştur
New-Item -ItemType Directory -Force -Path "logs" | Out-Null

# Speaker API'yi başlat
Write-Host "Speaker API başlatılıyor..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\backend\api'; conda activate voice_env; uvicorn main:app --host 0.0.0.0 --port 8000" -WindowStyle Normal

# Kısa bir bekleme
Start-Sleep -Seconds 2

# Emotion API'yi başlat
Write-Host "Emotion API başlatılıyor..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\backend\api'; conda activate voice_env; uvicorn wav2vec_emotion_api:app --host 0.0.0.0 --port 8001" -WindowStyle Normal

Write-Host ""
Write-Host "Her iki API de başlatıldı!"
Write-Host "Speaker API: http://localhost:8000"
Write-Host "Emotion API: http://localhost:8001"
Write-Host ""
Write-Host "API'leri durdurmak için pencereleri kapatın."


