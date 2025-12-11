# Frontend için Dockerfile
# Railway'da Root Directory: frontend olmalı
FROM node:20-alpine AS builder

WORKDIR /app

# Package dosyalarını kopyala
COPY package*.json ./

# Bağımlılıkları yükle
RUN npm ci

# Kaynak kodları kopyala
COPY . .

# Build yap (environment variables build time'da kullanılır)
ARG VITE_SPEAKER_API_URL
ARG VITE_EMOTION_API_URL
ENV VITE_SPEAKER_API_URL=$VITE_SPEAKER_API_URL
ENV VITE_EMOTION_API_URL=$VITE_EMOTION_API_URL

RUN npm run build

# Production image
FROM nginx:alpine

# Build edilmiş dosyaları kopyala
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

