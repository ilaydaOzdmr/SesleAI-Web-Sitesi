from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydub import AudioSegment
import uvicorn
import torch
import torchaudio
import numpy as np
from tensorflow.keras.models import load_model
import os
import logging
import uuid
import urllib.request
from transformers import Wav2Vec2Processor, Wav2Vec2Model

# Logger'ı önce tanımla (download_models_if_needed'den önce)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Model dosyalarını runtime'da indir (build size'ı küçültmek için)
def download_file_from_google_drive(url, destination):
    """Google Drive'dan dosya indir (büyük dosyalar için)"""
    try:
        import requests
    except ImportError:
        logger.error("❌ 'requests' package not installed. Install it with: pip install requests")
        return False
    
    try:
        # Google Drive direct download URL formatı
        if "drive.google.com" in url:
            # File ID'yi çıkar
            if "/file/d/" in url:
                file_id = url.split("/file/d/")[1].split("/")[0]
            elif "id=" in url:
                file_id = url.split("id=")[1].split("&")[0]
            else:
                file_id = url.split("/")[-1]
            
            # Direct download URL
            download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
            
            # Session ile cookie'leri yönet (büyük dosyalar için)
            session = requests.Session()
            response = session.get(download_url, stream=True)
            
            # Virus scan sayfası kontrolü
            if "virus scan" in response.text.lower() or "download anyway" in response.text.lower():
                # Confirm download link'ini bul
                confirm_url = download_url + "&confirm=t"
                response = session.get(confirm_url, stream=True)
            
            # Dosyayı indir
            total_size = int(response.headers.get('content-length', 0))
            with open(destination, 'wb') as f:
                if total_size == 0:
                    f.write(response.content)
                else:
                    chunk_size = 8192
                    downloaded = 0
                    for chunk in response.iter_content(chunk_size=chunk_size):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            if total_size > 0:
                                percent = (downloaded / total_size) * 100
                                if downloaded % (chunk_size * 100) == 0:  # Her 100 chunk'ta bir log
                                    logger.info(f"Downloaded {downloaded}/{total_size} bytes ({percent:.1f}%)")
            
            logger.info(f"✅ File downloaded successfully: {destination}")
            return True
        else:
            # Normal HTTP download
            response = requests.get(url, stream=True)
            response.raise_for_status()
            total_size = int(response.headers.get('content-length', 0))
            with open(destination, 'wb') as f:
                if total_size == 0:
                    f.write(response.content)
                else:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
            logger.info(f"✅ File downloaded successfully: {destination}")
            return True
    except Exception as e:
        logger.error(f"❌ Failed to download from {url}: {e}")
        return False

def download_models_if_needed():
    """Model dosyalarını runtime'da indir (eğer yoksa)"""
    model_path = os.environ.get("W2V_CLASSIFIER_PATH", "/app/backend/models/wav2vec2_model.h5")
    label_path = os.environ.get("W2V_LABELS_PATH", "/app/backend/models/classes.npy")
    
    model_url = os.environ.get("MODEL_DOWNLOAD_URL", "")
    label_url = os.environ.get("LABEL_DOWNLOAD_URL", "")
    
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    
    # Model dosyasını indir
    if model_url and not os.path.exists(model_path):
        logger.info(f"📥 Downloading model from {model_url}...")
        success = download_file_from_google_drive(model_url, model_path)
        if not success:
            logger.warning(f"⚠️ Model download failed, but continuing startup...")
    elif not os.path.exists(model_path):
        logger.warning(f"⚠️ Model file not found at {model_path} and no download URL provided")
    else:
        logger.info(f"✅ Model file already exists at {model_path}")
    
    # Label dosyasını indir
    if label_url and not os.path.exists(label_path):
        logger.info(f"📥 Downloading labels from {label_url}...")
        success = download_file_from_google_drive(label_url, label_path)
        if not success:
            logger.warning(f"⚠️ Label download failed, but continuing startup...")
    elif not os.path.exists(label_path):
        logger.warning(f"⚠️ Label file not found at {label_path} and no download URL provided")
    else:
        logger.info(f"✅ Label file already exists at {label_path}")

# Mirror behavior of apibackend_w2v/main_w2v.py but inside this backend

app = FastAPI(
    title="🎤 Wav2Vec2 Emotion Recognition API",
    description="Ses tabanlı duygu tanıma API'si - Wav2Vec2 modeli ile eğitilmiş",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS = {}
LABEL_ENCODER = None
WAV2VEC_PROCESSOR = None
WAV2VEC_MODEL = None

EN_TO_TR = {
    "neutral": "Nötr",
    "calm": "Sakin",
    "happy": "Mutlu",
    "sad": "Üzgün",
    "angry": "Kızgın",
    "fearful": "Endişeli",
    "disgust": "Hoşnutsuz",
    "surprised": "Şaşkın",
}

def load_wav2vec_models():
    global WAV2VEC_PROCESSOR, WAV2VEC_MODEL
    try:
        WAV2VEC_PROCESSOR = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base")
        # Safetensors kullanarak yükle (torch.load hatasından kaçınmak için)
        WAV2VEC_MODEL = Wav2Vec2Model.from_pretrained("facebook/wav2vec2-base", use_safetensors=True)
        WAV2VEC_MODEL.eval()
        logger.info("✅ Wav2Vec2 models loaded successfully")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to load Wav2Vec2 models: {e}")
        # Alternatif: Eğer safetensors çalışmazsa, normal yükleme dene
        try:
            logger.info("🔄 Trying alternative loading method...")
            WAV2VEC_MODEL = Wav2Vec2Model.from_pretrained("facebook/wav2vec2-base", local_files_only=False)
            WAV2VEC_MODEL.eval()
            logger.info("✅ Wav2Vec2 models loaded successfully (alternative method)")
            return True
        except Exception as e2:
            logger.error(f"❌ Alternative loading also failed: {e2}")
            WAV2VEC_PROCESSOR = None
            WAV2VEC_MODEL = None
            return False

def load_classifier_model():
    global MODELS
    # Railway'da /app/backend/models/ kullanılır, local'de backend/models/ kullanılır
    default_path = os.path.join(BASE_DIR, "../models/wav2vec2_model.h5")
    if not os.path.exists(default_path):
        default_path = "/app/backend/models/wav2vec2_model.h5"
    model_path = os.environ.get("W2V_CLASSIFIER_PATH", default_path)
    if not os.path.exists(model_path):
        logger.error(f"❌ Model file not found: {model_path}")
        return False
    try:
        model = load_model(model_path, compile=False)
        MODELS["Wav2Vec2"] = model
        logger.info("✅ Wav2Vec2 classifier loaded successfully")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to load classifier: {e}")
        return False

def load_label_encoder():
    global LABEL_ENCODER
    # Railway'da /app/backend/models/ kullanılır, local'de backend/models/ kullanılır
    default_path = os.path.join(BASE_DIR, "../models/classes.npy")
    if not os.path.exists(default_path):
        default_path = "/app/backend/models/classes.npy"
    encoder_path = os.environ.get("W2V_LABELS_PATH", default_path)
    if os.path.exists(encoder_path):
        try:
            LABEL_ENCODER = np.load(encoder_path)
            logger.info(f"✅ Label encoder loaded: {LABEL_ENCODER}")
            return True
        except Exception as e:
            logger.warning(f"⚠️ Could not load label encoder: {e}")
    else:
        logger.info("ℹ️ No label encoder found, using default classes")
    return False

@app.on_event("startup")
async def startup_event():
    """Startup event handler - modelleri yükle"""
    try:
        logger.info("🚀 Starting Wav2Vec2 Emotion Recognition API")
        
        # Önce model dosyalarını indir (eğer yoksa)
        try:
            download_models_if_needed()
        except Exception as e:
            logger.warning(f"⚠️ Model download failed (continuing anyway): {e}")
            import traceback
            logger.debug(traceback.format_exc())
        
        # Sonra modelleri yükle (her biri ayrı try-except ile)
        try:
            wav2vec_loaded = load_wav2vec_models()
            if not wav2vec_loaded:
                logger.warning("⚠️ Wav2Vec2 models could not be loaded. Feature extraction will fail.")
        except Exception as e:
            logger.error(f"❌ Error loading Wav2Vec2 models: {e}")
            import traceback
            logger.debug(traceback.format_exc())
        
        try:
            classifier_loaded = load_classifier_model()
            if not classifier_loaded:
                logger.warning("⚠️ Classifier model could not be loaded. Predictions will fail.")
        except Exception as e:
            logger.error(f"❌ Error loading classifier: {e}")
            import traceback
            logger.debug(traceback.format_exc())
        
        try:
            label_loaded = load_label_encoder()
            if not label_loaded:
                logger.warning("⚠️ Label encoder could not be loaded. Using default classes.")
        except Exception as e:
            logger.error(f"❌ Error loading label encoder: {e}")
            import traceback
            logger.debug(traceback.format_exc())
        
        logger.info("✅ API startup completed (some models may not be loaded)")
    except Exception as e:
        logger.error(f"❌ Critical error during startup: {e}")
        import traceback
        logger.error(traceback.format_exc())
        # API yine de başlamaya devam etsin

def convert_to_wav(input_path: str) -> str:
    try:
        output_path = input_path + "_conv.wav"
        sound = AudioSegment.from_file(input_path)
        sound = sound.set_frame_rate(16000).set_channels(1)
        sound.export(output_path, format="wav")
        return output_path
    except Exception as e:
        logger.error(f"❌ Conversion to wav failed: {e}")
        return None

def extract_wav2vec_features(file_path: str) -> np.ndarray:
    try:
        # Model ve processor kontrolü
        if WAV2VEC_PROCESSOR is None or WAV2VEC_MODEL is None:
            logger.error("❌ Wav2Vec2 models not loaded. Cannot extract features.")
            return None
        
        waveform, sample_rate = torchaudio.load(file_path)
        waveform = waveform.mean(dim=0)
        if sample_rate != 16000:
            resampler = torchaudio.transforms.Resample(sample_rate, 16000)
            waveform = resampler(waveform)
        inputs = WAV2VEC_PROCESSOR(waveform, sampling_rate=16000, return_tensors="pt", padding=True)
        with torch.no_grad():
            outputs = WAV2VEC_MODEL(inputs.input_values)
            hidden_states = outputs.last_hidden_state.mean(dim=1).cpu().numpy()
        return hidden_states.squeeze()
    except Exception as e:
        logger.error(f"❌ Wav2Vec2 feature extraction failed: {e}")
        return None

def preprocess_for_wav2vec(features: np.ndarray) -> np.ndarray:
    if features is None or len(features.shape) == 0:
        return None
    if len(features.shape) == 1:
        features = features.reshape(1, -1)
    return features

@app.get("/")
async def root():
    """Health check endpoint"""
    models_status = {
        "wav2vec_loaded": WAV2VEC_MODEL is not None and WAV2VEC_PROCESSOR is not None,
        "classifier_loaded": "Wav2Vec2" in MODELS,
        "label_encoder_loaded": LABEL_ENCODER is not None
    }
    return {
        "message": "🎤 Wav2Vec2 Emotion Recognition API",
        "status": "healthy" if all(models_status.values()) else "degraded",
        "models": models_status,
        "models_loaded": list(MODELS.keys()),
    }

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if not file or not file.filename:
        return {"error": "Dosya yüklenmedi"}

    temp_path = os.path.join(BASE_DIR, f"temp_{uuid.uuid4().hex}_{file.filename}")
    try:
        with open(temp_path, "wb") as f:
            f.write(await file.read())
    except Exception as e:
        return {"error": f"Dosya kaydedilemedi: {str(e)}"}

    try:
        wav_path = convert_to_wav(temp_path)
        if not wav_path:
            return {"error": "Ses dönüştürülemedi"}

        features = extract_wav2vec_features(wav_path)
        if features is None:
            return {"error": "Özellik çıkarılamadı"}

        x = preprocess_for_wav2vec(features)
        if x is None:
            return {"error": "Özellik işlenemedi"}

        model = MODELS.get("Wav2Vec2")
        if model is None:
            return {"error": "Model yüklenmedi"}

        prediction = model.predict(x, verbose=0)
        pred_idx = int(np.argmax(prediction))
        confidence = float(np.max(prediction))

        if LABEL_ENCODER is not None and pred_idx < len(LABEL_ENCODER):
            predicted_emotion = LABEL_ENCODER[pred_idx]
        else:
            return {"error": "Label encoder not loaded properly"}

        prediction_tr = EN_TO_TR.get(predicted_emotion, predicted_emotion)
        return {"prediction": predicted_emotion, "prediction_tr": prediction_tr, "confidence": confidence}
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return {"error": "Tahmin sırasında hata oluştu"}
    finally:
        for path in [temp_path, temp_path + "_conv.wav"]:
            if os.path.exists(path):
                try:
                    os.remove(path)
                except Exception:
                    pass

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run("wav2vec_emotion_api:app", host="0.0.0.0", port=port, reload=True, log_level="info")




