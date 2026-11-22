import { useEffect, useState } from "react";

import * as videoEffectCatalog from "../data/effects";

import { processPhotoEffect } from "../services/photoApi";


const PHOTO_EFFECTS = [
    {
        id: "pixel_art",
        name: "Pixel Art",
        family: "artistic",
        match: "pixel art",
    },
    {
        id: "mosaic",
        name: "Mosaic",
        family: "artistic",
        match: "mosaic",
    },
    {
        id: "comic_book",
        name: "Comic Book",
        family: "retro",
        match: "comic book",
    },
    {
        id: "classic_noir",
        name: "Classic Noir",
        family: "noir",
        match: "classic noir",
    },
    {
        id: "vintage_sepia",
        name: "Vintage Sepia",
        family: "vintage",
        match: "sepia",
    },
    {
        id: "cyberpunk_neon",
        name: "Cyberpunk Neon",
        family: "futuristic",
        match: "cyberpunk neon",
    },
];

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


const styles = {
    container: {
        maxWidth: 1150,
        margin: "0 auto",
        padding: 24,
        color: "#f3f4f6",
    },

    panel: {
        background: "#171b26",
        border: "1px solid #363b49",
        borderRadius: 14,
        padding: 20,
        marginBottom: 22,
    },

    grid: {
        display: "grid",
        gridTemplateColumns: "repeat(auto-fit, minmax(160px, 1fr))",
        gap: 14,
        marginTop: 18,
        marginBottom: 24,
    },

    image: {
        display: "block",
        width: "100%",
        maxHeight: 450,
        objectFit: "contain",
        borderRadius: 10,
    },

    button: {
        padding: "12px 22px",
        border: "none",
        borderRadius: 9,
        background: "#6759e8",
        color: "white",
        fontWeight: 600,
        cursor: "pointer",
    },
};


export default function PhotoEditor() {
    const [photo, setPhoto] = useState(null);

    const [selectedEffect, setSelectedEffect] = useState(
        "pixel_art"
    );

    const [sourceUrl, setSourceUrl] = useState(null);
    const [resultUrl, setResultUrl] = useState(null);

    const [processing, setProcessing] = useState(false);
    const [error, setError] = useState("");


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


    function handleUpload(event) {
        const file = event.target.files?.[0];

        if (!file) {
            return;
        }

        if (!["image/jpeg", "image/png", "image/webp"].includes(
            file.type
        )) {
            setError("Please select a JPG, PNG or WebP image.");
            return;
        }

        if (file.size > 10 * 1024 * 1024) {
            setError("Maximum photo size is 10 MB.");
            return;
        }

        setPhoto(file);
        setResultUrl(null);
        setError("");
    }


    function selectEffect(effectId) {
        setSelectedEffect(effectId);
        setResultUrl(null);
        setError("");
    }


    async function handleApply(event) {
        event.preventDefault();

        if (!photo || processing) {
            return;
        }

        setProcessing(true);
        setError("");
        setResultUrl(null);

        try {
            const resultBlob = await processPhotoEffect(
                photo,
                selectedEffect
            );

            const url = URL.createObjectURL(resultBlob);

            setResultUrl(url);

        } catch (err) {
            setError(
                err.message || "Failed to process image."
            );

        } finally {
            setProcessing(false);
        }
    }


    return (
        <div style={styles.container}>
            <h1>Photo Editor</h1>

            <p style={{ color: "#aeb7c8" }}>
                Apply creative effects to your photographs.
            </p>

            <form onSubmit={handleApply}>
                <section style={styles.panel}>
                    <h2>1. Upload a Photo</h2>

                    <input
                        type="file"
                        accept="image/jpeg,image/png,image/webp"
                        onChange={handleUpload}
                        style={{ marginTop: 12 }}
                    />

                    {photo && (
                        <p style={{ color: "#aeb7c8" }}>
                            Selected: {photo.name}
                        </p>
                    )}
                </section>


                <section style={styles.panel}>
                    <h2>2. Choose an Effect</h2>

                    <div style={styles.grid}>
                        {PHOTO_EFFECTS.map((effect) => {
                            const selected =
                                selectedEffect === effect.id;

                            const thumbnail =
                                findThumbnail(effect);

                            return (
                                <button
                                    type="button"
                                    key={effect.id}
                                    aria-pressed={selected}
                                    onClick={() =>
                                        selectEffect(effect.id)
                                    }
                                    style={{
                                        background: "#232838",
                                        border: selected
                                            ? "2px solid #8f86ff"
                                            : "2px solid #454a58",
                                        borderRadius: 12,
                                        padding: 8,
                                        color: "#ffffff",
                                        cursor: "pointer",
                                        textAlign: "left",
                                    }}
                                >
                                    {thumbnail ? (
                                        <img
                                            src={thumbnail}
                                            alt={effect.name}
                                            style={{
                                                width: "100%",
                                                aspectRatio: "16 / 9",
                                                objectFit: "cover",
                                                borderRadius: 7,
                                            }}
                                        />
                                    ) : (
                                        <div
                                            style={{
                                                width: "100%",
                                                aspectRatio: "16 / 9",
                                                borderRadius: 7,
                                                background:
                                                    "linear-gradient(135deg, #414b76, #9669a4)",
                                            }}
                                        />
                                    )}

                                    <div
                                        style={{
                                            marginTop: 8,
                                            fontWeight: 600,
                                        }}
                                    >
                                        {effect.name}
                                    </div>
                                </button>
                            );
                        })}
                    </div>

                    <button
                        type="submit"
                        disabled={!photo || processing}
                        style={{
                            ...styles.button,
                            opacity:
                                !photo || processing ? 0.5 : 1,
                        }}
                    >
                        {processing
                            ? "Processing..."
                            : "Apply Photo Effect"}
                    </button>

                    {error && (
                        <p
                            role="alert"
                            style={{ color: "#ff9292" }}
                        >
                            {error}
                        </p>
                    )}
                </section>
            </form>


            {sourceUrl && (
                <section style={styles.panel}>
                    <h2>3. Photo Preview</h2>

                    <div
                        style={{
                            display: "grid",
                            gridTemplateColumns:
                                "repeat(auto-fit, minmax(260px, 1fr))",
                            gap: 20,
                        }}
                    >
                        <div>
                            <h3>Original</h3>

                            <img
                                src={sourceUrl}
                                alt="Original upload"
                                style={styles.image}
                            />
                        </div>

                        {resultUrl && (
                            <div>
                                <h3>Processed</h3>

                                <img
                                    src={resultUrl}
                                    alt="Processed photograph"
                                    style={styles.image}
                                />
                            </div>
                        )}
                    </div>

                    {resultUrl && (
                        <a
                            href={resultUrl}
                            download={`${selectedEffect}.jpg`}
                            style={{
                                ...styles.button,
                                display: "inline-block",
                                textDecoration: "none",
                                marginTop: 24,
                            }}
                        >
                            Download Photo
                        </a>
                    )}
                </section>
            )}
        </div>
    );
}