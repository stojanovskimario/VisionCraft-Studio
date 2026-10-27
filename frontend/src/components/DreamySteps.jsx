
import React from 'react';

function DreamySteps({
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
            <h2>Dreamy Theme</h2>

            <p>
                Give your video a soft, bright, and dreamy appearance
                with gentle colors and a subtle glow.
            </p>

            <h3>Effects applied</h3>

            <ul>
                <li>
                    <strong>0–2 seconds:</strong> Gradually increase
                    brightness.
                </li>
                <li>
                    <strong>2–4 seconds:</strong> Introduce a soft-focus
                    blur.
                </li>
                <li>
                    <strong>4–6 seconds:</strong> Gradually increase
                    color saturation.
                </li>
                <li>
                    <strong>Throughout the video:</strong> Add a subtle
                    glow around bright areas.
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
                        <label htmlFor="dreamy-watermark-file">
                            Watermark image
                        </label>

                        <input
                            id="dreamy-watermark-file"
                            type="file"
                            accept="image/*"
                            onChange={handleWatermarkFileChange}
                        />

                        <label htmlFor="dreamy-watermark-position">
                            Watermark position
                        </label>

                        <select
                            id="dreamy-watermark-position"
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
                {processing ? 'Processing...' : 'Apply Dreamy Theme'}
            </button>
        </div>
    );
}

export default DreamySteps;
