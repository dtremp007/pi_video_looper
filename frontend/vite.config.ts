import { defineConfig } from 'vite'
import solid from 'vite-plugin-solid'

export default defineConfig({
  plugins: [solid()],
  build: {
    outDir: '../Adafruit_Video_Looper/static',
    emptyOutDir: true,
    assetsDir: '.',
  },
  resolve: {
    alias: {
      "~": `${import.meta.dir}/src`,
    }
  }
})
