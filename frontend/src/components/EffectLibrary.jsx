import EffectCard from './EffectCard'
import { effects } from '../data/effects'
import './EffectLibrary.css'

function EffectLibrary({ selectedEffectId, onSelectEffect }) {
    return (
        <section className="effect-library">
            <div className="effect-library__header">
                <div>
                    <h2>Underwater Effects</h2>
                    <p>Choose an effect to preview and apply to your video.</p>
                </div>

                <span className="effect-library__count">
                    {effects.length} effects
                </span>
            </div>

            <div className="effect-library__grid">
                {effects.map((effect) => (
                    <EffectCard
                        key={effect.id}
                        effect={effect}
                        selected={selectedEffectId === effect.id}
                        onSelect={onSelectEffect}
                    />
                ))}
            </div>
        </section>
    )
}

export default EffectLibrary