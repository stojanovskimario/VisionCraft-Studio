import { useState } from 'react'

function RetroSteps({
  choices,
  setChoices,
  onProcess,
  processing
}) {
  const [step, setStep] = useState(1)

  const nextStep = () => {
    setStep(step + 1)
  }

  const previousStep = () => {
    setStep(step - 1)
  }

  return (
    <div>
      <h2>Retro Theme</h2>

      <p>Step {step} / 2</p>

      {step === 1 && (
        <div>
          <h3>
            Do you want to apply a retro color effect?
          </h3>

          <button
            style={{
              backgroundColor:
                choices.colorEffect === true
                  ? 'green'
                  : '',
              color:
                choices.colorEffect === true
                  ? 'white'
                  : '',
            }}
            onClick={() =>
              setChoices({
                ...choices,
                colorEffect: true,
              })
            }
          >
            Yes
          </button>

          <button
            style={{
              backgroundColor:
                choices.colorEffect === false
                  ? 'green'
                  : '',
              color:
                choices.colorEffect === false
                  ? 'white'
                  : '',
            }}
            onClick={() =>
              setChoices({
                ...choices,
                colorEffect: false,
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
          <h3>
            Do you want to add film grain?
          </h3>

          <button
            style={{
              backgroundColor:
                choices.filmGrain === true
                  ? 'green'
                  : '',
              color:
                choices.filmGrain === true
                  ? 'white'
                  : '',
            }}
            onClick={() =>
              setChoices({
                ...choices,
                filmGrain: true,
              })
            }
          >
            Yes
          </button>

          <button
            style={{
              backgroundColor:
                choices.filmGrain === false
                  ? 'green'
                  : '',
              color:
                choices.filmGrain === false
                  ? 'white'
                  : '',
            }}
            onClick={() =>
              setChoices({
                ...choices,
                filmGrain: false,
              })
            }
          >
            No
          </button>

          {choices.filmGrain === true && (
            <div>
              <br />

              <label>
                Grain intensity:

                <input
                  type="number"
                  min="1"
                  max="10"
                  step="1"
                  value={
                    choices.filmGrainIntensity
                  }
                  onChange={(event) =>
                    setChoices({
                      ...choices,
                      filmGrainIntensity:
                        Number(
                          event.target.value
                        ),
                    })
                  }
                />

                / 10
              </label>
            </div>
          )}

          <br />
          <br />

          <button onClick={previousStep}>
            Back
          </button>

          <button
            onClick={onProcess}
            disabled={processing}
          >
            {processing
              ? 'Processing...'
              : 'Process Video'}
          </button>
        </div>
      )}
    </div>
  )
}

export default RetroSteps