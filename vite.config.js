import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  base: "/build-a-hospital-appointment-system-it-needs-a-backend-api-with-a-postgres-datab-791a01/",
  build: { outDir: "dist", assetsDir: "assets" },
  server: { port: 3000 },
});
