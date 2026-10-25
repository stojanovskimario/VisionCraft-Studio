
function VHSSteps({
    choices,
    setChoices,
    onProcess,
    processing,
    watermark,
    setWatermark
}) {
    return (
        <div>
            <h2>VHS Theme</h2>

            <p>
                Recreate the appearance of an old videotape recording.
            </p>

            <ul>
                <li>Faded, slightly desaturated colors</li>
                <li>Horizontal scanlines throughout</li>
                <li>RGB and horizontal glitch distortion (2–4 seconds)</li>
                <li>Subtle analog noise throughout</li>
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
                                    setWatermark(event.target.files[0])
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
                                        watermarkPosition: event.target.value
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
                {processing ? 'Processing...' : 'Apply VHS'}
            </button>
        </div>
    )
}

export default VHSSteps
