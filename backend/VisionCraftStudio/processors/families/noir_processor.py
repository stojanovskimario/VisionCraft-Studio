from VisionCraftStudio.services.effects.noir_service import (
    process_noir_effect,
)


def process_noir_family(
    input_path,
    output_path,
    config,
    choices=None,
    watermark_path=None,
):
    return process_noir_effect(
        input_path=input_path,
        output_path=output_path,
        config=config,
        choices=choices,
        watermark_path=watermark_path,
    )