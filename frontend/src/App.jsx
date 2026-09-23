import { useState } from 'react'
import { processVideo } from './services/api'

function App() {
  const [video, setVideo] = useState(null)
  const [theme, setTheme] = useState('')
  const [choices, setChoices] = useState({
    grayscale: false,
    rotate: 0,
    rotationDuration: 1,
    speed: 1,
  })

  const [processing, setProcessing] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')

  const handleProcess = async () => {
    if (!video) {
      setError('Please select a video.')
      return
    }

    if (!theme) {
      setError('Please select a theme.')
      return
    }

    setError('')
    setProcessing(true)
    setResult(null)

    try {
      const data = await processVideo(video, theme, choices)
      setResult(data)
    } catch (error) {
      console.error(error)
      setError(error.message)
    } finally {
      setProcessing(false)
    }
  }

  return (
    <div>
      <h1>VisionCraftStudio</h1>

      <h2>Upload Video</h2>

      <input
        type="file"
        accept="video/*"
        onChange={(event) => {
          setVideo(event.target.files[0])
          setResult(null)
          setError('')
        }}
      />

      {video && (
        <p>
          Selected video: {video.name}
        </p>
      )}

      <h2>Choose Theme</h2>

      <button onClick={() => setTheme('vintage')}>
        Vintage
      </button>

      {theme === 'vintage' && (
        <div>
          <h2>Vintage Settings</h2>

          <div>
            <label>
              <input
                type="checkbox"
                checked={choices.grayscale}
                onChange={(event) =>
                  setChoices({
                    ...choices,
                    grayscale: event.target.checked,
                  })
                }
              />
              Make video black and white
            </label>
          </div>

          <div>
            <label>
              Rotation duration (seconds):
              <input
                type="number"
                min="0"
                step="0.1"
                value={choices.rotationDuration}
                onChange={(event) =>
                  setChoices({
                    ...choices,
                    rotationDuration: Number(event.target.value),
                  })
                }
              />
            </label>
          </div>

          <div>
            <label>
              Rotation degrees:
              <input
                type="number"
                value={choices.rotate}
                onChange={(event) =>
                  setChoices({
                    ...choices,
                    rotate: Number(event.target.value),
                  })
                }
              />
            </label>
          </div>

          <div>
            <label>
              Speed multiplier:
              <input
                type="number"
                min="0.1"
                step="0.1"
                value={choices.speed}
                onChange={(event) =>
                  setChoices({
                    ...choices,
                    speed: Number(event.target.value),
                  })
                }
              />
            </label>
          </div>

          <button
            onClick={handleProcess}
            disabled={processing}
          >
            {processing ? 'Processing...' : 'Process Video'}
          </button>
        </div>
      )}

      {error && (
        <p>{error}</p>
      )}

      {result && (
        <div>
          <h2>Processed Video</h2>

          <video
            controls
            width="600"
            src={`http://127.0.0.1:8000${result.video_url}`}
          />

          <p>
            Video processed successfully!
          </p>
        </div>
      )}
    </div>
  )
}

export default App