
from VisionCraftStudio.services.effects.retro_service import (
    process_retro_effect,
)


def process_retro_family(
    input_path,
    output_path,
    config,
    choices=None,
    watermark_path=None,
):
    return process_retro_effect(
        input_path=input_path,
        output_path=output_path,
        config=config,
        choices=choices,
        watermark_path=watermark_path,
    )
