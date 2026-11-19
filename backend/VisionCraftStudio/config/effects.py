
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

    "tropical_water": {
        "id": "tropical_water",
        "name": "Tropical Water",
        "family": "underwater",
        "description": "Bright tropical turquoise water with vibrant colors and warm lighting.",
        "config": {
            "red": 0.95,
            "green": 1.12,
            "blue": 1.20,
            "contrast": 0.96,
            "distortion": 2.0,
            "bubbles": True,
            "light_rays": True,
            "soft_focus": 0.8
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
    }


}