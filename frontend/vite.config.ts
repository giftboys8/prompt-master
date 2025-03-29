import { fileURLToPath, URL } from "node:url";
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue({
      script: {
        sourceMap: true,
      },
    }),
  ],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
  server: {
    port: 5173,
    proxy: {
      "/api/v1": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
    },
  },
  build: {
    sourcemap: true,
    minify: "terser",
    terserOptions: {
      sourceMap: true,
    },
    rollupOptions: {
      output: {
        sourcemap: true,
        manualChunks: {
          "vue-vendor": ["vue", "vue-router", "pinia"],
          "element-plus": ["element-plus"],
        },
      },
    },
  },
  css: {
    devSourcemap: true,
    preprocessorOptions: {
      scss: {
        sassOptions: {
          outputStyle: "expanded",
          sourceMap: true,
        },
      },
    },
  },
  optimizeDeps: {
    include: ["vue", "vue-router", "pinia", "element-plus"],
    exclude: [],
    entries: ["./src/**/*.vue"],
    esbuildOptions: {
      sourcemap: true,
    },
  },
});
