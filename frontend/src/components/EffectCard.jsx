import { useEffect, useState } from 'react'

function EffectCard({ effect, selected, onSelect }) {
    const imageSrc = selected ? effect.preview : effect.thumbnail
    const [imageFailed, setImageFailed] = useState(false)

    useEffect(() => {
        setImageFailed(false)
    }, [imageSrc])

    return (
        <button
            type="button"
            className={`effect-card ${selected ? 'effect-card--selected' : ''}`}
            onClick={() => onSelect(effect.id)}
            aria-pressed={selected}
        >
            <div className="effect-card__image">
                {imageFailed ? (
                    <div className="effect-card__placeholder">
                        <span>{effect.name}</span>
                    </div>
                ) : (
                    <img
                        src={imageSrc}
                        alt={`${effect.name} effect preview`}
                        onError={() => setImageFailed(true)}
                    />
                )}

                {selected && (
                    <span className="effect-card__selected-label">
                        Selected
                    </span>
                )}
            </div>

            <div className="effect-card__content">
                <h3>{effect.name}</h3>
                <p>{effect.description}</p>
            </div>
        </button>
    )
}

export default EffectCard