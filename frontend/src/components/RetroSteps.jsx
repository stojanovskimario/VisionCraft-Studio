function RetroSteps({
  choices,
  setChoices,
  watermark,
  setWatermark,
  onProcess,
  processing
}) {
  return (
    <div>
      <h2>Retro Theme</h2>

      <h3>
        This theme will change your video in the following ways:
      </h3>

      <ul>
        <li>
          Apply warm retro colors throughout the entire video.
        </li>
        <li>
          Add film grain at a fixed intensity of 5/10
          to create an old-film appearance.
        </li>
        <li>
          Apply a vignette at a fixed intensity of 1/10,
          darkening the edges of the video.
        </li>
      </ul>

      <hr />

      <h3>Optional watermark</h3>

      <label>
        <input
          type="checkbox"
          checked={choices.watermark === true}
          onChange={(event) => {
            const enabled = event.target.checked

            setChoices({
              ...choices,
              watermark: enabled
            })

            if (!enabled) {
              setWatermark(null)
            }
          }}
        />
        Add a watermark
      </label>

      {choices.watermark === true && (
        <div>
          <br />

          <label>
            Upload watermark:

            <input
              type="file"
              accept="image/*"
              onChange={(event) =>
                setWatermark(
                  event.target.files?.[0] ?? null
                )
              }
            />
          </label>

          {watermark && (
            <p>
              Selected watermark: {watermark.name}
            </p>
          )}

          <br />

          <label>
            Watermark position:

            <select
              value={
                choices.watermarkPosition || 'top-right'
              }
              onChange={(event) =>
                setChoices({
                  ...choices,
                  watermarkPosition: event.target.value
                })
              }
            >
              <option value="top-left">Top Left</option>
              <option value="top-right">Top Right</option>
              <option value="bottom-left">Bottom Left</option>
              <option value="bottom-right">Bottom Right</option>
            </select>
          </label>
        </div>
      )}

      <hr />

      <p>
        Review the effects above before applying the
        Retro theme to your video.
      </p>

      <button
        onClick={onProcess}
        disabled={
          processing ||
          (choices.watermark === true && !watermark)
        }
      >
        {processing ? 'Processing...' : 'Apply Retro'}
      </button>
    </div>
  )
}

export default RetroSteps