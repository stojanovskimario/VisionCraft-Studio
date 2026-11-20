from VisionCraftStudio.services.effects.vhs_service import process_vhs_effect


def process_vhs_family(
    input_path,
    output_path,
    config,
    choices=None,
    watermark_path=None,
):
    return process_vhs_effect(
        input_path=input_path,
        output_path=output_path,
        config=config,
        choices=choices,
        watermark_path=watermark_path,
    )