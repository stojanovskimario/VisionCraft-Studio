import { useState } from 'react'

function FuturisticSteps({
  choices,
  setChoices,
  watermark,
  setWatermark,
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
      <h2>Futuristic Theme</h2>

      <p>Step {step} / 4</p>

      {step === 1 && (
        <div>
          <h3>Do you want to apply a futuristic color effect?</h3>

            <button
                style={{
                    backgroundColor:
                        choices.colorEffect === true ? 'green' : '',
                    color:
                        choices.colorEffect === true ? 'white' : '',
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
                        choices.colorEffect === false ? 'green' : '',
                    color:
                        choices.colorEffect === false ? 'white' : '',
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
    <h3>Do you want to add a glitch effect?</h3>

    <button
      style={{
        backgroundColor:
          choices.glitch === true ? 'green' : '',
        color:
          choices.glitch === true ? 'white' : '',
      }}
      onClick={() =>
        setChoices({
          ...choices,
          glitch: true,
        })
      }
    >
      Yes
    </button>

    <button
      style={{
        backgroundColor:
          choices.glitch === false ? 'green' : '',
        color:
          choices.glitch === false ? 'white' : '',
      }}
      onClick={() =>
        setChoices({
          ...choices,
          glitch: false,
        })
      }
    >
      No
    </button>

    {choices.glitch && (
      <div>
        <br />

        <label>
          Start at:
          <input
            type="number"
            min="0"
            step="0.1"
            value={choices.glitchStart}
            onChange={(event) =>
              setChoices({
                ...choices,
                glitchStart: Number(event.target.value),
              })
            }
          />
          seconds
        </label>

        <br />

        <label>
          Duration:
          <input
            type="number"
            min="0.1"
            step="0.1"
            value={choices.glitchDuration}
            onChange={(event) =>
              setChoices({
                ...choices,
                glitchDuration: Number(event.target.value),
              })
            }
          />
          seconds
        </label>

        <br />

        <label>
          Intensity:
          <input
            type="number"
            min="1"
            max="10"
            step="1"
            value={choices.glitchIntensity}
            onChange={(event) =>
              setChoices({
                ...choices,
                glitchIntensity: Number(event.target.value),
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

    <button onClick={nextStep}>
      Next
    </button>
  </div>
)}

      {step === 3 && (
        <div>
          <h3>Do you want to speed up part of the video?</h3>

            <button
                style={{
                    backgroundColor:
                        choices.speed !== 1 ? 'green' : '',
                    color:
                        choices.speed !== 1 ? 'white' : '',
                }}
                onClick={() =>
                    setChoices({
                        ...choices,
                        speed: 1.5,
                    })
                }
            >
                Yes
            </button>

            <button
                style={{
                    backgroundColor:
                        choices.speed === 1 ? 'green' : '',
                    color:
                        choices.speed === 1 ? 'white' : '',
                }}
                onClick={() =>
                    setChoices({
                        ...choices,
                        speed: 1,
                    })
                }
            >
                No
            </button>

          {choices.speed !== 1 && (
            <div>
              <br />

              <label>
                Start at:
                <input
                  type="number"
                  min="0"
                  step="0.1"
                  value={choices.speedStart || 0}
                  onChange={(event) =>
                    setChoices({
                      ...choices,
                      speedStart: Number(event.target.value),
                    })
                  }
                />
                seconds
              </label>

              <br />

              <label>
                End at:
                <input
                  type="number"
                  min="0"
                  step="0.1"
                  value={choices.speedEnd || 0}
                  onChange={(event) =>
                    setChoices({
                      ...choices,
                      speedEnd: Number(event.target.value),
                    })
                  }
                />
                seconds
              </label>

              <br />

              <label>
                Speed:
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
                x
              </label>
            </div>
          )}

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
          <h3>Do you want to add a watermark?</h3>

          <button
            style={{
              backgroundColor:
                choices.watermark === true ? 'green' : '',
              color:
                choices.watermark === true ? 'white' : '',
            }}
            onClick={() =>
              setChoices({
                ...choices,
                watermark: true,
              })
            }
          >
            Yes
          </button>

          <button
            style={{
              backgroundColor:
                choices.watermark === false ? 'green' : '',
              color:
                choices.watermark === false ? 'white' : '',
            }}
            onClick={() => {
              setChoices({
                ...choices,
                watermark: false,
              })

              setWatermark(null)
            }}
          >
            No
          </button>

          {choices.watermark === true && (
            <div>
              <br />

              <label>
                Upload watermark:
                <input
                  type="file"
                  accept="image/*"
                  onChange={(event) =>
                    setWatermark(event.target.files[0])
                  }
                />
              </label>

              {watermark && (
                <p>
                  Selected watermark: {watermark.name}
                </p>
              )}

              <br />

              <h4>Where should the watermark appear?</h4>

              <button
                style={{
                  backgroundColor:
                    choices.watermarkPosition === 'top-left'
                      ? 'green'
                      : '',
                  color:
                    choices.watermarkPosition === 'top-left'
                      ? 'white'
                      : '',
                }}
                onClick={() =>
                  setChoices({
                    ...choices,
                    watermarkPosition: 'top-left',
                  })
                }
              >
                Top Left
              </button>

              <button
                style={{
                  backgroundColor:
                    choices.watermarkPosition === 'top-right'
                      ? 'green'
                      : '',
                  color:
                    choices.watermarkPosition === 'top-right'
                      ? 'white'
                      : '',
                }}
                onClick={() =>
                  setChoices({
                    ...choices,
                    watermarkPosition: 'top-right',
                  })
                }
              >
                Top Right
              </button>

              <button
                style={{
                  backgroundColor:
                    choices.watermarkPosition === 'bottom-left'
                      ? 'green'
                      : '',
                  color:
                    choices.watermarkPosition === 'bottom-left'
                      ? 'white'
                      : '',
                }}
                onClick={() =>
                  setChoices({
                    ...choices,
                    watermarkPosition: 'bottom-left',
                  })
                }
              >
                Bottom Left
              </button>

              <button
                style={{
                  backgroundColor:
                    choices.watermarkPosition === 'bottom-right'
                      ? 'green'
                      : '',
                  color:
                    choices.watermarkPosition === 'bottom-right'
                      ? 'white'
                      : '',
                }}
                onClick={() =>
                  setChoices({
                    ...choices,
                    watermarkPosition: 'bottom-right',
                  })
                }
              >
                Bottom Right
              </button>
            </div>
          )}

          <br />
          <br />

          <button onClick={previousStep}>
            Back
          </button>

          <button
            onClick={onProcess}
            disabled={
              processing ||
              (choices.watermark === true && !watermark)
            }
          >
            {processing ? 'Processing...' : 'Process Video'}
          </button>
        </div>
      )}
    </div>
  )
}

export default FuturisticSteps