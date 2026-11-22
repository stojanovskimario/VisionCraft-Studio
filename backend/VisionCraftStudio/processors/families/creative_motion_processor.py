from VisionCraftStudio.services.effects.creative_motion_service import (
    process_creative_motion_effect,
)


def process_creative_motion_family(
    input_path,
    output_path,
    config,
    choices=None,
    watermark_path=None,
):
    return process_creative_motion_effect(
        input_path=input_path,
        output_path=output_path,
        config=config,
        choices=choices,
        watermark_path=watermark_path,
    )
