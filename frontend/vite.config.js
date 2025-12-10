import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  define: {
    // Environment variables için
    'import.meta.env.VITE_SPEAKER_API_URL': JSON.stringify(process.env.VITE_SPEAKER_API_URL || 'http://localhost:8000'),
    'import.meta.env.VITE_EMOTION_API_URL': JSON.stringify(process.env.VITE_EMOTION_API_URL || 'http://localhost:8001'),
  },
})
