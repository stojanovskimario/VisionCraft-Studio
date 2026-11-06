import { useState } from 'react'
import { processVideo, processEffect } from './services/api'

import VideoUpload from './components/VideoUpload'
import ThemeSelector from './components/ThemeSelector'
import EffectLibrary from './components/EffectLibrary'
import VintageSteps from './components/VintageSteps'
import ProcessedVideo from './components/ProcessedVideo'
import FuturisticSteps from './components/FuturisticSteps'
import RetroSteps from './components/RetroSteps.jsx'
import CinematicSteps from './components/CinematicSteps.jsx'
import NoirSteps from './components/NoirSteps.jsx'
import VHSSteps from './components/VHSSteps.jsx'
import DreamySteps from './components/DreamySteps'
import ActionSteps from './components/ActionSteps.jsx'
import CyberpunkSteps from './components/CyberpunkSteps.jsx'
import TravelSteps from './components/TravelSteps.jsx'
import SilentFilmSteps from './components/SilentFilmSteps.jsx'
import UnderwaterSteps from './components/UnderwaterSteps.jsx'

function App() {
    const [video, setVideo] = useState(null)
    const [theme, setTheme] = useState('')

    // New effect library state
    const [selectedEffectId, setSelectedEffectId] = useState('')

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

        // Futuristic
        colorEffect: false,
        glitch: false,
        glitchStart: 3,
        glitchDuration: 2,
        glitchIntensity: 5,

        // Retro
        filmGrain: false,
        filmGrainIntensity: 5,
        vignette: false,
        vignetteIntensity: 5,
    })

    const [processing, setProcessing] = useState(false)
    const [result, setResult] = useState(null)
    const [error, setError] = useState('')
    const [watermark, setWatermark] = useState(null)

    // Existing theme processing
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

    // New individual effect processing
    const handleProcessEffect = async () => {
        if (!video) {
            setError('Please select a video.')
            return
        }

        if (!selectedEffectId) {
            setError('Please select an effect.')
            return
        }

        setError('')
        setProcessing(true)
        setResult(null)

        try {
            const effectChoices = {
                ...choices,
                watermark: Boolean(watermark),
            }

            const data = await processEffect(
                video,
                selectedEffectId,
                effectChoices,
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

            {/* New effect library */}
            <EffectLibrary
                selectedEffectId={selectedEffectId}
                onSelectEffect={(effectId) => {
                    setSelectedEffectId(effectId)
                    setError('')
                    setResult(null)
                }}
            />

            <button
                type="button"
                onClick={handleProcessEffect}
                disabled={processing || !selectedEffectId}
            >
                {processing ? 'Processing...' : 'Apply Selected Effect'}
            </button>

            <hr />

            {/* Original theme workflow - kept temporarily */}
            <details>
                <summary>Original Theme Workflow</summary>

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

                {theme === 'futuristic' && (
                    <FuturisticSteps
                        choices={choices}
                        setChoices={setChoices}
                        watermark={watermark}
                        setWatermark={setWatermark}
                        onProcess={handleProcess}
                        processing={processing}
                    />
                )}

                {theme === 'retro' && (
                    <RetroSteps
                        choices={choices}
                        setChoices={setChoices}
                        watermark={watermark}
                        setWatermark={setWatermark}
                        onProcess={handleProcess}
                        processing={processing}
                    />
                )}

                {theme === 'cinematic' && (
                    <CinematicSteps
                        choices={choices}
                        setChoices={setChoices}
                        onProcess={handleProcess}
                        processing={processing}
                        watermark={watermark}
                        setWatermark={setWatermark}
                    />
                )}

                {theme === 'noir' && (
                    <NoirSteps
                        choices={choices}
                        setChoices={setChoices}
                        onProcess={handleProcess}
                        processing={processing}
                        watermark={watermark}
                        setWatermark={setWatermark}
                    />
                )}

                {theme === 'vhs' && (
                    <VHSSteps
                        choices={choices}
                        setChoices={setChoices}
                        onProcess={handleProcess}
                        processing={processing}
                        watermark={watermark}
                        setWatermark={setWatermark}
                    />
                )}

                {theme === 'dreamy' && (
                    <DreamySteps
                        choices={choices}
                        setChoices={setChoices}
                        onProcess={handleProcess}
                        processing={processing}
                        watermark={watermark}
                        setWatermark={setWatermark}
                    />
                )}

                {theme === 'action' && (
                    <ActionSteps
                        choices={choices}
                        setChoices={setChoices}
                        onProcess={handleProcess}
                        processing={processing}
                        watermark={watermark}
                        setWatermark={setWatermark}
                    />
                )}

                {theme === 'cyberpunk' && (
                    <CyberpunkSteps
                        choices={choices}
                        setChoices={setChoices}
                        onProcess={handleProcess}
                        processing={processing}
                        watermark={watermark}
                        setWatermark={setWatermark}
                    />
                )}

                {theme === 'travel' && (
                    <TravelSteps
                        choices={choices}
                        setChoices={setChoices}
                        onProcess={handleProcess}
                        processing={processing}
                        watermark={watermark}
                        setWatermark={setWatermark}
                    />
                )}

                {theme === 'silent_film' && (
                    <SilentFilmSteps
                        choices={choices}
                        setChoices={setChoices}
                        onProcess={handleProcess}
                        processing={processing}
                        watermark={watermark}
                        setWatermark={setWatermark}
                    />
                )}

                {theme === 'underwater' && (
                    <UnderwaterSteps
                        choices={choices}
                        setChoices={setChoices}
                        onProcess={handleProcess}
                        processing={processing}
                        watermark={watermark}
                        setWatermark={setWatermark}
                    />
                )}
            </details>

            {error && <p>{error}</p>}

            <ProcessedVideo result={result} />
        </div>
    )
}

export default App