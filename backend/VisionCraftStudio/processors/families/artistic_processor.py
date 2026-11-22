from VisionCraftStudio.services.effects.artistic_service import (
    process_artistic_effect,
)


def process_artistic_family(
    input_path,
    output_path,
    config,
    choices=None,
    watermark_path=None,
):
    return process_artistic_effect(
        input_path=input_path,
        output_path=output_path,
        config=config,
        choices=choices,
        watermark_path=watermark_path,
    )