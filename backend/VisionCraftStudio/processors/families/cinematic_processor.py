
from VisionCraftStudio.services.effects.cinematic_service import (
    process_cinematic_effect,
)


def process_cinematic_family(
    input_path,
    output_path,
    config,
    choices=None,
    watermark_path=None,
):
    return process_cinematic_effect(
        input_path=input_path,
        output_path=output_path,
        config=config,
        choices=choices,
        watermark_path=watermark_path,
    )
