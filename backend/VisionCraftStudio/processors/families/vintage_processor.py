
from VisionCraftStudio.services.effects.vintage_service import (
    process_vintage_effect,
)


def process_vintage_family(
    input_path,
    output_path,
    config,
    choices=None,
    watermark_path=None,
):
    return process_vintage_effect(
        input_path=input_path,
        output_path=output_path,
        config=config,
        choices=choices,
        watermark_path=watermark_path,
    )
