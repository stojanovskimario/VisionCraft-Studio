
function VintageSteps({
  choices,
  setChoices,
  watermark,
  setWatermark,
  onProcess,
  processing
}) {
  return (
    <div>
      <h2>Vintage Theme</h2>

      <h3>This theme will change your video in the following ways:</h3>

      <ul>
        <li>
          Convert the entire video to black and white.
        </li>
        <li>
          Starting at 2 seconds, rotate the video to
          90° over 1 second, hold that angle for
          1 second, then return to its original
          orientation over 1 second.
        </li>
        <li>
          Speed up the section from 5 to 7 seconds
          to 1.5× its original speed, then return
          to normal speed.
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
        Vintage theme to your video.
      </p>

      <button
        onClick={onProcess}
        disabled={
          processing ||
          (choices.watermark === true && !watermark)
        }
      >
        {processing ? 'Processing...' : 'Apply Vintage'}
      </button>
    </div>
  )
}

export default VintageSteps
