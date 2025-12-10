# 🔧 RAILWAY "Application failed to respond" HATASI ÇÖZÜMÜ

"Application failed to respond" hatası genellikle API'nin başlamadığını gösterir. Yapılan düzeltmeler:

---

## ✅ YAPILAN DÜZELTMELER

### 1. Logger Sırası Düzeltildi
- `wav2vec_emotion_api.py`'de logger tanımlanmadan kullanılıyordu
- Logger artık fonksiyonlardan **önce** tanımlanıyor

### 2. Startup Event Handler Eklendi
- Model indirme işlemi artık startup event handler içinde
- Hata olsa bile API başlamaya devam ediyor

### 3. Port Ayarları Düzeltildi
- Railway'ın `$PORT` environment variable'ı kullanılıyor
- Her iki API'de de `host="0.0.0.0"` ve `port=$PORT` ayarlandı

### 4. Model Path'leri Düzeltildi
- Windows path'leri kaldırıldı
- Railway'a uygun default path'ler eklendi (`/app/backend/models/`)

### 5. Gereksiz Kod Kaldırıldı
- `main.py`'den `download_models_if_needed()` çağrısı kaldırıldı (speaker-api için gerekli değil)

---

## 🚀 RAILWAY'DA KONTROL EDİLECEKLER

### 1. Environment Variables

**speaker-api** service'inde:
```
PORT = ${{PORT}}  (otomatik)
CORS_ORIGINS = https://your-frontend.railway.app
```

**emotion-api** service'inde:
```
PORT = ${{PORT}}  (otomatik)
W2V_CLASSIFIER_PATH = /app/backend/models/wav2vec2_model.h5
W2V_LABELS_PATH = /app/backend/models/classes.npy
MODEL_DOWNLOAD_URL = https://drive.google.com/uc?export=download&id=YOUR_FILE_ID
LABEL_DOWNLOAD_URL = https://drive.google.com/uc?export=download&id=YOUR_FILE_ID
```

### 2. Start Command

**speaker-api:**
```bash
python -m uvicorn main:app --host 0.0.0.0 --port $PORT
```

**emotion-api:**
```bash
python -m uvicorn wav2vec_emotion_api:app --host 0.0.0.0 --port $PORT
```

### 3. Build Command

Her iki service için:
```bash
pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
```

---

## 🔍 HATA AYIKLAMA

### 1. Deploy Loglarını Kontrol Edin

Railway'da **Deployments** > **Latest Deployment** > **View Logs**:

- ✅ "🚀 Starting Wav2Vec2 Emotion Recognition API" görünüyor mu?
- ✅ "✅ Wav2Vec2 models loaded successfully" görünüyor mu?
- ✅ "✅ API ready for predictions" görünüyor mu?
- ❌ Hata mesajları var mı?

### 2. Health Check Endpoint'ini Test Edin

API URL'lerini tarayıcıda açın:
- `https://your-speaker-api.railway.app/`
- `https://your-emotion-api.railway.app/`

Şu şekilde bir response görmelisiniz:
```json
{
  "message": "🎤 Wav2Vec2 Emotion Recognition API",
  "status": "healthy",
  "models": {
    "wav2vec_loaded": true,
    "classifier_loaded": true,
    "label_encoder_loaded": true
  }
}
```

### 3. Model Dosyaları Kontrolü

Eğer `status: "degraded"` görüyorsanız:
- Model dosyaları indirilememiş olabilir
- `MODEL_DOWNLOAD_URL` ve `LABEL_DOWNLOAD_URL` doğru mu?
- Google Drive link'leri "Anyone with the link" olarak paylaşılmış mı?

---

## 📋 ADIM ADIM KONTROL LİSTESİ

1. ✅ GitHub'a push yapıldı mı?
2. ✅ Railway'da service'ler otomatik deploy oldu mu?
3. ✅ Deploy loglarında hata var mı?
4. ✅ Health check endpoint'leri çalışıyor mu?
5. ✅ Environment variables doğru mu?
6. ✅ Model dosyaları indirildi mi?

---

## 🆘 HALA ÇALIŞMIYORSA

1. **Service'i silip yeniden oluşturun** (build cache temizlenmesi için)
2. **Deploy loglarını paylaşın** (hata mesajlarını görmek için)
3. **Health check response'unu paylaşın** (model durumunu görmek için)

**Başarılar! 🚀**

