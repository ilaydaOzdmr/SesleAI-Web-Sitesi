import os
import uvicorn
import urllib.request
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from speaker_api import SpeakerRecognitionAPI

# Model dosyalarını runtime'da indir (build size'ı küçültmek için)
def download_models_if_needed():
    """Model dosyalarını runtime'da indir (eğer yoksa)"""
    model_path = os.environ.get("W2V_CLASSIFIER_PATH", "/app/backend/models/wav2vec2_model.h5")
    label_path = os.environ.get("W2V_LABELS_PATH", "/app/backend/models/classes.npy")
    
    model_url = os.environ.get("MODEL_DOWNLOAD_URL", "")
    label_url = os.environ.get("LABEL_DOWNLOAD_URL", "")
    
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    
    if model_url and not os.path.exists(model_path):
        print(f"Downloading model from {model_url}...")
        try:
            urllib.request.urlretrieve(model_url, model_path)
            print("Model downloaded successfully!")
        except Exception as e:
            print(f"Failed to download model: {e}")
    
    if label_url and not os.path.exists(label_path):
        print(f"Downloading labels from {label_url}...")
        try:
            urllib.request.urlretrieve(label_url, label_path)
            print("Labels downloaded successfully!")
        except Exception as e:
            print(f"Failed to download labels: {e}")

# Startup'ta model dosyalarını indir
download_models_if_needed()

# FastAPI uygulamasını başlat
app = FastAPI()

# CORS ayarları
# Production için environment variable'dan al, yoksa localhost kullan
allowed_origins = os.environ.get("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",")
origins = [origin.strip() for origin in allowed_origins]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    api = SpeakerRecognitionAPI()
except Exception as e:
    print(f"API başlatılırken bir hata oluştu: {e}")
    api = None

@app.get("/")
def read_root():
    return {"message": "Ses Kimlik Tespiti API'si çalışıyor."}

@app.post("/register/")
async def register_speaker(name: str, audio_files: list[UploadFile] = File(...)):
    if not api:
        return JSONResponse(status_code=500, content={"error": "API başlatılamadı."})

    temp_audio_paths = []
    for audio_file in audio_files:
        temp_audio_path = os.path.join(os.getcwd(), audio_file.filename)
        with open(temp_audio_path, "wb") as f:
            f.write(await audio_file.read())
        temp_audio_paths.append(temp_audio_path)

    success, message = api.register_speaker_with_multiple_files(name, temp_audio_paths)

    for temp_path in temp_audio_paths:
        os.remove(temp_path)

    if success:
        return JSONResponse(status_code=200, content={"message": message})
    else:
        return JSONResponse(status_code=400, content={"error": message})

@app.post("/recognize/")
async def recognize_speaker(audio_file: UploadFile = File(...)):
    if not api:
        return JSONResponse(status_code=500, content={"error": "API başlatılamadı."})
    
    temp_audio_path = os.path.join(os.getcwd(), audio_file.filename)
    with open(temp_audio_path, "wb") as f:
        f.write(await audio_file.read())

    success, result = api.recognize_speaker(temp_audio_path)

    os.remove(temp_audio_path)

    if success:
        return JSONResponse(status_code=200, content=result)
    else:
        return JSONResponse(status_code=404, content={"error": result})

@app.post("/update_speaker/")
async def update_speaker(name: str, audio_files: list[UploadFile] = File(...)):
    if not api:
        return JSONResponse(status_code=500, content={"error": "API başlatılamadı."})
    
    temp_audio_paths = []
    for audio_file in audio_files:
        temp_audio_path = os.path.join(os.getcwd(), audio_file.filename)
        with open(temp_audio_path, "wb") as f:
            f.write(await audio_file.read())
        temp_audio_paths.append(temp_audio_path)

    success, message = api.update_speaker(name, temp_audio_paths)

    for temp_path in temp_audio_paths:
        os.remove(temp_path)

    if success:
        return JSONResponse(status_code=200, content={"message": message})
    else:
        return JSONResponse(status_code=400, content={"error": message})

@app.post("/correct_guess/")
async def correct_guess(name: str, audio_file: UploadFile = File(...)):
    if not api:
        return JSONResponse(status_code=500, content={"error": "API başlatılamadı."})
    
    temp_audio_path = os.path.join(os.getcwd(), audio_file.filename)
    with open(temp_audio_path, "wb") as f:
        f.write(await audio_file.read())

    success, message = api.correct_guess(name, [temp_audio_path])

    os.remove(temp_audio_path)

    if success:
        return JSONResponse(status_code=200, content={"message": message})
    else:
        return JSONResponse(status_code=400, content={"error": message})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
