import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  server: {
    port: 3000, // Default port Vite will use
  },
  plugins: [react()],
});
