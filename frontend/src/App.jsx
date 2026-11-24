
import { useEffect, useState } from 'react'
import { processVideo, processEffect } from './services/api'
import { effects } from './data/effects'

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

import './VideoStudio.css'


function formatFileSize(bytes) {
    if (typeof bytes !== 'number') {
        return ''
    }

    return `${(bytes / (1024 * 1024)).toFixed(2)} MB`
}


function App() {
    const [video, setVideo] = useState(null)
    const [theme, setTheme] = useState('')

    // Individual effect library
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

    // Source video preview — visual only
    const [videoPreviewUrl, setVideoPreviewUrl] = useState(null)

    useEffect(() => {
        if (!video) {
            setVideoPreviewUrl(null)
            return
        }

        const url = URL.createObjectURL(video)
        setVideoPreviewUrl(url)

        return () => URL.revokeObjectURL(url)
    }, [video])

    const selectedEffect = effects.find(
        (effect) => effect.id === selectedEffectId
    )

    // ORIGINAL THEME PROCESSING — UNCHANGED
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

    // INDIVIDUAL EFFECT PROCESSING — UNCHANGED
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
        <div className="video-studio">

            {/* HERO */}
            <section className="video-studio__hero">
                <video
                    className="video-studio__hero-video"
                    autoPlay
                    muted
                    loop
                    playsInline
                    preload="metadata"
                    aria-hidden="true"
                    tabIndex={-1}
                >
                    <source
                        src="/hero/video-hero.mp4"
                        type="video/mp4"
                    />
                </video>
                <div className="video-studio__eyebrow">
                    <span className="video-studio__eyebrow-dot" />
                    VIDEO WORKSPACE
                </div>

                <h1>
                    Bring your videos{' '}
                    <span>to life.</span>
                </h1>

                <p>
                    Transform ordinary footage into something
                    extraordinary. Explore cinematic looks,
                    artistic styles, and creative motion effects.
                </p>

                <div className="video-studio__hero-stats">
                    <span>
                        <strong>{effects.length}</strong>
                        {' '}Video effects
                    </span>
                    <span>12 Creative families</span>
                    <span>Custom visual transformations</span>
                </div>
            </section>


            {/* VIDEO WORKSPACE */}
            <section className="video-studio__workspace">
                <div className="video-studio__section-heading">
                    <div>
                        <span className="video-studio__kicker">
                            YOUR WORKSPACE
                        </span>

                        <h2>Start creating</h2>

                        <p>
                            Upload your footage and choose
                            the perfect effect.
                        </p>
                    </div>

                    <span className="video-studio__status">
                        <span />
                        {video ? 'Video ready' : 'Ready to create'}
                    </span>
                </div>

                <div className="video-studio__workspace-grid">

                    {/* UPLOAD PANEL */}
                    <div className="video-studio__panel">
                        <div className="video-studio__panel-heading">
                            <span className="video-studio__step-number">
                                01
                            </span>

                            <div>
                                <h3>Upload your video</h3>
                                <p>Select the footage you want to edit</p>
                            </div>
                        </div>

                        <div className="video-studio__upload-body">
                            <VideoUpload
                                video={video}
                                setVideo={setVideo}
                            />
                        </div>

                        {video && (
                            <div className="video-studio__file-info">
                                <div className="video-studio__file-icon">
                                    <svg
                                        viewBox="0 0 24 24"
                                        fill="none"
                                        stroke="currentColor"
                                        strokeWidth="1.8"
                                        strokeLinecap="round"
                                        strokeLinejoin="round"
                                        aria-hidden="true"
                                    >
                                        <rect
                                            x="3" y="5"
                                            width="14" height="14"
                                            rx="3"
                                        />
                                        <path d="m17 10 4-3v10l-4-3" />
                                    </svg>
                                </div>

                                <div className="video-studio__file-text">
                                    <strong title={video.name}>
                                        {video.name}
                                    </strong>

                                    <span>
                                        {formatFileSize(video.size)}
                                    </span>
                                </div>

                                <span className="video-studio__file-check">
                                    ✓
                                </span>
                            </div>
                        )}
                    </div>


                    {/* VIDEO PREVIEW */}
                    <div className="video-studio__panel">
                        <div className="video-studio__panel-heading">
                            <span className="video-studio__step-number">
                                02
                            </span>

                            <div>
                                <h3>Source preview</h3>
                                <p>Review your original footage</p>
                            </div>
                        </div>

                        <div className="video-studio__preview">
                            {videoPreviewUrl ? (
                                <video
                                    src={videoPreviewUrl}
                                    controls
                                    playsInline
                                    preload="metadata"
                                    className="video-studio__preview-video"
                                />
                            ) : (
                                <div className="video-studio__preview-empty">
                                    <div className="video-studio__preview-icon">
                                        <svg
                                            viewBox="0 0 24 24"
                                            fill="none"
                                            stroke="currentColor"
                                            strokeWidth="1.5"
                                            strokeLinecap="round"
                                            strokeLinejoin="round"
                                            aria-hidden="true"
                                        >
                                            <rect
                                                x="3" y="5"
                                                width="14" height="14"
                                                rx="3"
                                            />
                                            <path d="m17 10 4-3v10l-4-3" />
                                        </svg>
                                    </div>

                                    <strong>
                                        Your video preview
                                    </strong>

                                    <p>
                                        Upload a video to see
                                        it here.
                                    </p>
                                </div>
                            )}
                        </div>

                        <div className="video-studio__preview-footer">
                            <span>
                                {video
                                    ? 'Original footage'
                                    : 'No video selected'}
                            </span>

                            <span>
                                {video
                                    ? 'Ready for editing'
                                    : 'Awaiting upload'}
                            </span>
                        </div>
                    </div>
                </div>
            </section>


            {/* VIDEO EFFECT LIBRARY */}
            <section className="video-studio__library">
                <div className="video-studio__library-intro">
                    <div>
                        <span className="video-studio__kicker">
                            DISCOVER YOUR STYLE
                        </span>

                        <h2>Explore video effects</h2>

                        <p>
                            Browse the collection and select
                            an effect for your video.
                        </p>
                    </div>
                </div>

                <EffectLibrary
                    selectedEffectId={selectedEffectId}
                    onSelectEffect={(effectId) => {
                        setSelectedEffectId(effectId)
                        setError('')
                        setResult(null)
                    }}
                />
            </section>


            {/* PROCESSING BAR */}
            <div className="video-studio__apply-bar">
                <div className="video-studio__apply-info">
                    <span>SELECTED EFFECT</span>

                    <strong>
                        {selectedEffect
                            ? selectedEffect.name
                            : 'No effect selected'}
                    </strong>

                    <small>
                        {selectedEffect
                            ? 'Ready to apply to your footage'
                            : 'Choose an effect from the library'}
                    </small>
                </div>

                <button
                    type="button"
                    className="video-studio__apply-button"
                    onClick={handleProcessEffect}
                    disabled={processing || !selectedEffectId}
                >
                    {processing ? (
                        <>
                            <span className="video-studio__spinner" />
                            Processing...
                        </>
                    ) : (
                        <>
                            Apply Selected Effect

                            <svg
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                strokeWidth="2"
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                aria-hidden="true"
                            >
                                <path d="M5 12h14" />
                                <path d="m13 6 6 6-6 6" />
                            </svg>
                        </>
                    )}
                </button>
            </div>

            {error && (
                <div
                    className="video-studio__error"
                    role="alert"
                >
                    {error}
                </div>
            )}


            {/* PROCESSED VIDEO */}
            <section className="video-studio__result">
                <div className="video-studio__section-heading">
                    <div>
                        <span className="video-studio__kicker">
                            YOUR FINAL CREATION
                        </span>

                        <h2>Processed video</h2>

                        <p>
                            Preview and download your
                            transformed footage.
                        </p>
                    </div>

                    {result && (
                        <span className="video-studio__result-ready">
                            ✓ Ready
                        </span>
                    )}
                </div>

                <div className="video-studio__result-panel">
                    {processing ? (
                        <div className="video-studio__result-empty">
                            <span className="video-studio__spinner video-studio__spinner--large" />

                            <strong>
                                Transforming your video
                            </strong>

                            <p>
                                Your selected effect is being applied.
                            </p>
                        </div>
                    ) : !result ? (
                        <div className="video-studio__result-empty">
                            <div className="video-studio__result-icon">
                                <svg
                                    viewBox="0 0 24 24"
                                    fill="none"
                                    stroke="currentColor"
                                    strokeWidth="1.5"
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    aria-hidden="true"
                                >
                                    <rect
                                        x="3" y="3"
                                        width="18" height="18"
                                        rx="3"
                                    />
                                    <path d="m3 17 5-5 4 4 3-3 6 6" />
                                    <circle cx="8.5" cy="8.5" r="1.5" />
                                </svg>
                            </div>

                            <strong>
                                Your finished video will appear here
                            </strong>

                            <p>
                                Upload footage, select an effect,
                                and start processing.
                            </p>
                        </div>
                    ) : null}

                    <ProcessedVideo result={result} />
                </div>
            </section>


            {/* ORIGINAL THEME WORKFLOW — PRESERVED */}
            <section className="video-studio__legacy">
                <details>
                    <summary>
                        <span>
                            Original Theme Workflow
                        </span>

                        <small>
                            Legacy editing controls
                        </small>
                    </summary>

                    <div className="video-studio__legacy-content">
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
                    </div>
                </details>
            </section>
        </div>
    )
}

export default App
