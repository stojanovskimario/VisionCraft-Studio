import { useState } from 'react'

function VintageSteps({ choices, setChoices, onProcess, processing }) {
  const [step, setStep] = useState(1)

  const nextStep = () => {
    setStep(step + 1)
  }

  const previousStep = () => {
    setStep(step - 1)
  }

  return (
    <div>
      <h2>Vintage Theme</h2>

      <p>Step {step} / 4</p>

      {step === 1 && (
        <div>
          <h3>Do you want to make the video black and white?</h3>

          <button
            onClick={() =>
              setChoices({
                ...choices,
                grayscale: true,
              })
            }
          >
            Yes
          </button>

          <button
            onClick={() =>
              setChoices({
                ...choices,
                grayscale: false,
              })
            }
          >
            No
          </button>

          <br />
          <br />

          <button onClick={nextStep}>
            Next
          </button>
        </div>
      )}

      {step === 2 && (
        <div>
          <h3>How long should the rotation last?</h3>

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

          <span> seconds</span>

          <br />
          <br />

          <button onClick={previousStep}>
            Back
          </button>

          <button onClick={nextStep}>
            Next
          </button>
        </div>
      )}

      {step === 3 && (
        <div>
          <h3>How many degrees should the video rotate?</h3>

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

          <span>°</span>

          <br />
          <br />

          <button onClick={previousStep}>
            Back
          </button>

          <button onClick={nextStep}>
            Next
          </button>
        </div>
      )}

      {step === 4 && (
        <div>
          <h3>How much do you want to speed up the video?</h3>

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

          <span>x</span>

          <br />
          <br />

          <button onClick={previousStep}>
            Back
          </button>

          <button
            onClick={onProcess}
            disabled={processing}
          >
            {processing ? 'Processing...' : 'Process Video'}
          </button>
        </div>
      )}
    </div>
  )
}

export default VintageSteps