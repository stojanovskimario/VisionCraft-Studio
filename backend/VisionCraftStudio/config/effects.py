
EFFECTS = {
    "underwater": {
        "id": "underwater",
        "name": "Underwater",
        "family": "underwater",
        "description": "A balanced underwater atmosphere with turquoise tones, gentle water movement and floating bubbles.",
        "config": {
            "red": 0.88,
            "green": 1.04,
            "blue": 1.18,
            "contrast": 0.94,
            "distortion": 2.5,
            "bubbles": True,
            "light_rays": True,
            "soft_focus": 1.2
        }
    },

    "deep_ocean": {
        "id": "deep_ocean",
        "name": "Deep Ocean",
        "family": "underwater",
        "description": "A mysterious deep-ocean atmosphere with darker blue tones and subtle lighting.",
        "config": {
            "red": 0.65,
            "green": 0.85,
            "blue": 1.30,
            "contrast": 1.12,
            "distortion": 1.8,
            "bubbles": True,
            "light_rays": False,
            "soft_focus": 1.5
        }
    },

    "bioluminescent_lagoon": {
        "id": "bioluminescent_lagoon",
        "name": "Bioluminescent Lagoon",
        "family": "underwater",
        "description": "A mysterious nighttime underwater atmosphere with glowing turquoise and emerald particles, deep navy tones and subtle violet illumination.",
        "config": {
            "effect_type": "bioluminescent",

            "red": 0.52,
            "green": 0.82,
            "blue": 1.18,

            "contrast": 1.08,
            "brightness": 0.72,

            "glow_threshold": 75,
            "glow_range": 100,
            "glow_radius": 12,
            "glow_color": [15, 230, 175],
            "glow_intensity": 1.0,

            "violet_color": [125, 45, 210],
            "violet_intensity": 0.30,

            "particle_count": 35,
            "particle_speed": 18,
            "particle_glow_radius": 5
        }
    },


    "arctic_water": {
        "id": "arctic_water",
        "name": "Arctic Water",
        "family": "underwater",
        "description": "A cold, icy underwater appearance with crisp blue tones.",
        "config": {
            "red": 0.72,
            "green": 0.94,
            "blue": 1.28,
            "contrast": 1.08,
            "distortion": 1.2,
            "bubbles": False,
            "light_rays": True,
            "soft_focus": 0.6
        }
    },

    "abyss": {
        "id": "abyss",
        "name": "Abyss",
        "family": "underwater",
        "description": "An atmospheric dark abyss with deep shadows and minimal illumination.",
        "config": {
            "red": 0.48,
            "green": 0.68,
            "blue": 1.15,
            "contrast": 1.18,
            "distortion": 1.0,
            "bubbles": False,
            "light_rays": False,
            "soft_focus": 1.8
        }
    },

    "coral_reef": {
        "id": "coral_reef",
        "name": "Coral Reef",
        "family": "underwater",
        "description": "A vibrant coral reef appearance with enhanced colors and bright underwater lighting.",
        "config": {
            "red": 1.12,
            "green": 1.08,
            "blue": 1.16,
            "contrast": 1.04,
            "distortion": 1.8,
            "bubbles": True,
            "light_rays": True,
            "soft_focus": 0.7
        }
    },
    #VINTAGE
    "vintage_classic": {
        "id": "vintage_classic",
        "name": "Classic Vintage",
        "family": "vintage",
        "description": "A timeless black and white vintage film appearance.",
        "config": {
            "color_mode": "grayscale",
            "contrast": 1.05,
            "brightness": 1.0,
            "film_grain": 3,
            "vignette": 2,
            "rotation": {
                "angle": 90,
                "start_percent": 20,
                "rotate_in_percent": 5,
                "hold_percent": 15,
                "rotate_out_percent": 5,
            },
            "speed": {
                "factor": 1.25,
                "start_percent": 55,
                "end_percent": 75
            }
        }
    },

    "vintage_super8": {
        "id": "vintage_super8",
        "name": "70s Super 8",
        "family": "vintage",
        "description": "Warm colors inspired by old Super 8 home movies.",
        "config": {
            "color_mode": "warm",
            "contrast": 0.95,
            "brightness": 1.05,
            "film_grain": 6,
            "vignette": 3,
            "flicker": 3,
            "rotation": {
                "angle": 45,
                "start_percent": 20,
                "in_percent": 5,
                "hold_percent": 5,
                "out_percent": 5
            },
            "speed": {
                "factor": 1.5,
                "start_percent": 55,
                "end_percent": 75
            }
        }
    },

    "vintage_faded": {
        "id": "vintage_faded",
        "name": "Faded Memories",
        "family": "vintage",
        "description": "Soft, washed-out colors with a nostalgic appearance.",
        "config": {
            "color_mode": "faded",
            "contrast": 0.80,
            "brightness": 1.08,
            "film_grain": 2,
            "vignette": 1,
            "soft_focus": 1.5,
            "rotation": {
                "angle": 0,
                "start_percent": 20,
                "in_percent": 5,
                "hold_percent": 5,
                "out_percent": 5
            },
            "speed": {
                "factor": 1.4,
                "start_percent": 55,
                "end_percent": 90
            }
        }
    },

    "vintage_sepia": {
        "id": "vintage_sepia",
        "name": "Sepia",
        "family": "vintage",
        "description": "Classic brown-toned old photograph styling.",
        "config": {
            "color_mode": "sepia",
            "contrast": 0.95,
            "brightness": 1.0,
            "film_grain": 3,
            "vignette": 4,
            "rotation": {
                "angle": 90,
                "start_percent": 40,
                "rotate_in_percent": 5,
                "hold_percent": 25,
                "rotate_out_percent": 5,
            },
            "speed": {
                "factor": 1.25,
                "start_percent": 65,
                "end_percent": 85
            }
        }
    },

    "vintage_old_reel": {
        "id": "vintage_old_reel",
        "name": "Old Film Reel",
        "family": "vintage",
        "description": "Aged black and white footage with authentic film imperfections.",
        "config": {
            "color_mode": "grayscale",
            "contrast": 1.05,
            "brightness": 1.0,
            "film_grain": 7,
            "vignette": 3,
            "flicker": 5,
            "dust": 6,
            "scratches": 5,
            "rotation": {
                "angle": 90,
                "start_percent": 30,
                "rotate_in_percent": 5,
                "hold_percent": 35,
                "rotate_out_percent": 5,
            },
            "speed": {
                "factor": 1.5,
                "start_percent": 55,
                "end_percent": 75
            }
        }
    },

    "vintage_golden": {
        "id": "vintage_golden",
        "name": "Golden Light Leak",
        "family": "vintage",
        "description": "Warm golden highlights with a nostalgic film appearance.",
        "config": {
            "color_mode": "golden",
            "contrast": 0.95,
            "brightness": 1.08,
            "film_grain": 3,
            "vignette": 2,
            "light_leak": 5,
            "rotation": {
                "angle": 45,
                "start_percent": 40,
                "in_percent": 5,
                "hold_percent": 10,
                "out_percent": 5
            },
            "speed": {
                "factor": 1.25,
                "start_percent": 10,
                "end_percent": 30
            }
        }
    },
    # FUTURISTIC
    "cyberpunk_neon": {
        "id": "cyberpunk_neon",
        "name": "Cyberpunk Neon",
        "family": "futuristic",
        "description": "A vibrant cyberpunk look with cool blue shadows, magenta highlights and a subtle neon glow.",
        "config": {
            "red": 1.08,
            "green": 0.88,
            "blue": 1.20,
            "contrast": 1.12,
            "brightness": 1.02,
            "glow": 0.35,
            "glow_radius": 8,
            "scan_lines": 0,
            "rgb_shift": 2,
            "glitch_intensity": 0
        }
    },

    "hologram": {
        "id": "hologram",
        "name": "Hologram",
        "family": "futuristic",
        "description": "A holographic appearance with cool cyan and purple tones, luminous highlights and subtle horizontal scan lines.",
        "config": {
            "red": 0.88,
            "green": 1.12,
            "blue": 1.25,
            "contrast": 0.96,
            "brightness": 1.08,
            "glow": 0.30,
            "glow_radius": 10,
            "scan_lines": 0.16,
            "rgb_shift": 2,
            "glitch_intensity": 0
        }
    },

    "thermal_vision": {
        "id": "thermal_vision",
        "name": "Thermal Vision",
        "family": "futuristic",
        "description": "Transforms footage into an infrared thermal view with deep purple shadows, red and orange midtones, and bright yellow highlights.",
        "config": {
            "effect_type": "thermal",
            "thermal_contrast": 1.15,
            "thermal_brightness": 1.0,
            "glow": 0.18,
            "glow_radius": 8
        }
    },

    "cybernetic_vision": {
        "id": "cybernetic_vision",
        "name": "Cybernetic Vision",
        "family": "futuristic",
        "description": "A futuristic digital vision effect with bright cyan neon outlines, glowing edges and cool blue cinematic grading.",
        "config": {
            "effect_type": "cybernetic",
            "red": 0.72,
            "green": 0.95,
            "blue": 1.25,
            "contrast": 1.18,
            "brightness": 0.88,
            "edge_threshold": 18,
            "edge_strength": 4.0,
            "edge_color": [25, 220, 255],
            "edge_brightness": 1.5,
            "edge_glow_radius": 5,
            "edge_glow_intensity": 0.9,
            "glow_color": [0, 110, 255],
            "pulse_period": 4.0,
            "pulse_intensity": 0.12,
            "glow": 0.10,
            "glow_radius": 6
        }
    },

    "time_rift": {
        "id": "time_rift",
        "name": "Time Rift",
        "family": "futuristic",
        "description": "A temporal distortion effect with cyan and violet motion echoes trailing behind moving objects.",
        "config": {
            "effect_type": "time_rift",
            "red": 0.92,
            "green": 0.96,
            "blue": 1.12,
            "contrast": 1.08,
            "brightness": 1.0,
            "echo_delays": [0.08, 0.16, 0.24],
            "echo_strengths": [0.38, 0.27, 0.17],
            "motion_threshold": 14,
            "motion_range": 45,
            "motion_blur": 3,
            "pulse_period": 3.5,
            "pulse_intensity": 0.035
        }
    },

    "wireframe": {
        "id": "wireframe",
        "name": "Wireframe Reality",
        "family": "futuristic",
        "description": "A digital simulation aesthetic with glowing violet wireframe outlines, electric pink highlights and a deep purple geometric grid.",
        "config": {
            "effect_type": "wireframe",

            "base_brightness": 0.68,
            "base_saturation": 0.72,

            "base_red": 0.92,
            "base_green": 0.72,
            "base_blue": 1.12,

            "edge_threshold": 22,
            "edge_strength": 3.2,
            "edge_thickness": 3,
            "edge_intensity": 1.15,

            "glow_radius": 7,
            "glow_intensity": 0.75,

            "edge_color": [185, 75, 255],
            "glow_color": [105, 25, 220],
            "highlight_color": [255, 45, 170],

            "highlight_threshold": 110,
            "highlight_intensity": 0.55,

            "grid_spacing": 48,
            "grid_intensity": 0.30,
            "grid_color": [95, 35, 160],

            "pulse_period": 4.0,
            "pulse_intensity": 0.10
        }
    },

    # RETRO

    "analog_memories": {
        "id": "analog_memories",
        "name": "Analog Memories",
        "family": "retro",
        "description": "A nostalgic analog film appearance with warm colors, natural film grain and softly darkened edges.",
        "config": {
            "effect_type": "analog_memories",
            "red": 1.12,
            "green": 0.98,
            "blue": 0.82,
            "contrast": 0.90,
            "grain_intensity": 5,
            "vignette_intensity": 1.0
        }
    },

    "crt_television": {
        "id": "crt_television",
        "name": "CRT Television",
        "family": "retro",
        "description": "An old television display with curved screen distortion, glowing RGB pixels, scanlines and subtle flickering.",
        "config": {
            "effect_type": "crt_television",
            "red": 0.90,
            "green": 1.02,
            "blue": 1.12,
            "contrast": 1.12,
            "curvature": 0.06,
            "scanline_strength": 0.18,
            "rgb_shift": 1,
            "glow_radius": 2,
            "glow_intensity": 0.18,
            "flicker": 0.025
        }
    },

    "camcorder_90s": {
        "id": "camcorder_90s",
        "name": "90s Camcorder",
        "family": "retro",
        "description": "A nostalgic 1990s home-video recording with timestamp overlays, analog noise and characteristic camcorder colors.",
        "config": {
            "effect_type": "camcorder_90s",
            "red": 1.05,
            "green": 1.04,
            "blue": 0.90,
            "contrast": 0.96,
            "warmth": 1.05,
            "green_tint": 1.04,
            "blue_tint": 0.88,
            "color_bleed": 2,
            "noise_intensity": 4,
            "show_timestamp": True
        }
    },

    "y2k_digital": {
        "id": "y2k_digital",
        "name": "Y2K Digital Camera",
        "family": "retro",
        "description": "An early-2000s digital camera aesthetic with cool highlights, boosted contrast, digital noise and soft flash-like brightness.",
        "config": {
            "effect_type": "y2k_digital",
            "red": 0.94,
            "green": 1.02,
            "blue": 1.12,
            "contrast": 1.05,
            "brightness": 1.04,
            "contrast_boost": 1.10,
            "blue_highlights": 1.10,
            "noise_intensity": 3,
            "glow_radius": 3,
            "glow_intensity": 0.20
        }
    },

    "synthwave": {
        "id": "synthwave",
        "name": "Synthwave",
        "family": "retro",
        "description": "A vibrant 1980s-inspired neon appearance with purple shadows, magenta highlights and luminous colors.",
        "config": {
            "effect_type": "synthwave",
            "red": 1.15,
            "green": 0.78,
            "blue": 1.30,
            "contrast": 1.12,
            "glow_radius": 8,
            "glow_intensity": 0.30,
            "pulse_intensity": 0.06
        }
    },

    "comic_book": {
        "id": "comic_book",
        "name": "Comic Book",
        "family": "retro",
        "description": "A bold comic-book illustration with vibrant colors, thick ink outlines, reduced color palettes and halftone shading.",
        "config": {
            "effect_type": "comic_book",
            "red": 1.08,
            "green": 1.02,
            "blue": 1.05,
            "contrast": 1.15,
            "saturation": 1.25,
            "smoothing": 0.6,
            "palette_colors": 12,
            "edge_threshold": 45,
            "outline_strength": 0.85,
            "dot_size": 6,
            "dot_intensity": 0.25
        }
    },

    # CINEMATIC

    "hollywood_blockbuster": {
        "id": "hollywood_blockbuster",
        "name": "Hollywood Blockbuster",
        "family": "cinematic",
        "description": "A polished cinematic look with teal shadows, warm highlights, strong contrast and subtle vignette.",
        "config": {
            "effect_type": "hollywood_blockbuster",
            "red": 1.02,
            "green": 1.0,
            "blue": 1.02,
            "contrast": 1.14,
            "brightness": 1.0,
            "saturation": 1.08,
            "split_strength": 0.9,
            "vignette": 0.16,
        },
    },

    "dark_moody": {
        "id": "dark_moody",
        "name": "Dark & Moody",
        "family": "cinematic",
        "description": "A mysterious film appearance with cool shadows, muted colors, deep contrast and fine grain.",
        "config": {
            "effect_type": "dark_moody",
            "red": 0.96,
            "green": 0.98,
            "blue": 1.04,
            "contrast": 1.18,
            "brightness": 0.91,
            "saturation": 0.70,
            "split_strength": 0.85,
            "vignette": 0.26,
            "grain": 3.0,
        },
    },

    "golden_hour": {
        "id": "golden_hour",
        "name": "Golden Hour Cinema",
        "family": "cinematic",
        "description": "Warm golden tones, glowing highlights and soft cinematic bloom inspired by sunset lighting.",
        "config": {
            "effect_type": "golden_hour",
            "red": 1.10,
            "green": 1.04,
            "blue": 0.90,
            "contrast": 0.98,
            "brightness": 1.04,
            "saturation": 1.12,
            "split_strength": 0.9,
            "bloom_radius": 10,
            "bloom_intensity": 0.35,
            "bloom_threshold": 155,
        },
    },

    "anamorphic": {
        "id": "anamorphic",
        "name": "Anamorphic Cinema",
        "family": "cinematic",
        "description": "A widescreen cinematic appearance with letterbox bars, cool highlights, bloom and horizontal lens flares.",
        "config": {
            "effect_type": "anamorphic",
            "red": 0.96,
            "green": 1.0,
            "blue": 1.10,
            "contrast": 1.10,
            "brightness": 1.0,
            "split_strength": 0.65,
            "bloom_radius": 9,
            "bloom_intensity": 0.30,
            "flare_strength": 0.28,
            "flare_threshold": 225,
            "letterbox": True,
            "bar_ratio": 0.12,
        },
    },

    "indie_film": {
        "id": "indie_film",
        "name": "Indie Film",
        "family": "cinematic",
        "description": "A natural independent-film aesthetic with soft contrast, faded blacks, pastel colors and fine grain.",
        "config": {
            "effect_type": "indie_film",
            "red": 1.04,
            "green": 1.02,
            "blue": 0.98,
            "contrast": 0.90,
            "brightness": 1.02,
            "saturation": 0.82,
            "black_lift": 12,
            "split_strength": 0.55,
            "grain": 2.5,
        },
    },

    "technicolor_pop": {
        "id": "technicolor_pop",
        "name": "Technicolor Pop",
        "family": "cinematic",
        "description": (
            "A vivid classic-cinema look with rich colors, clean whites, "
            "and punchy contrast."
        ),
        "config": {
            "effect_type": "technicolor_pop",
            "red_boost": 0.36,
            "orange_boost": 0.06,
            "green_boost": 0.30,
            "blue_boost": 0.32,
            "contrast": 1.06,
        },
    },

    # NOIR

    "classic_noir": {
        "id": "classic_noir",
        "name": "Classic Noir",
        "family": "noir",
        "description": "Black-and-white footage with gradually increasing contrast and visible film grain.",
        "config": {
            "effect_type": "classic_noir",
            "contrast": 1.20,
            "contrast_ramp_seconds": 3.0,
            "vignette_strength": 0.25,
            "vignette_start_seconds": 2.0,
            "vignette_end_seconds": 4.0,
            "grain_strength": 8.0,
        },
    },
    "focus_pull": {
        "id": "focus_pull",
        "name": "Focus Pull",
        "family": "noir",
        "description": "A band of sharp focus sweeps across softly blurred black-and-white footage.",
        "config": {
            "effect_type": "focus_pull",
            "sweep_seconds": 6.0,
            "focus_width": 0.30,
            "feather_width": 0.18,
            "blur_radius": 9.0,
        },
    },
    "staccato_noir": {
        "id": "staccato_noir",
        "name": "Staccato Noir",
        "family": "noir",
        "description": (
            "Black-and-white footage with deliberately stepped motion "
            "and unchanged playback duration and audio."
        ),
        "config": {
            "effect_type": "staccato_noir",
            "motion_fps": 8.0,
            "contrast": 1.05,
        },
    },
    "midnight_blue": {
        "id": "midnight_blue",
        "name": "Midnight Blue",
        "family": "noir",
        "description": "A near-monochrome look with steel-blue shadows and neutral highlights.",
        "config": {
            "effect_type": "midnight_blue",
            "contrast": 1.10,
            "tint_strength": 1.0,
        },
    },
    "evidence_triptych": {
        "id": "evidence_triptych",
        "name": "Evidence Triptych",
        "family": "noir",
        "description": "A three-panel black-and-white layout with the full shot framed by two close-ups.",
        "config": {
            "effect_type": "evidence_triptych",
            "center_share": 0.50,
            "gutter_ratio": 0.012,
            "background_level": 22,
        },
    },
    "red_evidence": {
        "id": "red_evidence",
        "name": "Red Evidence",
        "family": "noir",
        "description": "Keeps reds from the original footage visible while turning the rest black and white.",
        "config": {
            "effect_type": "red_evidence",
            "red_hue_width_degrees": 31.0,
            "minimum_saturation": 0.20,
        },
    },

    # VHS

    "classic_vhs": {
        "id": "classic_vhs",
        "name": "Classic VHS",
        "family": "vhs",
        "description": "Faded tape colors, horizontal scanlines, a brief RGB glitch, and light analog noise.",
        "config": {
            "effect_type": "classic_vhs",
            "saturation": 0.75,
            "rgb_gain": [1.08, 1.02, 0.92],
            "contrast": 0.90,
            "scanline_stride": 3,
            "scanline_gain": 0.82,
            "glitch_start_seconds": 2.0,
            "glitch_end_seconds": 3.0,
            "glitch_intensity": 5,
            "slice_probability": 0.25,
            "noise_strength": 4.0,
        },
    },
    "vhs_tracking_error": {
        "id": "vhs_tracking_error",
        "name": "Tracking Error",
        "family": "vhs",
        "description": "A moving tracking band briefly tears sections of the picture sideways.",
        "config": {
            "effect_type": "vhs_tracking_error",
            "saturation": 0.82,
            "rgb_gain": [1.02, 1.00, 0.96],
            "contrast": 0.96,
            "band_ratio": 0.22,
            "shift_ratio": 0.055,
            "offset_seconds": 0.7,
            "interval_seconds": 4.5,
            "burst_seconds": 1.1,
        },
    },
    "vhs_chroma_bleed": {
        "id": "vhs_chroma_bleed",
        "name": "Chroma Bleed",
        "family": "vhs",
        "description": "Leaves a sideways color trail while keeping brightness detail sharp.",
        "config": {
            "effect_type": "vhs_chroma_bleed",
            "bleed_ratio": 0.026,
            "bleed_strength": 0.88,
            "saturation": 1.42,
        },
    },
    "vhs_long_play": {
        "id": "vhs_long_play",
        "name": "Long Play",
        "family": "vhs",
        "description": "Softens fine detail and washes out colors to mimic a low-quality tape recording.",
        "config": {
            "effect_type": "vhs_long_play",
            "saturation": 0.58,
            "rgb_gain": [1.04, 1.01, 0.94],
            "contrast": 0.84,
            "detail_short_side": 144,
            "horizontal_detail": 0.72,
        },
    },
    "vhs_vertical_hold": {
        "id": "vhs_vertical_hold",
        "name": "Vertical Hold",
        "family": "vhs",
        "description": "Briefly rolls the entire picture vertically before it settles back into place.",
        "config": {
            "effect_type": "vhs_vertical_hold",
            "saturation": 0.90,
            "rgb_gain": [0.98, 1.02, 1.04],
            "contrast": 0.98,
            "offset_seconds": 1.2,
            "interval_seconds": 5.5,
            "roll_seconds": 0.9,
            "seam_ratio": 0.028,
            "seam_strength": 0.88,
        },
    },
    "vhs_tape_leader": {
        "id": "vhs_tape_leader",
        "name": "Tape Leader",
        "family": "vhs",
        "description": "Opens with a short color-bar screen that fades into faded videotape footage.",
        "config": {
            "effect_type": "vhs_tape_leader",
            "saturation": 0.80,
            "rgb_gain": [1.07, 1.02, 0.93],
            "contrast": 0.92,
            "leader_seconds": 1.1,
            "fade_seconds": 0.35,
            "max_clip_share": 0.30,
        },
    },

    # DREAMY

    "dreamy_lucid": {
        "id": "dreamy_lucid",
        "name": "Lucid Dream",
        "family": "dreamy",
        "description": "Lifted midtones, clearer detail, and richer natural colors without a tint.",
        "config": {
            "effect_type": "dreamy_grade",
            "tone_curve": [0, 0.115, 0.34, 0.62, 0.83, 0.952, 1],
            "saturation": 1.09,
            "vibrance": 0.28,
            "clarity": 0.52,
        },
    },
    "dreamy_peach_daylight": {
        "id": "dreamy_peach_daylight",
        "name": "Peach Daylight",
        "family": "dreamy",
        "description": "Peach-and-cream highlights with nearly neutral shadows.",
        "config": {
            "effect_type": "dreamy_grade",
            "tone_curve": [0, 0.14, 0.35, 0.615, 0.83, 0.948, 0.995],
            "saturation": 1.06,
            "vibrance": 0.16,
            "clarity": 0.38,
            "highlight_tint": [0.170, 0.045, -0.115],
        },
    },
    "dreamy_sunbreak": {
        "id": "dreamy_sunbreak",
        "name": "Sunbreak",
        "family": "dreamy",
        "description": (
            "Gradually opens up the midtones, like sunlight emerging "
            "from behind a cloud."
        ),
        "config": {
            "effect_type": "dreamy_grade",
            "tone_curve": [0, 0.12, 0.29, 0.53, 0.76, 0.93, 1],
            "saturation": 1.04,
            "vibrance": 0.14,
            "clarity": 0.45,
            "sunbreak_strength": 0.32,
            "sunbreak_start_seconds": 0.4,
            "sunbreak_end_seconds": 2.2,
        },
    },
    "dreamy_wildflower": {
        "id": "dreamy_wildflower",
        "name": "Wildflower",
        "family": "dreamy",
        "description": "Selectively enriches greens and pinks, giving leaves and petals more life.",
        "config": {
            "effect_type": "dreamy_grade",
            "tone_curve": [0, 0.12, 0.32, 0.575, 0.81, 0.95, 1],
            "saturation": 1.065,
            "vibrance": 0.12,
            "clarity": 0.44,
            "hue_accents": [(115, 52, 0.67), (314, 57, 0.79)],
        },
    },
    "dreamy_pearl_daylight": {
        "id": "dreamy_pearl_daylight",
        "name": "Pearl Daylight",
        "family": "dreamy",
        "description": "A bright, airy high-key grade with softer whites and restrained pastels.",
        "config": {
            "effect_type": "dreamy_grade",
            "tone_curve": [0.023, 0.24, 0.46, 0.71, 0.87, 0.962, 1],
            "saturation": 0.94,
            "vibrance": 0.075,
            "clarity": 0.30,
        },
    },
    "dreamy_window_light": {
        "id": "dreamy_window_light",
        "name": "Window Light",
        "family": "dreamy",
        "description": "A soft directional lift from the upper left, fading gradually across the frame.",
        "config": {
            "effect_type": "dreamy_grade",
            "tone_curve": [0, 0.12, 0.305, 0.55, 0.775, 0.937, 1],
            "saturation": 1.05,
            "vibrance": 0.13,
            "clarity": 0.43,
            "window_strength": 0.48,
            "window_side": "left",
            "highlight_tint": [0.045, 0.012, -0.035],
        },
    },

}