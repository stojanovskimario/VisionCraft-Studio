
import { useEffect, useRef, useState } from "react";

import * as videoEffectCatalog from "../data/effects";
import { processPhotoEffect } from "../services/photoApi";

import "./PhotoEditor.css";


const PHOTO_EFFECTS = [
    { id: "pixel_art", name: "Pixel Art", family: "artistic", match: "pixel art" },
    { id: "mosaic", name: "Mosaic", family: "artistic", match: "mosaic" },
    { id: "comic_book", name: "Comic Book", family: "retro", match: "comic book" },
    { id: "classic_noir", name: "Classic Noir", family: "noir", match: "classic noir" },
    { id: "vintage_sepia", name: "Vintage Sepia", family: "vintage", match: "sepia" },
    { id: "cyberpunk_neon", name: "Cyberpunk Neon", family: "futuristic", match: "cyberpunk neon" },

    { id: "abyss", name: "Abyss", family: "underwater", match: "abyss" },
    { id: "deep_ocean", name: "Deep Ocean", family: "underwater", match: "deep ocean" },
    { id: "faded_memories", name: "Faded Memories", family: "vintage", match: "faded" },
    { id: "wireframe_reality", name: "Wireframe Reality", family: "futuristic", match: "wireframe" },
    { id: "synthwave", name: "Synthwave", family: "retro", match: "synthwave" },
    { id: "camcorder_90s", name: "90s Camcorder", family: "retro", match: "camcorder" },
    { id: "golden_hour_cinema", name: "Golden Hour Cinema", family: "cinematic", match: "golden hour" },
    { id: "dark_moody", name: "Dark & Moody", family: "cinematic", match: "dark" },
    { id: "midnight_blue", name: "Midnight Blue", family: "noir", match: "midnight blue" },
    { id: "evidence_triptych", name: "Evidence Triptych", family: "noir", match: "evidence triptych" },
    { id: "chroma_bleed", name: "Chroma Bleed", family: "vhs", match: "chroma bleed" },
    { id: "window_light", name: "Window Light", family: "dreamy", match: "window light" },
    { id: "wildflower", name: "Wildflower", family: "dreamy", match: "wildflower" },
    { id: "miniature_world", name: "Miniature World", family: "travel", match: "miniature world" },
    { id: "pencil_sketch", name: "Pencil Sketch", family: "artistic", match: "pencil sketch" },
    { id: "oil_painting", name: "Oil Painting", family: "artistic", match: "oil painting" },
    { id: "watercolor", name: "Watercolor", family: "artistic", match: "watercolor" },
    { id: "photo_stack", name: "Photo Stack", family: "creative_motion", match: "photo stack" },
];


const FAMILY_NAMES = {
    artistic: "Artistic",
    retro: "Retro",
    noir: "Noir",
    vintage: "Vintage",
    futuristic: "Futuristic",
    underwater: "Underwater",
    cinematic: "Cinematic",
    vhs: "VHS",
    dreamy: "Dreamy",
    travel: "Travel",
    creative_motion: "Creative Motion",
};


const existingVideoEffects = Object.values(
    videoEffectCatalog
).flatMap((value) => {
    if (Array.isArray(value)) {
        return value;
    }

    if (Array.isArray(value?.effects)) {
        return value.effects;
    }

    return [];
});


function findThumbnail(effect) {
    const matching = existingVideoEffects.find(
        (videoEffect) =>
            videoEffect.family === effect.family &&
            String(videoEffect.name || "")
                .toLowerCase()
                .includes(effect.match)
    );

    return matching?.thumbnail || null;
}


function formatFileSize(bytes) {
    if (bytes < 1024 * 1024) {
        return `${(bytes / 1024).toFixed(1)} KB`;
    }

    return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
}


const FAMILIES = [
    "all",
    ...new Set(PHOTO_EFFECTS.map((effect) => effect.family)),
];


export default function PhotoEditor() {
    const [photo, setPhoto] = useState(null);
    const [selectedEffect, setSelectedEffect] = useState("pixel_art");

    const [sourceUrl, setSourceUrl] = useState(null);
    const [resultUrl, setResultUrl] = useState(null);
    const [resultEffectId, setResultEffectId] = useState(null);

    const [processing, setProcessing] = useState(false);
    const [error, setError] = useState("");

    const [search, setSearch] = useState("");
    const [activeFamily, setActiveFamily] = useState("all");
    const [dragging, setDragging] = useState(false);

    const fileInputRef = useRef(null);
    const previewRef = useRef(null);


    useEffect(() => {
        if (!photo) {
            setSourceUrl(null);
            return;
        }

        const url = URL.createObjectURL(photo);
        setSourceUrl(url);

        return () => URL.revokeObjectURL(url);
    }, [photo]);


    useEffect(() => {
        return () => {
            if (resultUrl) {
                URL.revokeObjectURL(resultUrl);
            }
        };
    }, [resultUrl]);


    const currentEffect = PHOTO_EFFECTS.find(
        (effect) => effect.id === selectedEffect
    );

    const filteredEffects = PHOTO_EFFECTS.filter((effect) => {
        const matchesFamily =
            activeFamily === "all" ||
            effect.family === activeFamily;

        const query = search.trim().toLowerCase();

        const matchesSearch =
            effect.name.toLowerCase().includes(query) ||
            (FAMILY_NAMES[effect.family] || "")
                .toLowerCase()
                .includes(query);

        return matchesFamily && matchesSearch;
    });


    function handleFile(file) {
        if (!file || processing) {
            return;
        }

        const supportedTypes = [
            "image/jpeg",
            "image/png",
            "image/webp",
        ];

        if (!supportedTypes.includes(file.type)) {
            setError("Please select a JPG, PNG, or WebP image.");
            return;
        }

        if (file.size > 10 * 1024 * 1024) {
            setError("Maximum photo size is 10 MB.");
            return;
        }

        setPhoto(file);
        setResultUrl(null);
        setResultEffectId(null);
        setError("");
    }


    function handleUpload(event) {
        const file = event.target.files?.[0];

        if (file) {
            handleFile(file);
        }

        // Allow selecting the same file again.
        event.target.value = "";
    }


    function handleDrop(event) {
        event.preventDefault();

        setDragging(false);

        if (processing) {
            return;
        }

        const file = event.dataTransfer.files?.[0];

        if (file) {
            handleFile(file);
        }
    }


    function selectEffect(effectId) {
        if (processing) {
            return;
        }

        setSelectedEffect(effectId);
        setResultUrl(null);
        setResultEffectId(null);
        setError("");
    }


    async function handleApply() {
        if (!photo || processing) {
            return;
        }

        const effectToApply = selectedEffect;

        setProcessing(true);
        setError("");
        setResultUrl(null);
        setResultEffectId(null);

        try {
            const resultBlob = await processPhotoEffect(
                photo,
                effectToApply
            );

            const url = URL.createObjectURL(resultBlob);

            setResultUrl(url);
            setResultEffectId(effectToApply);

            requestAnimationFrame(() => {
                previewRef.current?.scrollIntoView({
                    behavior: "smooth",
                    block: "start",
                });
            });

        } catch (err) {
            setError(
                err.message || "Failed to process image."
            );
        } finally {
            setProcessing(false);
        }
    }


    return (
        <div className="photo-editor">
            <div className="photo-editor__inner">

                {/* HERO */}
                <section className="photo-hero">
                    <div className="photo-hero__eyebrow">
                        <span className="photo-hero__dot" />
                        PHOTO WORKSPACE
                    </div>

                    <h1>
                        Your photos,{" "}
                        <span>reimagined.</span>
                    </h1>

                    <p>
                        From cinematic colors to digital art.
                        Upload a photo, explore creative styles,
                        and transform it in a click.
                    </p>

                    <div className="photo-hero__badges">
                        <span>
                            <strong>{PHOTO_EFFECTS.length}</strong>
                            {" "}Creative effects
                        </span>
                        <span>JPG, PNG & WebP</span>
                        <span>High-quality JPG export</span>
                    </div>
                </section>


                {/* WORKSPACE */}
                <section
                    className="photo-workspace"
                    ref={previewRef}
                >
                    <div className="photo-workspace__heading">
                        <div>
                            <span className="photo-section-kicker">
                                YOUR CANVAS
                            </span>
                            <h2>Editing workspace</h2>
                            <p>
                                Your original and transformed photo,
                                side by side.
                            </p>
                        </div>

                        <span className="photo-workspace__status">
                            <span />
                            {photo ? "Photo loaded" : "Ready to create"}
                        </span>
                    </div>

                    <div className="photo-workspace__grid">

                        {/* ORIGINAL */}
                        <article className="photo-panel">
                            <div className="photo-panel__header">
                                <div className="photo-panel__title">
                                    <span className="photo-panel__number">
                                        01
                                    </span>
                                    <div>
                                        <h3>Original photo</h3>
                                        <p>Your source image</p>
                                    </div>
                                </div>

                                {photo && (
                                    <span className="photo-panel__tag">
                                        ORIGINAL
                                    </span>
                                )}
                            </div>

                            <div
                                className={
                                    "photo-upload-zone" +
                                    (dragging
                                        ? " photo-upload-zone--dragging"
                                        : "") +
                                    (sourceUrl
                                        ? " photo-upload-zone--filled"
                                        : "")
                                }
                                onDragOver={(event) => {
                                    event.preventDefault();
                                    setDragging(true);
                                }}
                                onDragLeave={() => setDragging(false)}
                                onDrop={handleDrop}
                            >
                                {sourceUrl ? (
                                    <img
                                        src={sourceUrl}
                                        alt="Original uploaded photograph"
                                        className="photo-upload-zone__image"
                                    />
                                ) : (
                                    <div className="photo-upload-zone__empty">
                                        <div className="photo-upload-zone__icon">
                                            <svg
                                                viewBox="0 0 24 24"
                                                fill="none"
                                                stroke="currentColor"
                                                strokeWidth="1.5"
                                                strokeLinecap="round"
                                                strokeLinejoin="round"
                                                aria-hidden="true"
                                            >
                                                <path d="M12 16V4" />
                                                <path d="m7 9 5-5 5 5" />
                                                <path d="M4 16v3a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-3" />
                                            </svg>
                                        </div>

                                        <strong>
                                            Drop your photo here
                                        </strong>

                                        <p>
                                            Drag and drop, or use
                                            the button below.
                                        </p>
                                    </div>
                                )}
                            </div>

                            <input
                                ref={fileInputRef}
                                type="file"
                                accept="image/jpeg,image/png,image/webp"
                                onChange={handleUpload}
                                className="photo-file-input"
                                disabled={processing}
                                aria-label="Upload photograph"
                            />

                            <div className="photo-upload-actions">
                                <button
                                    type="button"
                                    className="photo-button photo-button--secondary"
                                    onClick={() =>
                                        fileInputRef.current?.click()
                                    }
                                    disabled={processing}
                                >
                                    <svg
                                        viewBox="0 0 24 24"
                                        fill="none"
                                        stroke="currentColor"
                                        strokeWidth="2"
                                        strokeLinecap="round"
                                        strokeLinejoin="round"
                                        aria-hidden="true"
                                    >
                                        <path d="M12 16V4" />
                                        <path d="m7 9 5-5 5 5" />
                                        <path d="M4 16v3a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-3" />
                                    </svg>

                                    {photo ? "Change photo" : "Upload photo"}
                                </button>

                                <span>Max. 10 MB</span>
                            </div>

                            {photo && (
                                <div className="photo-file-details">
                                    <span title={photo.name}>
                                        {photo.name}
                                    </span>
                                    <small>
                                        {formatFileSize(photo.size)}
                                    </small>
                                </div>
                            )}
                        </article>


                        {/* PROCESSED */}
                        <article className="photo-panel">
                            <div className="photo-panel__header">
                                <div className="photo-panel__title">
                                    <span className="photo-panel__number">
                                        02
                                    </span>
                                    <div>
                                        <h3>Processed photo</h3>
                                        <p>Your creative result</p>
                                    </div>
                                </div>

                                {resultUrl && (
                                    <span className="photo-panel__tag photo-panel__tag--success">
                                        READY
                                    </span>
                                )}
                            </div>

                            <div className="photo-result-zone">
                                {processing ? (
                                    <div
                                        className="photo-result-zone__empty"
                                        role="status"
                                    >
                                        <span className="photo-spinner" />
                                        <strong>
                                            Creating your effect
                                        </strong>
                                        <p>
                                            Processing your photograph...
                                        </p>
                                    </div>
                                ) : resultUrl ? (
                                    <img
                                        src={resultUrl}
                                        alt="Processed photograph"
                                        className="photo-result-zone__image"
                                    />
                                ) : (
                                    <div className="photo-result-zone__empty">
                                        <div className="photo-result-zone__symbol">
                                            <svg
                                                viewBox="0 0 24 24"
                                                fill="none"
                                                stroke="currentColor"
                                                strokeWidth="1.5"
                                                strokeLinecap="round"
                                                strokeLinejoin="round"
                                                aria-hidden="true"
                                            >
                                                <rect x="3" y="3" width="18" height="18" rx="3" />
                                                <path d="m3 17 5-5 4 4 3-3 6 6" />
                                                <circle cx="8.5" cy="8.5" r="1.5" />
                                            </svg>
                                        </div>

                                        <strong>
                                            Your result appears here
                                        </strong>

                                        <p>
                                            Select an effect below
                                            and click Apply Effect.
                                        </p>
                                    </div>
                                )}
                            </div>

                            <div className="photo-result-actions">
                                {resultUrl ? (
                                    <a
                                        className="photo-button photo-button--primary"
                                        href={resultUrl}
                                        download={`${resultEffectId || selectedEffect}.jpg`}
                                    >
                                        <svg
                                            viewBox="0 0 24 24"
                                            fill="none"
                                            stroke="currentColor"
                                            strokeWidth="2"
                                            strokeLinecap="round"
                                            strokeLinejoin="round"
                                            aria-hidden="true"
                                        >
                                            <path d="M12 3v12" />
                                            <path d="m7 10 5 5 5-5" />
                                            <path d="M4 17v3h16v-3" />
                                        </svg>
                                        Download photo
                                    </a>
                                ) : (
                                    <span className="photo-result-actions__hint">
                                        Your finished image will be
                                        available for download here.
                                    </span>
                                )}
                            </div>
                        </article>
                    </div>
                </section>


                {/* EFFECTS */}
                <section className="photo-library">
                    <div className="photo-library__heading">
                        <div>
                            <span className="photo-section-kicker">
                                FIND YOUR STYLE
                            </span>
                            <h2>Explore photo effects</h2>
                            <p>
                                Choose a look that fits your photograph.
                            </p>
                        </div>

                        <span className="photo-library__count">
                            {filteredEffects.length} / {PHOTO_EFFECTS.length} effects
                        </span>
                    </div>

                    <div className="photo-library__toolbar">
                        <label className="photo-library__search">
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
                                placeholder="Search photo effects..."
                                aria-label="Search photo effects"
                            />
                        </label>
                    </div>

                    <div
                        className="photo-library__filters"
                        aria-label="Filter by effect family"
                    >
                        {FAMILIES.map((family) => {
                            const selected = activeFamily === family;

                            return (
                                <button
                                    key={family}
                                    type="button"
                                    className={
                                        "photo-filter-chip" +
                                        (selected
                                            ? " photo-filter-chip--active"
                                            : "")
                                    }
                                    aria-pressed={selected}
                                    onClick={() =>
                                        setActiveFamily(family)
                                    }
                                >
                                    {family === "all"
                                        ? "All effects"
                                        : FAMILY_NAMES[family] || family}
                                </button>
                            );
                        })}
                    </div>

                    <div className="photo-effects-grid">
                        {filteredEffects.map((effect) => {
                            const selected =
                                selectedEffect === effect.id;

                            const thumbnail = findThumbnail(effect);

                            return (
                                <button
                                    type="button"
                                    key={effect.id}
                                    aria-pressed={selected}
                                    disabled={processing}
                                    onClick={() =>
                                        selectEffect(effect.id)
                                    }
                                    className={
                                        "photo-effect-card" +
                                        (selected
                                            ? " photo-effect-card--selected"
                                            : "")
                                    }
                                >
                                    <div className="photo-effect-card__image">
                                        {thumbnail ? (
                                            <img
                                                src={thumbnail}
                                                alt={effect.name}
                                            />
                                        ) : (
                                            <div className="photo-effect-card__placeholder">
                                                <span>
                                                    {effect.name}
                                                </span>
                                            </div>
                                        )}

                                        {selected && (
                                            <span className="photo-effect-card__badge">
                                                Selected
                                            </span>
                                        )}
                                    </div>

                                    <div className="photo-effect-card__name">
                                        {effect.name}
                                    </div>
                                </button>
                            );
                        })}
                    </div>

                    {filteredEffects.length === 0 && (
                        <div className="photo-library__empty">
                            <strong>No matching effects</strong>
                            <p>
                                Try another search or select
                                a different category.
                            </p>
                            <button
                                type="button"
                                onClick={() => {
                                    setSearch("");
                                    setActiveFamily("all");
                                }}
                            >
                                Show all effects
                            </button>
                        </div>
                    )}

                    <div className="photo-apply-bar">
                        <div className="photo-apply-bar__selection">
                            <span>SELECTED EFFECT</span>
                            <strong>
                                {currentEffect?.name || "Choose an effect"}
                            </strong>
                            <small>
                                {currentEffect
                                    ? FAMILY_NAMES[currentEffect.family]
                                    : ""}
                            </small>
                        </div>

                        <button
                            type="button"
                            onClick={handleApply}
                            disabled={!photo || processing}
                            className="photo-button photo-button--primary photo-apply-bar__button"
                        >
                            {processing ? (
                                <>
                                    <span className="photo-button__spinner" />
                                    Processing...
                                </>
                            ) : (
                                <>
                                    Apply Effect
                                    <svg
                                        viewBox="0 0 24 24"
                                        fill="none"
                                        stroke="currentColor"
                                        strokeWidth="2"
                                        strokeLinecap="round"
                                        strokeLinejoin="round"
                                        aria-hidden="true"
                                    >
                                        <path d="M5 12h14" />
                                        <path d="m13 6 6 6-6 6" />
                                    </svg>
                                </>
                            )}
                        </button>
                    </div>

                    {error && (
                        <div className="photo-editor__error" role="alert">
                            {error}
                        </div>
                    )}
                </section>
            </div>
        </div>
    );
}
