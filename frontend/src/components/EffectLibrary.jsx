
import EffectCard from './EffectCard'
import { effects } from '../data/effects'
import './EffectLibrary.css'

const familyNames = {
    underwater: 'Underwater Effects',
    vintage: 'Vintage Effects',
}

function EffectLibrary({ selectedEffectId, onSelectEffect }) {
    const families = [...new Set(effects.map((effect) => effect.family))]

    return (
        <section className="effect-library">
            <div className="effect-library__header">
                <div>
                    <h2>Effect Library</h2>
                    <p>Choose an effect to preview and apply to your video.</p>
                </div>

                <span className="effect-library__count">
                    {effects.length} effects
                </span>
            </div>

            {families.map((family) => {
                const familyEffects = effects.filter(
                    (effect) => effect.family === family
                )

                return (
                    <div className="effect-library__family" key={family}>
                        <h3 className="effect-library__family-title">
                            {familyNames[family] || family}
                        </h3>

                        <div className="effect-library__grid">
                            {familyEffects.map((effect) => (
                                <EffectCard
                                    key={effect.id}
                                    effect={effect}
                                    selected={selectedEffectId === effect.id}
                                    onSelect={onSelectEffect}
                                />
                            ))}
                        </div>
                    </div>
                )
            })}
        </section>
    )
}

export default EffectLibrary
