from VisionCraftStudio.services.effects.dreamy_service import (
    process_dreamy_effect,
)


def process_dreamy_family(
    input_path,
    output_path,
    config,
    choices=None,
    watermark_path=None,
):
    return process_dreamy_effect(
        input_path=input_path,
        output_path=output_path,
        config=config,
        choices=choices,
        watermark_path=watermark_path,
    )