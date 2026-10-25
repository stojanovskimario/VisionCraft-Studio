import { useState } from 'react'

function FuturisticSteps({
  choices,
  setChoices,
  watermark,
  setWatermark,
  onProcess,
  processing
}) {
  const [confirmed, setConfirmed] = useState(false)

  const futuristicChoices = {
    ...choices,
    colorEffect: true,
    glitch: true,
    glitchStart: 2,
    glitchDuration: 2,
    glitchIntensity: 5,
    speed: 1.3,
    speedStart: 5,
    speedEnd: 7
  }

  const handleApply = () => {
    setConfirmed(true)
    onProcess(futuristicChoices)
  }

  return (
    <div>
      <h2>Futuristic Theme</h2>

      <h3>
        This theme will change your video in the following ways:
      </h3>

      <ul>
        <li>
          Apply a futuristic color effect to the entire video,
          with enhanced blue tones and increased contrast.
        </li>
        <li>
          Apply a glitch effect starting at 2 seconds,
          lasting 2 seconds, with an intensity of 5/10.
        </li>
        <li>
          Speed up the section from 5 to 7 seconds
          to 1.3× its original speed, then continue
          at normal speed.
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
        Futuristic theme to your video.
      </p>

      <button
        onClick={handleApply}
        disabled={
          processing ||
          confirmed ||
          (choices.watermark === true && !watermark)
        }
      >
        {processing
          ? 'Processing...'
          : confirmed
            ? 'Processing requested...'
            : 'Apply Futuristic'}
      </button>
    </div>
  )
}

export default FuturisticSteps