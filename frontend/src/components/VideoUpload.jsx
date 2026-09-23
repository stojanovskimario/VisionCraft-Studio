function VideoUpload({ video, setVideo }) {
  return (
    <div>
      <h2>Upload Video</h2>

      <input
        type="file"
        accept="video/*"
        onChange={(event) => {
          setVideo(event.target.files[0])
        }}
      />

      {video && (
        <p>
          Selected video: {video.name}
        </p>
      )}
    </div>
  )
}

export default VideoUpload