import { useState } from 'react'
import './App.css'

function App() {
  const [url, setUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleDownload = async () => {
    if (!url) return

    setLoading(true)
    setError(null)

    try {
      // Trigger download directly via browser
      // Using the backend running on port 8080 as per existing setup
      window.location.href = `http://localhost:8080/download?url=${encodeURIComponent(url)}`

      // Reset loading after a delay since we can't easily track download progress this way
      setTimeout(() => setLoading(false), 3000)
    } catch (err) {
      setError('Something went wrong. Please check the URL.')
      setLoading(false)
    }
  }

  return (
    <div className="app-container">
      <div className="glass-card">
        <h1 className="title">MP3 Downloader</h1>
        <p className="subtitle">Download high-quality audio from YouTube instantly</p>

        <div className="input-group">
          <input
            type="text"
            placeholder="Paste YouTube URL here..."
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            className="url-input"
          />
        </div>

        {error && <div className="error-message">{error}</div>}

        <button
          onClick={handleDownload}
          disabled={loading || !url}
          className={`download-btn ${loading ? 'loading' : ''}`}
        >
          {loading ? 'Processing...' : 'Download MP3'}
        </button>

        <p className="footer-text">
          Powered by yt-dlp
        </p>
      </div>
    </div>
  )
}

export default App
