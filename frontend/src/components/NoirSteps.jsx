
function NoirSteps({
    choices,
    setChoices,
    onProcess,
    processing,
    watermark,
    setWatermark
}) {
    return (
        <div>
            <h2>Noir Theme</h2>

            <p>
                Give your video a dramatic black-and-white film look.
            </p>

            <ul>
                <li>Black-and-white color throughout</li>
                <li>Gradually increasing contrast (0–3 seconds)</li>
                <li>Strong vignette (2–4 seconds)</li>
                <li>Subtle film grain throughout</li>
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
                                <option value="top-left">Top left</option>
                                <option value="top-right">Top right</option>
                                <option value="bottom-left">Bottom left</option>
                                <option value="bottom-right">Bottom right</option>
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
                {processing ? 'Processing...' : 'Apply Noir'}
            </button>
        </div>
    )
}

export default NoirSteps
