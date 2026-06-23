import path from "path" // Importă modulul path din Node
import react from "@vitejs/plugin-react"
import { defineConfig } from 'vite'
import fs from 'fs'

export default defineConfig({
    plugins: [react()],
    resolve: {
        alias: {
            "@": path.resolve(__dirname, "./src"), // Aici mapăm @ către folderul src
        },
    },
    server: {
        host: true,
        port: 5173,
        https: {
            key: fs.readFileSync('./certs/localhost-key.pem'),
            cert: fs.readFileSync('./certs/localhost-cert.pem'),
        },
    },
})