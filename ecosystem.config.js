// PM2 Process Manager Configuration
// Kullanım: pm2 start ecosystem.config.js

module.exports = {
  apps: [
    {
      name: 'speaker-api',
      script: 'uvicorn',
      args: 'main:app --host 0.0.0.0 --port 8000',
      cwd: './backend/api',
      interpreter: 'python',
      env: {
        PYTHONPATH: './backend/api',
        W2V_CLASSIFIER_PATH: './backend/models/wav2vec2_model.h5',
        W2V_LABELS_PATH: './backend/models/classes.npy',
        CORS_ORIGINS: process.env.CORS_ORIGINS || 'http://localhost:5173,http://127.0.0.1:5173'
      },
      error_file: './logs/speaker-api-error.log',
      out_file: './logs/speaker-api-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
      merge_logs: true,
      autorestart: true,
      max_memory_restart: '2G',
      instances: 1,
      exec_mode: 'fork'
    },
    {
      name: 'emotion-api',
      script: 'uvicorn',
      args: 'wav2vec_emotion_api:app --host 0.0.0.0 --port 8001',
      cwd: './backend/api',
      interpreter: 'python',
      env: {
        PYTHONPATH: './backend/api',
        W2V_CLASSIFIER_PATH: './backend/models/wav2vec2_model.h5',
        W2V_LABELS_PATH: './backend/models/classes.npy'
      },
      error_file: './logs/emotion-api-error.log',
      out_file: './logs/emotion-api-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
      merge_logs: true,
      autorestart: true,
      max_memory_restart: '2G',
      instances: 1,
      exec_mode: 'fork'
    }
  ]
};


