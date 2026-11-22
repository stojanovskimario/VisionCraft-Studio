from VisionCraftStudio.config.photo_effects import PHOTO_EFFECTS

from VisionCraftStudio.services.photo_effects.photo_service import (
    apply_photo_effect,
)


def run_photo_effect(image, effect_id):

    effect = PHOTO_EFFECTS.get(effect_id)

    if effect is None:
        raise ValueError(
            f"Unknown photo effect: {effect_id}"
        )

    return apply_photo_effect(
        image=image,
        effect_id=effect_id,
        config=effect["config"],
    )