
import React from 'react';

function SilentFilmSteps({
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
            <h2>Silent Film Theme</h2>

            <p>
                Recreate the look of early black-and-white movies
                with scratches, dust, flicker, grain, and vignette.
            </p>

            <h3>Effects applied</h3>
            <ul>
                <li>0–2 seconds: Gradual transition to black and white.</li>
                <li>2–4 seconds: Film scratches and dust.</li>
                <li>4–6 seconds: Mild brightness flicker.</li>
                <li>Throughout: Film grain and vignette.</li>
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
                        <label htmlFor="silent-film-watermark-file">
                            Watermark image
                        </label>
                        <input
                            id="silent-film-watermark-file"
                            type="file"
                            accept="image/*"
                            onChange={handleWatermarkFileChange}
                        />

                        <label htmlFor="silent-film-watermark-position">
                            Watermark position
                        </label>
                        <select
                            id="silent-film-watermark-position"
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
                {processing ? 'Processing...' : 'Apply Silent Film Theme'}
            </button>
        </div>
    );
}

export default SilentFilmSteps;
