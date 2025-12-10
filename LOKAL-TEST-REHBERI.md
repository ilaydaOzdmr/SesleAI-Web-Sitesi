# 🧪 LOKAL TEST REHBERİ

Bu rehber, projenizi canlıya almadan önce her şeyin çalıştığından emin olmanız için hazırlanmıştır.

---

## ✅ ADIM 1: BACKEND API'LERİNİ TEST ETME

### 1.1 İlk Terminal Penceresi - Speaker API (Port 8000)

**PowerShell'i açın ve şu komutları çalıştırın:**

```powershell
# Proje klasörüne git
cd "C:\Users\MONSTER\Desktop\sesleAI Proje Web Sitesi\backend\api"

# Conda environment'ı aktif et
conda activate voice_env

# Environment variable'ları ayarla
$env:W2V_CLASSIFIER_PATH="C:\Users\MONSTER\Desktop\sesleAI Proje Web Sitesi\backend\models\wav2vec2_model.h5"
$env:W2V_LABELS_PATH="C:\Users\MONSTER\Desktop\sesleAI Proje Web Sitesi\backend\models\classes.npy"

# Speaker API'yi başlat
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Beklenen Çıktı:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [...]
INFO:     Started server process [...]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**✅ Başarılı ise:** Bu terminali açık bırakın, başka bir terminal açın.

---

### 1.2 İkinci Terminal Penceresi - Emotion API (Port 8001)

**YENİ bir PowerShell penceresi açın ve şu komutları çalıştırın:**

```powershell
# Proje klasörüne git
cd "C:\Users\MONSTER\Desktop\sesleAI Proje Web Sitesi\backend\api"

# Conda environment'ı aktif et
conda activate voice_env

# Environment variable'ları ayarla
$env:W2V_CLASSIFIER_PATH="C:\Users\MONSTER\Desktop\sesleAI Proje Web Sitesi\backend\models\wav2vec2_model.h5"
$env:W2V_LABELS_PATH="C:\Users\MONSTER\Desktop\sesleAI Proje Web Sitesi\backend\models\classes.npy"

# Emotion API'yi başlat
uvicorn wav2vec_emotion_api:app --reload --host 0.0.0.0 --port 8001
```

**Beklenen Çıktı:**
```
INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
INFO:     Started reloader process [...]
INFO:     Started server process [...]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**✅ Başarılı ise:** Bu terminali de açık bırakın.

---

### 1.3 API'leri Test Etme

**ÜÇÜNCÜ bir PowerShell penceresi açın ve test edin:**

```powershell
# Speaker API'yi test et
curl http://localhost:8000/

# Beklenen çıktı:
# {"message":"Ses Kimlik Tespiti API'si çalışıyor."}

# Emotion API'yi test et
curl http://localhost:8001/

# Beklenen çıktı:
# {"message":"🎤 Wav2Vec2 Emotion Recognition API","status":"running",...}
```

**VEYA tarayıcıda açın:**
- Speaker API: http://localhost:8000
- Emotion API: http://localhost:8001

Her ikisinde de JSON mesajı görmelisiniz.

**✅ Her iki API de çalışıyorsa:** ADIM 2'ye geçin.

---

## ✅ ADIM 2: FRONTEND'İ TEST ETME

### 2.1 Frontend Klasörüne Git

**DÖRDÜNCÜ bir PowerShell penceresi açın:**

```powershell
# Frontend klasörüne git
cd "C:\Users\MONSTER\Desktop\sesleAI Proje Web Sitesi\frontend"
```

### 2.2 Bağımlılıkları Kontrol Et

```powershell
# node_modules klasörü var mı kontrol et
Test-Path node_modules

# Yoksa yükle
npm install
```

### 2.3 Frontend'i Başlat

```powershell
# Development modunda başlat
npm run dev
```

**Beklenen Çıktı:**
```
  VITE v7.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

**✅ Başarılı ise:** Tarayıcıda http://localhost:5173 adresini açın.

---

### 2.4 Frontend'i Tarayıcıda Test Et

1. **Tarayıcıda açın:** http://localhost:5173

2. **Kontrol edin:**
   - ✅ Sayfa yükleniyor mu?
   - ✅ Hata mesajı var mı? (F12 > Console)
   - ✅ API bağlantıları çalışıyor mu?

3. **Test senaryoları:**
   - Ses kaydı yapmayı deneyin
   - API'ye istek atmayı deneyin
   - Hata mesajlarını kontrol edin

**✅ Frontend çalışıyorsa:** Tüm testler başarılı!

---

## 🐛 SORUN GİDERME

### API'ler Başlamıyor

**Hata:** `Port 8000 already in use`
```powershell
# Portu kullanan process'i bul
netstat -ano | findstr :8000

# Process'i durdur (PID'yi değiştirin)
taskkill /PID <PID_NUMARASI> /F
```

**Hata:** `Module not found`
```powershell
# Environment'ı tekrar aktif et
conda activate voice_env

# Eksik paketleri yükle
pip install fastapi uvicorn torch torchaudio transformers speechbrain tensorflow keras librosa soundfile pydub numpy scikit-learn scipy
```

### Frontend Başlamıyor

**Hata:** `Port 5173 already in use`
```powershell
# Farklı port kullan
npm run dev -- --port 3000
```

**Hata:** `Cannot find module`
```powershell
# node_modules'ı sil ve tekrar yükle
Remove-Item -Recurse -Force node_modules
npm install
```

### CORS Hatası

Frontend'den API'ye istek atarken CORS hatası alıyorsanız:

1. **Backend API'lerin çalıştığından emin olun**
2. **Tarayıcı console'unu kontrol edin (F12)**
3. **API URL'lerinin doğru olduğundan emin olun**

---

## ✅ TEST CHECKLIST

Her şeyin çalıştığından emin olmak için bu checklist'i kullanın:

### Backend API'ler
- [ ] Speaker API (port 8000) başlatıldı
- [ ] Emotion API (port 8001) başlatıldı
- [ ] http://localhost:8000 çalışıyor
- [ ] http://localhost:8001 çalışıyor
- [ ] Her iki API'de de JSON response alınıyor

### Frontend
- [ ] `npm install` başarılı
- [ ] `npm run dev` başarılı
- [ ] http://localhost:5173 açılıyor
- [ ] Sayfa hatasız yükleniyor
- [ ] Console'da hata yok (F12)

### Entegrasyon
- [ ] Frontend'den API'lere istek atılabiliyor
- [ ] CORS hatası yok
- [ ] Ses kaydı çalışıyor (varsa)
- [ ] API response'ları alınıyor

---

## 🎉 TAMAMLANDI!

Eğer yukarıdaki tüm adımlar başarılıysa, projeniz canlıya alma için hazır!

**Sonraki adım:** `ADIM-ADIM-REHBER.md` dosyasındaki "ADIM 2: SUNUCUYA BAĞLANMA" bölümüne geçin.

---

## 📝 NOTLAR

- **3-4 terminal penceresi** açık olacak (2 API + 1 Frontend + 1 Test)
- **Her terminali açık bırakın**, kapatmayın
- **Test bittikten sonra** tüm terminal'leri kapatabilirsiniz (Ctrl+C ile)

**Başarılar! 🚀**


