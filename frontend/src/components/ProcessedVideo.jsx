function ProcessedVideo({ result }) {
  if (!result) {
    return null
  }

  return (
    <div>
      <h2>Processed Video</h2>

      <video
        controls
        width="600"
        src={`http://127.0.0.1:8000${result.video_url}`}
      />

      <p>
        Video processed successfully!
      </p>
    </div>
  )
}

export default ProcessedVideo