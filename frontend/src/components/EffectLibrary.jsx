
import { useState } from 'react'

import EffectCard from './EffectCard'
import { effects } from '../data/effects'

import './EffectLibrary.css'


const familyNames = {
    underwater: 'Underwater Effects',
    vintage: 'Vintage Effects',
    futuristic: 'Futuristic Effects',
    retro: 'Retro Effects',
    cinematic: 'Cinematic Effects',
    noir: 'Noir Effects',
    vhs: 'VHS Effects',
    dreamy: 'Dreamy Effects',
    action: 'Action Effects',
    travel: 'Travel Effects',
    artistic: 'Artistic Effects',
    creative_motion: 'Creative Motion & Composition Effects',
}

const FAMILY_ORDER = [
    'vintage',
    'futuristic',
    'vhs',
    'cinematic',
    'noir',
    'retro',
    'artistic',
    'dreamy',
    'creative_motion',
    'travel',
    'action',
    'underwater',
]


function EffectLibrary({
    selectedEffectId,
    onSelectEffect
}) {
    const [search, setSearch] = useState('')
    const [activeFamily, setActiveFamily] = useState('all')

    const availableFamilies = [
        ...new Set(effects.map((effect) => effect.family))
    ]

    const families = [
        ...FAMILY_ORDER.filter(
            (family) => availableFamilies.includes(family)
        ),
        ...availableFamilies.filter(
            (family) => !FAMILY_ORDER.includes(family)
        ),
    ]

    const query = search.trim().toLowerCase()

    const filteredEffects = effects.filter((effect) => {
        const matchesFamily =
            activeFamily === 'all' ||
            effect.family === activeFamily

        const searchableText = [
            effect.name,
            effect.description,
            effect.family,
            familyNames[effect.family],
        ]
            .filter(Boolean)
            .join(' ')
            .toLowerCase()

        const matchesSearch = searchableText.includes(query)

        return matchesFamily && matchesSearch
    })

    const visibleFamilies = families.filter((family) =>
        filteredEffects.some(
            (effect) => effect.family === family
        )
    )

    return (
        <section className="effect-library">

            <div className="effect-library__header">
                <div>
                    <h2>Effect Library</h2>

                    <p>
                        Discover styles across all
                        12 creative families.
                    </p>
                </div>

                <span className="effect-library__count">
                    {filteredEffects.length} / {effects.length} effects
                </span>
            </div>


            {/* SEARCH */}
            <div className="effect-library__toolbar">
                <label className="effect-library__search">
                    <svg
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        aria-hidden="true"
                    >
                        <circle cx="11" cy="11" r="7" />
                        <path d="m20 20-4-4" />
                    </svg>

                    <input
                        type="search"
                        value={search}
                        onChange={(event) =>
                            setSearch(event.target.value)
                        }
                        placeholder="Search video effects..."
                        aria-label="Search video effects"
                    />
                </label>
            </div>


            {/* FAMILY FILTERS */}
            <div className="effect-library__filters">
                <button
                    type="button"
                    className={
                        'effect-library__filter' +
                        (activeFamily === 'all'
                            ? ' effect-library__filter--active'
                            : '')
                    }
                    aria-pressed={activeFamily === 'all'}
                    onClick={() => setActiveFamily('all')}
                >
                    All effects
                </button>

                {families.map((family) => (
                    <button
                        key={family}
                        type="button"
                        className={
                            'effect-library__filter' +
                            (activeFamily === family
                                ? ' effect-library__filter--active'
                                : '')
                        }
                        aria-pressed={activeFamily === family}
                        onClick={() => setActiveFamily(family)}
                    >
                        {familyNames[family] || family}
                    </button>
                ))}
            </div>


            {/* EFFECTS GROUPED BY FAMILY */}
            {visibleFamilies.map((family) => {
                const familyEffects = filteredEffects.filter(
                    (effect) => effect.family === family
                )

                return (
                    <div
                        className="effect-library__family"
                        key={family}
                    >
                        <div className="effect-library__family-heading">
                            <h3 className="effect-library__family-title">
                                {familyNames[family] || family}
                            </h3>

                            <span className="effect-library__family-count">
                                {familyEffects.length}
                                {' '}
                                {familyEffects.length === 1
                                    ? 'effect'
                                    : 'effects'}
                            </span>
                        </div>

                        <div className="effect-library__grid">
                            {familyEffects.map((effect) => (
                                <EffectCard
                                    key={effect.id}
                                    effect={effect}
                                    selected={
                                        selectedEffectId === effect.id
                                    }
                                    onSelect={onSelectEffect}
                                />
                            ))}
                        </div>
                    </div>
                )
            })}


            {/* NO SEARCH RESULTS */}
            {filteredEffects.length === 0 && (
                <div className="effect-library__empty">
                    <strong>No matching effects</strong>

                    <p>
                        Try a different name or category.
                    </p>

                    <button
                        type="button"
                        onClick={() => {
                            setSearch('')
                            setActiveFamily('all')
                        }}
                    >
                        Show all effects
                    </button>
                </div>
            )}
        </section>
    )
}

export default EffectLibrary
