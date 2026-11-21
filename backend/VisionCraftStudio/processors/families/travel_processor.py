from VisionCraftStudio.services.effects.travel_service import (
    process_travel_effect,
)


def process_travel_family(
    input_path,
    output_path,
    config,
    choices=None,
    watermark_path=None,
):
    return process_travel_effect(
        input_path=input_path,
        output_path=output_path,
        config=config,
        choices=choices,
        watermark_path=watermark_path,
    )