
import React from 'react';

function CyberpunkSteps({
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
            <h2>Cyberpunk Theme</h2>

            <p>
                Transform your video into a futuristic,
                neon-lit scene with vivid colors, digital glitches,
                deep shadows, and glowing highlights.
            </p>

            <h3>Effects applied</h3>

            <ul>
                <li>
                    <strong>0–2 seconds:</strong> Shift colors toward
                    cyan and magenta.
                </li>
                <li>
                    <strong>2–4 seconds:</strong> Gradually increase
                    contrast.
                </li>
                <li>
                    <strong>4–5 seconds:</strong> Apply an RGB glitch
                    effect.
                </li>
                <li>
                    <strong>5–7 seconds:</strong> Add a subtle glow.
                </li>
                <li>
                    <strong>Throughout:</strong> Keep shadows dark.
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
                        <label htmlFor="cyberpunk-watermark-file">
                            Watermark image
                        </label>

                        <input
                            id="cyberpunk-watermark-file"
                            type="file"
                            accept="image/*"
                            onChange={handleWatermarkFileChange}
                        />

                        <label htmlFor="cyberpunk-watermark-position">
                            Watermark position
                        </label>

                        <select
                            id="cyberpunk-watermark-position"
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
                {processing ? 'Processing...' : 'Apply Cyberpunk Theme'}
            </button>
        </div>
    );
}

export default CyberpunkSteps;
