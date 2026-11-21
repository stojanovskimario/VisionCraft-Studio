
from VisionCraftStudio.config.effects import EFFECTS

from VisionCraftStudio.processors.families.underwater_processor import (
    process_underwater_effect,
)

from VisionCraftStudio.processors.families.vintage_processor import (
    process_vintage_family,
)

from VisionCraftStudio.processors.families.futuristic_processor import (
    process_futuristic_effect
)

from VisionCraftStudio.processors.families.retro_processor import (
    process_retro_family,
)

from VisionCraftStudio.processors.families.cinematic_processor import (
    process_cinematic_family,
)

from VisionCraftStudio.processors.families.noir_processor import (
    process_noir_family,
)

from VisionCraftStudio.processors.families.vhs_processor import (
    process_vhs_family,
)

from VisionCraftStudio.processors.families.dreamy_processor import (
    process_dreamy_family,
)

from VisionCraftStudio.processors.families.action_processor import (
    process_action_family,
)

from VisionCraftStudio.processors.families.travel_processor import (
    process_travel_family,
)


FAMILY_PROCESSORS = {
    "underwater": process_underwater_effect,
    "vintage": process_vintage_family,
    "futuristic": process_futuristic_effect,
    "retro": process_retro_family,
    "cinematic": process_cinematic_family,
    "noir": process_noir_family,
    "vhs": process_vhs_family,
    "dreamy": process_dreamy_family,
    "action": process_action_family,
    "travel": process_travel_family,
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
