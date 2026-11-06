
from VisionCraftStudio.config.effects import EFFECTS

from VisionCraftStudio.processors.families.underwater_processor import (
    process_underwater_effect
)


FAMILY_PROCESSORS = {
    "underwater": process_underwater_effect,
}


def process_effect(
    effect_id,
    input_path,
    output_path,
    choices=None,
    watermark_path=None
):

    effect = EFFECTS.get(effect_id)

    if effect is None:
        raise ValueError(f"Unknown effect ID: {effect_id}")

    family = effect.get("family")
    config = effect.get("config", {})

    processor = FAMILY_PROCESSORS.get(family)

    if processor is None:
        raise ValueError(
            f"No processor registered for effect family: {family}"
        )

    return processor(
        input_path=input_path,
        output_path=output_path,
        config=config,
        choices=choices,
        watermark_path=watermark_path
    )
