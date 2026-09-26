export async function processVideo(video, theme, choices, watermark) {
  const formData = new FormData()

  formData.append('video', video)
  formData.append('theme', theme)
  formData.append('choices', JSON.stringify(choices))

  if (watermark) {
    formData.append('watermark', watermark)
  }

  const response = await fetch('/api/process-video/', {
    method: 'POST',
    body: formData,
  })

  const data = await response.json()

  if (!response.ok) {
    throw new Error(data.error || 'Failed to process video.')
  }

  return data
}