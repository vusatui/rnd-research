import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { viteSingleFile } from "vite-plugin-singlefile";

// npm run build -> dist/ (base "./": works from any static host and any sub-path)
//                + dist/standalone/index.html (one self-contained file, fonts inlined; opens from file:// with a double-click)
export default defineConfig(({ mode }) =>
  mode === "single"
    ? {
        base: "./",
        plugins: [react(), viteSingleFile()],
        build: { outDir: "dist/standalone", emptyOutDir: true, chunkSizeWarningLimit: 4000 },
      }
    : {
        base: "./",
        plugins: [react()],
        build: { outDir: "dist", assetsInlineLimit: 0, chunkSizeWarningLimit: 2000 },
        server: { port: 5173, host: true },
      },
);
