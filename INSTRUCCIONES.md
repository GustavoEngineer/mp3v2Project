# Guía de Instalación y Ejecución

Sigue estos pasos para ejecutar el proyecto completo (Backend y Frontend) en tu máquina local.

## 1. Prerrequisitos
Asegúrate de tener instalado:
*   **Python 3.10+**: [Descargar aquí](https://www.python.org/downloads/)
*   **Node.js 18+**: [Descargar aquí](https://nodejs.org/es/)
*   **FFmpeg**: Necesario para la conversión de audio. [Descargar aquí](https://ffmpeg.org/download.html)
    *   *Nota: Asegúrate de agregar FFmpeg a las variables de entorno (PATH) de tu sistema.*

---

## 2. Configurar y Ejecutar el Backend (API)

El backend se encarga de procesar las descargas.

1.  Abre una terminal y navega a la carpeta `Backend`:
    ```bash
    cd Backend
    ```

2.  (Opcional) Crea y activa un entorno virtual:
    ```bash
    python -m venv venv
    # En Windows:
    .\venv\Scripts\activate
    # En Mac/Linux:
    source venv/bin/activate
    ```

3.  Instala las dependencias de Python:
    ```bash
    pip install -r requirements.txt
    ```

4.  Ejecuta el servidor:
    ```bash
    python api.py
    ```
    *Deberías ver un mensaje indicando que el servidor corre en `http://127.0.0.1:8080` o similar.*

---

## 3. Configurar y Ejecutar el Frontend (Interfaz)

El frontend es la página web donde pegarás los links.

1.  Abre **otra nueva terminal** (no cierres la del backend) y navega a la carpeta `Frontend`:
    ```bash
    cd Frontend
    ```

2.  Instala las dependencias de Node.js:
    ```bash
    npm install
    ```

3.  Configura las variables de entorno:
    *   Crea un archivo llamado `.env` en la carpeta `Frontend` (puedes copiar el ejemplo).
    *   Asegúrate de que tenga la URL de tu backend local:
    ```env
    VITE_API_URL=http://localhost:8080
    ```

4.  Ejecuta el servidor de desarrollo:
    ```bash
    npm run dev
    ```

---

## 4. Usar la Aplicación

1.  Mira la terminal del Frontend, te mostrará una URL local, generalmente:
    👉 **http://localhost:5173**
2.  Abre esa dirección en tu navegador.
3.  Pega un link de YouTube y prueba descargar Video o MP3.
