
function CinematicSteps({
    choices,
    setChoices,
    onProcess,
    processing,
    watermark,
    setWatermark
}) {
    return (
        <div>
            <h2>Cinematic Theme</h2>

            <p>
                Give your video a dramatic, movie-like appearance.
            </p>

            <ul>
                <li>
                    Teal-and-orange color grading (0–2 seconds)
                </li>
                <li>
                    Gradually increasing vignette (2–4 seconds)
                </li>
                <li>
                    Gradually increasing contrast (4–6 seconds)
                </li>
                <li>
                    Cinematic black bars throughout the video
                </li>
            </ul>

            <label>
                <input
                    type="checkbox"
                    checked={choices.watermark || false}
                    onChange={(event) =>
                        setChoices({
                            ...choices,
                            watermark: event.target.checked
                        })
                    }
                />
                Add watermark
            </label>

            {choices.watermark && (
                <>
                    <div>
                        <label>
                            Watermark image:
                            <input
                                type="file"
                                accept="image/*"
                                onChange={(event) =>
                                    setWatermark(
                                        event.target.files[0]
                                    )
                                }
                            />
                        </label>
                    </div>

                    <div>
                        <label>
                            Watermark position:
                            <select
                                value={
                                    choices.watermarkPosition ||
                                    'top-right'
                                }
                                onChange={(event) =>
                                    setChoices({
                                        ...choices,
                                        watermarkPosition:
                                            event.target.value
                                    })
                                }
                            >
                                <option value="top-left">
                                    Top left
                                </option>
                                <option value="top-right">
                                    Top right
                                </option>
                                <option value="bottom-left">
                                    Bottom left
                                </option>
                                <option value="bottom-right">
                                    Bottom right
                                </option>
                            </select>
                        </label>
                    </div>
                </>
            )}

            <button
                onClick={onProcess}
                disabled={
                    processing ||
                    (choices.watermark && !watermark)
                }
            >
                {processing ? 'Processing...' : 'Apply Cinematic'}
            </button>
        </div>
    )
}

export default CinematicSteps
