
import tempfile
import shutil
import os
import re
import sys
import traceback
import yt_dlp
from flask import Flask, request, jsonify, send_from_directory, Response, stream_with_context, send_file, after_this_request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, expose_headers=["Content-Disposition"])

# DEBUG: Check for ffmpeg on startup
ffmpeg_path = shutil.which('ffmpeg')
if ffmpeg_path:
    print(f"Startup Check: FFmpeg found at: {ffmpeg_path}")
else:
    print("Startup Check: FFmpeg NOT FOUND on PATH! Downloads will likely fail.")

def limpiar_nombre(nombre):
    """Eliminar caracteres inválidos del nombre de archivo"""
    return re.sub(r'[\\/*?:\"<>|]', "", nombre)

# Configuration for stealth/browser simulation
SHARED_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
}

def descargar_video(url, carpeta="descargas"):
    os.makedirs(carpeta, exist_ok=True)
    
    opciones = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': f'{carpeta}/%(title)s.%(ext)s',
        'postprocessors': [],
        'nocheckcertificate': True,
        'noplaylist': True,
        'quiet': True,
        'http_headers': SHARED_HEADERS,
    }

    try:
        with yt_dlp.YoutubeDL(opciones) as ydl:
            info = ydl.extract_info(url, download=False)
            info['title'] = limpiar_nombre(info['title'])
            ydl.download([url])
        return {"estado": "exito", "mensaje": f"Video descargado en '{carpeta}'"}
    except Exception as e:
        return {"estado": "error", "mensaje": str(e)}

def descargar_mp3(url, carpeta="descargas"):
    os.makedirs(carpeta, exist_ok=True)
    
    opciones = {
        'format': 'bestaudio/best',
        'outtmpl': f'{carpeta}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],

        'nocheckcertificate': True,
        'noplaylist': True,
        'quiet': True,
        'http_headers': SHARED_HEADERS,
    }

    try:
        with yt_dlp.YoutubeDL(opciones) as ydl:
            info = ydl.extract_info(url, download=False)
            info['title'] = limpiar_nombre(info['title'])
            ydl.download([url])
        return {"estado": "exito", "mensaje": f"Audio MP3 descargado en '{carpeta}'"}
    except Exception as e:
        return {"estado": "error", "mensaje": str(e)}

# ... (rest of helper functions if needed, but I'll redefine the relevant endpoint below)

@app.route('/download', methods=['GET'])
def api_descargar_audio_get():
    """Endpoint para descargar MP3 directamente al navegador usando archivos temporales."""
    url = request.args.get('url')
    if not url:
        return jsonify({"message": "No se proporcionó URL."}), 400

    # Crear directorio temporal único para esta descarga
    temp_dir = tempfile.mkdtemp()

    try:
        opciones_ydl = {
            'format': 'bestaudio/best',
            'outtmpl': f'{temp_dir}/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'nocheckcertificate': True,
            'quiet': True,
            'noplaylist': True,
            'http_headers': SHARED_HEADERS,
        }

        # Check for FFmpeg to decide if we can convert
        if not shutil.which('ffmpeg'):
            print("FFmpeg not found. Skipping MP3 conversion.")
            # Remove postprocessors if no ffmpeg
            if 'postprocessors' in opciones_ydl:
                del opciones_ydl['postprocessors']

        with yt_dlp.YoutubeDL(opciones_ydl) as ydl:
            info = ydl.extract_info(url, download=True)
            titulo = limpiar_nombre(info['title'])
            # Determine extension
            ext = info.get('ext', 'mp3')
            if shutil.which('ffmpeg'):
                ext = 'mp3'
            
            archivo_path = os.path.join(temp_dir, f"{titulo}.{ext}")

        # Verificar si el archivo existe (a veces el título puede variar ligeramente)
        if not os.path.exists(archivo_path):
            # Intentar buscar cualquier archivo en el directorio temp
            archivos = [f for f in os.listdir(temp_dir) if os.path.isfile(os.path.join(temp_dir, f))]
            if archivos:
                archivo_path = os.path.join(temp_dir, archivos[0])
                titulo = os.path.splitext(archivos[0])[0]
                ext = os.path.splitext(archivos[0])[1].replace('.', '')
            else:
                raise Exception("No se pudo encontrar el archivo descargado.")

        @after_this_request
        def remove_temp_dir(response):
            try:
                shutil.rmtree(temp_dir)
            except Exception as e:
                app.logger.error(f"Error eliminando directorio temporal: {e}")
            return response

        return send_file(
            archivo_path, 
            as_attachment=True, 
            download_name=f"{titulo}.{ext}", 
            mimetype='audio/mpeg' if ext == 'mp3' else 'application/octet-stream'
        )

    except Exception as e:
        app.logger.error(f"Error serving download: {e}")
        app.logger.error(traceback.format_exc())
        # Limpiar si falla antes de enviar respuesta
        shutil.rmtree(temp_dir, ignore_errors=True)
        return jsonify({"message": str(e)}), 500



@app.route('/descargas/<path:filename>')
def servir_archivo_descargado(filename):
    """Sirve los archivos desde la carpeta de descargas."""
    directorio_descargas = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'descargas')
    return send_from_directory(directorio_descargas, filename, as_attachment=True)

@app.route('/descargar-video', methods=['POST'])
def api_descargar_video():
    return procesar_descarga_generica(request, 'video')

@app.route('/descargar-mp3', methods=['POST'])
def api_descargar_mp3():
    return procesar_descarga_generica(request, 'mp3')

def procesar_descarga_generica(req, tipo):
    data = req.get_json()
    url = data.get('url')
    if not url:
        return jsonify({"estado": "error", "mensaje": "No se proporcionó URL"}), 400

    temp_dir = tempfile.mkdtemp()

    try:
        opciones = {
            'outtmpl': f'{temp_dir}/%(title)s.%(ext)s',
            'nocheckcertificate': True,
            'noplaylist': True,
            'quiet': True,
            'http_headers': SHARED_HEADERS,
        }

        if tipo == 'mp3':
            opciones.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            })
        else:
            opciones.update({
                'format': 'bestvideo+bestaudio/best',
            })

        with yt_dlp.YoutubeDL(opciones) as ydl:
            info = ydl.extract_info(url, download=True)
            titulo = limpiar_nombre(info['title'])
            ext = 'mp3' if tipo == 'mp3' else info.get('ext', 'mp4')
            
            # Busqueda de archivo flexible
            archivo_path = os.path.join(temp_dir, f"{titulo}.{ext}")
            if not os.path.exists(archivo_path):
                 # Failover: buscar cualquier archivo
                 archivos = os.listdir(temp_dir)
                 if archivos:
                     archivo_path = os.path.join(temp_dir, archivos[0])
                     titulo = os.path.splitext(archivos[0])[0]

        @after_this_request
        def remove_temp_dir(response):
            try:
                shutil.rmtree(temp_dir)
            except Exception as e:
                app.logger.error(f"Error eliminando directorio temporal: {e}")
            return response

        return send_file(
            archivo_path, 
            as_attachment=True, 
            download_name=f"{titulo}.{ext}", 
            mimetype='audio/mpeg' if tipo == 'mp3' else 'video/mp4'
        )

    except Exception as e:
        app.logger.error(f"Error serving download: {e}")
        app.logger.error(traceback.format_exc())
        shutil.rmtree(temp_dir, ignore_errors=True)
        return jsonify({"estado": "error", "mensaje": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
