PHOTO_EFFECTS = {
    "pixel_art": {
        "name": "Pixel Art",
        "family": "artistic",
        "config": {
            "pixel_size": 12,
            "color_bits": 5,
        },
    },

    "mosaic": {
        "name": "Mosaic",
        "family": "artistic",
        "config": {
            "tile_size": 18,
            "grout_width": 2,
        },
    },

    "comic_book": {
        "name": "Comic Book",
        "family": "retro",
        "config": {
            "color_bits": 4,
            "edge_threshold": 65,
        },
    },

    "classic_noir": {
        "name": "Classic Noir",
        "family": "noir",
        "config": {},
    },

    "vintage_sepia": {
        "name": "Vintage Sepia",
        "family": "vintage",
        "config": {},
    },

    "cyberpunk_neon": {
        "name": "Cyberpunk Neon",
        "family": "futuristic",
        "config": {},
    },
}
PHOTO_EFFECTS.update({
    effect_id: {
        "name": name,
        "family": family,
        "config": {},
    }
    for effect_id, name, family in [
        ("abyss", "Abyss", "underwater"),
        ("deep_ocean", "Deep Ocean", "underwater"),
        ("faded_memories", "Faded Memories", "vintage"),
        ("wireframe_reality", "Wireframe Reality", "futuristic"),
        ("synthwave", "Synthwave", "retro"),
        ("camcorder_90s", "90s Camcorder", "retro"),
        ("golden_hour_cinema", "Golden Hour Cinema", "cinematic"),
        ("dark_moody", "Dark & Moody", "cinematic"),
        ("midnight_blue", "Midnight Blue", "noir"),
        ("evidence_triptych", "Evidence Triptych", "noir"),
        ("chroma_bleed", "Chroma Bleed", "vhs"),
        ("window_light", "Window Light", "dreamy"),
        ("wildflower", "Wildflower", "dreamy"),
        ("miniature_world", "Miniature World", "travel"),
        ("pencil_sketch", "Pencil Sketch", "artistic"),
        ("oil_painting", "Oil Painting", "artistic"),
        ("watercolor", "Watercolor", "artistic"),
        ("photo_stack", "Photo Stack", "creative_motion"),
    ]
})