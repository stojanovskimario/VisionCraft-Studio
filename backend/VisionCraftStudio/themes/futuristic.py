from .theme import ThemeStep


FUTURISTIC_THEME = {
    "id": "futuristic",
    "name": "Futuristic",
    "description": "Give your video a futuristic style.",
    "steps": [
        ThemeStep(
            id="color_effect",
            question="Do you want to apply a futuristic color effect?",
            step_type="boolean"
        ),
        ThemeStep(
            id="glitch",
            question="Do you want to add a glitch effect?",
            step_type="boolean"
        ),
        ThemeStep(
            id="speed",
            question="Do you want to speed up part of the video?",
            step_type="number"
        ),
        ThemeStep(
            id="watermark",
            question="Do you want to add a watermark?",
            step_type="boolean"
        )
    ]
}