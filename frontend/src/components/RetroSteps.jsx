import { useState } from 'react'

function RetroSteps({
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
      <h2>Retro Theme</h2>

      <p>Step {step} / 4</p>

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

          <button onClick={nextStep}>
            Next
          </button>
        </div>
      )}

      {step === 3 && (
        <div>
          <h3>
            Do you want to add a vignette effect?
          </h3>

          <button
            style={{
              backgroundColor:
                choices.vignette === true
                  ? 'green'
                  : '',
              color:
                choices.vignette === true
                  ? 'white'
                  : '',
            }}
            onClick={() =>
              setChoices({
                ...choices,
                vignette: true,
              })
            }
          >
            Yes
          </button>

          <button
            style={{
              backgroundColor:
                choices.vignette === false
                  ? 'green'
                  : '',
              color:
                choices.vignette === false
                  ? 'white'
                  : '',
            }}
            onClick={() =>
              setChoices({
                ...choices,
                vignette: false,
              })
            }
          >
            No
          </button>

          {choices.vignette === true && (
            <div>
              <br />

              <label>
                Vignette intensity:

                <input
                  type="number"
                  min="1"
                  max="10"
                  step="1"
                  value={
                    choices.vignetteIntensity
                  }
                  onChange={(event) =>
                    setChoices({
                      ...choices,
                      vignetteIntensity:
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

            <button onClick={nextStep}>
                Next
            </button>
        </div>
      )}

        {step === 4 && (
            <div>
                <h3>
                    Do you want to add a watermark?
                </h3>

                <button
                    style={{
                        backgroundColor:
                            choices.watermark === true
                                ? 'green'
                                : '',
                        color:
                            choices.watermark === true
                                ? 'white'
                                : '',
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
                            choices.watermark === false
                                ? 'green'
                                : '',
                        color:
                            choices.watermark === false
                                ? 'white'
                                : '',
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
                        <br/>

                        <input
                            type="file"
                            accept="image/*"
                            onChange={(event) =>
                                setWatermark(
                                    event.target.files[0]
                                )
                            }
                        />

                        <br/>
                        <br/>

                        <label>
                            Watermark position:

                            <select
                                value={
                                    choices.watermarkPosition
                                }
                                onChange={(event) =>
                                    setChoices({
                                        ...choices,
                                        watermarkPosition:
                                        event.target.value,
                                    })
                                }
                            >
                                <option value="top-left">
                                    Top Left
                                </option>

                                <option value="top-right">
                                    Top Right
                                </option>

                                <option value="bottom-left">
                                    Bottom Left
                                </option>

                                <option value="bottom-right">
                                    Bottom Right
                                </option>
                            </select>
                        </label>
                    </div>
                )}

                <br/>
                <br/>

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