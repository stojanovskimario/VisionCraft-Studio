from .theme import ThemeStep


RETRO_THEME = {
    "id": "retro",
    "name": "Retro",
    "description": "Give your video a warm, old-school retro style.",
    "steps": [
        ThemeStep(
            id="colorEffect",
            question="Do you want to apply a retro color effect?",
            step_type="boolean"
        ),
        ThemeStep(
            id="filmGrain",
            question="Do you want to add film grain?",
            step_type="boolean"
        ),
    ]
}