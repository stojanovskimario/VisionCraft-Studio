from VisionCraftStudio.services.effects.action_service import (
    process_action_effect,
)


def process_action_family(
    input_path,
    output_path,
    config,
    choices=None,
    watermark_path=None,
):
    return process_action_effect(
        input_path=input_path,
        output_path=output_path,
        config=config,
        choices=choices,
        watermark_path=watermark_path,
    )