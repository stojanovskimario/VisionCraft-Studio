export async function processPhotoEffect(photo, effectId) {
    const formData = new FormData();

    formData.append("photo", photo);
    formData.append("effect_id", effectId);

    const response = await fetch("/api/process-photo-effect/", {
        method: "POST",
        body: formData,
    });

    if (!response.ok) {
        const data = await response.json().catch(() => null);

        throw new Error(
            data?.error || "Failed to process photo."
        );
    }

    return response.blob();
}