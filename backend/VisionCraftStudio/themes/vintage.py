from .theme import ThemeStep


VINTAGE_THEME = {
    "id": "vintage",
    "name": "Vintage",
    "description": "Give your video an old-school vintage style.",
    "steps": [
        ThemeStep(
            id="grayscale",
            question="Do you want to make the video black and white?",
            step_type="boolean"
        ),
        ThemeStep(
            id="rotate",
            question="How many degrees do you want to rotate the video?",
            step_type="number"
        ),
        ThemeStep(
            id="speed",
            question="How much do you want to speed up the video? Enter a multiplier such as 1.5 for 1.5x.",
            step_type="number"
        ),
        ThemeStep(
            id="watermark",
            question="Do you want to add a watermark?",
            step_type="boolean"
        )
    ]
}