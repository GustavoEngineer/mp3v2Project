import { useState } from 'react';
import { API_URL } from '../config';

const useDownload = () => {
    const [status, setStatus] = useState('');
    const [loading, setLoading] = useState(false);

    const downloadMedia = async (url, type) => {
        if (!url) {
            setStatus('Por favor ingresa una URL de YouTube');
            return;
        }

        setLoading(true);
        setStatus('Iniciando descarga...');

        const endpoint = type === 'mp3' ? '/descargar-mp3' : '/descargar-video';

        try {
            const response = await fetch(`${API_URL}${endpoint}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url }),
            });

            if (response.ok) {
                setStatus('Procesando archivo...');
                const blob = await response.blob();

                // Crear URL temporal para el blob
                const downloadUrl = window.URL.createObjectURL(blob);
                const link = document.createElement('a');
                link.href = downloadUrl;

                // Intentar obtener nombre del archivo del header
                const contentDisposition = response.headers.get('Content-Disposition');
                let fileName = type === 'mp3' ? `audio_${Date.now()}.mp3` : `video_${Date.now()}.mp4`; // Fallback

                if (contentDisposition) {
                    // Buscar filename="nombre.ext" o filename*=UTF-8''nombre.ext
                    const fileNameMatch = contentDisposition.match(/filename\*?=([^;]+)/);
                    if (fileNameMatch && fileNameMatch[1]) {
                        // Limpiar comillas y encoding si existe
                        fileName = fileNameMatch[1].replace(/['"]/g, '').replace('UTF-8\'\'', '');
                        fileName = decodeURIComponent(fileName);
                    }
                }

                link.setAttribute('download', fileName);
                document.body.appendChild(link);
                link.click();
                link.parentNode.removeChild(link);
                window.URL.revokeObjectURL(downloadUrl);

                setStatus('¡Descarga iniciada!');
            } else {
                const data = await response.json();
                setStatus(`Error: ${data.mensaje || 'Error desconocido'}`);
            }
        } catch (error) {
            console.error('Error:', error);
            setStatus('Error de conexión o descarga fallida');
        } finally {
            setLoading(false);
        }
    };

    return {
        status,
        loading,
        downloadMedia,
    };
};

export default useDownload;
