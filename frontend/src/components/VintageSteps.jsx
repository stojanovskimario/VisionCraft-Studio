function VintageSteps({ choices, setChoices, onProcess, processing }) {
  return (
    <div>
      <h2>Vintage Settings</h2>

      <div>
        <label>
          <input
            type="checkbox"
            checked={choices.grayscale}
            onChange={(event) =>
              setChoices({
                ...choices,
                grayscale: event.target.checked,
              })
            }
          />
          Make video black and white
        </label>
      </div>

      <div>
        <label>
          Rotation duration (seconds):
          <input
            type="number"
            min="0"
            step="0.1"
            value={choices.rotationDuration}
            onChange={(event) =>
              setChoices({
                ...choices,
                rotationDuration: Number(event.target.value),
              })
            }
          />
        </label>
      </div>

      <div>
        <label>
          Rotation degrees:
          <input
            type="number"
            value={choices.rotate}
            onChange={(event) =>
              setChoices({
                ...choices,
                rotate: Number(event.target.value),
              })
            }
          />
        </label>
      </div>

      <div>
        <label>
          Speed multiplier:
          <input
            type="number"
            min="0.1"
            step="0.1"
            value={choices.speed}
            onChange={(event) =>
              setChoices({
                ...choices,
                speed: Number(event.target.value),
              })
            }
          />
        </label>
      </div>

      <button
        onClick={onProcess}
        disabled={processing}
      >
        {processing ? 'Processing...' : 'Process Video'}
      </button>
    </div>
  )
}

export default VintageSteps