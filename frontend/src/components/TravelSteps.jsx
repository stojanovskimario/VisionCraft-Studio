
import React from 'react';

function TravelSteps({
    choices,
    setChoices,
    onProcess,
    processing,
    watermark,
    setWatermark
}) {
    const handleWatermarkChange = (enabled) => {
        setWatermark(enabled);

        setChoices((previousChoices) => ({
            ...previousChoices,
            watermark: enabled
        }));
    };

    const handleWatermarkPositionChange = (position) => {
        setChoices((previousChoices) => ({
            ...previousChoices,
            watermarkPosition: position
        }));
    };

    const handleWatermarkFileChange = (event) => {
        const file = event.target.files[0];

        setChoices((previousChoices) => ({
            ...previousChoices,
            watermarkFile: file
        }));
    };

    const canProcess =
        !processing &&
        (!watermark || choices.watermarkFile);

    return (
        <div className="theme-steps">
            <h2>Travel Theme</h2>

            <p>
                Enhance landscapes, holidays, and travel videos
                with vibrant colors, warm tones, a gentle zoom,
                and a smooth fade-out.
            </p>

            <h3>Effects applied</h3>

            <ul>
                <li>
                    <strong>0–2 seconds:</strong> Gradually increase
                    saturation.
                </li>
                <li>
                    <strong>2–4 seconds:</strong> Add a warm color tint.
                </li>
                <li>
                    <strong>4–6 seconds:</strong> Apply a subtle zoom-in.
                </li>
                <li>
                    <strong>Final 2 seconds:</strong> Fade out to black.
                </li>
            </ul>

            <div className="watermark-options">
                <label>
                    <input
                        type="checkbox"
                        checked={watermark}
                        onChange={(event) =>
                            handleWatermarkChange(event.target.checked)
                        }
                    />
                    Add a watermark
                </label>

                {watermark && (
                    <div>
                        <label htmlFor="travel-watermark-file">
                            Watermark image
                        </label>

                        <input
                            id="travel-watermark-file"
                            type="file"
                            accept="image/*"
                            onChange={handleWatermarkFileChange}
                        />

                        <label htmlFor="travel-watermark-position">
                            Watermark position
                        </label>

                        <select
                            id="travel-watermark-position"
                            value={
                                choices.watermarkPosition || 'top-right'
                            }
                            onChange={(event) =>
                                handleWatermarkPositionChange(
                                    event.target.value
                                )
                            }
                        >
                            <option value="top-left">Top left</option>
                            <option value="top-right">Top right</option>
                            <option value="bottom-left">Bottom left</option>
                            <option value="bottom-right">Bottom right</option>
                        </select>
                    </div>
                )}
            </div>

            <button
                type="button"
                onClick={() => onProcess()}
                disabled={!canProcess}
            >
                {processing ? 'Processing...' : 'Apply Travel Theme'}
            </button>
        </div>
    );
}

export default TravelSteps;
