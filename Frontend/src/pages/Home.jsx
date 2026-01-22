import React, { useState } from 'react';
import Header from '../components/layout/Header';
import Button from '../components/common/Button';
import Input from '../components/common/Input';
import useDownload from '../hooks/useDownload';
import { API_URL } from '../config';

const Home = () => {
    const [url, setUrl] = useState('');
    const { status, loading, downloadMedia } = useDownload();

    return (
        <div className="container">
            <Header />
            <div className="card">
                <Input
                    placeholder="Pega la URL de YouTube aquí..."
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                />
                <div className="button-group">
                    <Button onClick={() => downloadMedia(url, 'mp3')} disabled={loading}>
                        {loading ? 'Procesando...' : 'Descargar MP3'}
                    </Button>
                </div>
                {status && <p className="status-message">{status}</p>}
            </div>
            <p className="footer">
                Backend URL: {API_URL}
            </p>
        </div>
    );
};

export default Home;
