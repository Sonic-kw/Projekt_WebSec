import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    allowedHosts: ['rybmw.space', 'k8s-default-appingre-6d548e4681-582162090.eu-north-1.elb.amazonaws.com'] // <-- ADD THIS LINE
  }
})
