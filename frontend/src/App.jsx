import { useState } from 'react'
import { processVideo } from './services/api'

import VideoUpload from './components/VideoUpload'
import ThemeSelector from './components/ThemeSelector'
import VintageSteps from './components/VintageSteps'
import ProcessedVideo from './components/ProcessedVideo'

function App() {
  const [video, setVideo] = useState(null)
  const [theme, setTheme] = useState('')

  const [choices, setChoices] = useState({
    grayscale: null,
  rotationStart: 2,
  rotationDuration: 1,
  rotate: 0,
  speed: 1,
  speedStart: 3,
  speedEnd: 6,
  watermark: false,
  watermarkPosition: 'top-right',
  })

  const [processing, setProcessing] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [watermark, setWatermark] = useState(null)

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
      const data = await processVideo(
        video,
        theme,
        choices,
        watermark
      )
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

      <VideoUpload
        video={video}
        setVideo={setVideo}
      />

      <ThemeSelector
        theme={theme}
        setTheme={setTheme}
      />

      {theme === 'vintage' && (
        <VintageSteps
          choices={choices}
          setChoices={setChoices}
          onProcess={handleProcess}
          processing={processing}
          watermark={watermark}
          setWatermark={setWatermark}
        />
      )}

      {error && (
        <p>{error}</p>
      )}

      <ProcessedVideo result={result} />
    </div>
  )
}

export default App