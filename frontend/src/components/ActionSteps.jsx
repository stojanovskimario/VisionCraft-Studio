
import React from 'react';

function ActionSteps({
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
            <h2>Action Theme</h2>

            <p>
                Give your video an intense, dynamic look with
                animated zoom, camera shake, increased contrast,
                and a speed boost.
            </p>

            <h3>Effects applied</h3>

            <ul>
                <li>
                    <strong>0–2 seconds:</strong> Gradually zoom in.
                </li>
                <li>
                    <strong>2–4 seconds:</strong> Add dynamic camera shake.
                </li>
                <li>
                    <strong>Throughout the video:</strong> Increase contrast.
                </li>
                <li>
                    <strong>4–6 seconds:</strong> Speed up to 1.5×.
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
                        <label htmlFor="action-watermark-file">
                            Watermark image
                        </label>

                        <input
                            id="action-watermark-file"
                            type="file"
                            accept="image/*"
                            onChange={handleWatermarkFileChange}
                        />

                        <label htmlFor="action-watermark-position">
                            Watermark position
                        </label>

                        <select
                            id="action-watermark-position"
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
                {processing ? 'Processing...' : 'Apply Action Theme'}
            </button>
        </div>
    );
}

export default ActionSteps;
