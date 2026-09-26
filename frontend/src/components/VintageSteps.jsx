import { useState } from 'react'

function VintageSteps({
  choices,
  setChoices,
  watermark,
  setWatermark,
  onProcess,
  processing,
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
      <h2>Vintage Theme</h2>

      <p>Step {step} / 6</p>

      {step === 1 && (
        <div>
          <h3>Do you want to make the entire video black and white?</h3>

          <button
            style={{
              backgroundColor:
                choices.grayscale === true ? 'green' : '',
              color:
                choices.grayscale === true ? 'white' : '',
            }}
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
            style={{
              backgroundColor:
                choices.grayscale === false ? 'green' : '',
              color:
                choices.grayscale === false ? 'white' : '',
            }}
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

          <button
            onClick={nextStep}
            disabled={choices.grayscale === null}
          >
            Next
          </button>
        </div>
      )}

      {step === 2 && (
        <div>
          <h3>At what second should the rotation start?</h3>

          <input
            type="number"
            min="0"
            step="0.1"
            value={choices.rotationStart}
            onChange={(event) =>
              setChoices({
                ...choices,
                rotationStart: Number(event.target.value),
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

      {step === 4 && (
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

      {step === 5 && (
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
                  value={choices.speedStart}
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
                  value={choices.speedEnd}
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

      {step === 6 && (
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

export default VintageSteps