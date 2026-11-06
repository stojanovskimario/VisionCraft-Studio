
import React from 'react';

function UnderwaterSteps({
    choices,
    setChoices,
    onProcess,
    processing,
    watermark,
    setWatermark
}) {
    const handleWatermarkChange = (enabled) => {
        setWatermark(enabled);
        setChoices((previous) => ({
            ...previous,
            watermark: enabled
        }));
    };

    const handleWatermarkFileChange = (event) => {
        const file = event.target.files[0];

        setChoices((previous) => ({
            ...previous,
            watermarkFile: file
        }));
    };

    const canProcess =
        !processing && (!watermark || choices.watermarkFile);

    return (
        <div className="theme-steps">
            <h2>Underwater Theme</h2>

            <p>
                Transform your video into an underwater scene with
                blue and turquoise tones, flowing water distortion,
                floating bubbles, and cinematic light rays.
            </p>

            <h3>Effects applied</h3>
            <ul>
                <li>Gradual blue and turquoise color grading.</li>
                <li>Animated water distortion across the image.</li>
                <li>Floating bubbles and underwater particles.</li>
                <li>Soft, moving underwater light rays.</li>
                <li>Subtle brightness variation and soft focus.</li>
                <li>Slightly reduced contrast for a natural underwater atmosphere.</li>
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
                        <label htmlFor="underwater-watermark-file">
                            Watermark image
                        </label>
                        <input
                            id="underwater-watermark-file"
                            type="file"
                            accept="image/*"
                            onChange={handleWatermarkFileChange}
                        />

                        <label htmlFor="underwater-watermark-position">
                            Watermark position
                        </label>
                        <select
                            id="underwater-watermark-position"
                            value={choices.watermarkPosition || 'top-right'}
                            onChange={(event) =>
                                setChoices((previous) => ({
                                    ...previous,
                                    watermarkPosition: event.target.value
                                }))
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
                {processing ? 'Processing...' : 'Apply Underwater Theme'}
            </button>
        </div>
    );
}

export default UnderwaterSteps;
