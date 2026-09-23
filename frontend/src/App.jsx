import { useEffect, useState } from 'react'

function App() {
  const [message, setMessage] = useState('Connecting...')

  useEffect(() => {
    fetch('/api/test/')
      .then(response => response.json())
      .then(data => {
        setMessage(data.message)
      })
      .catch(error => {
        console.error(error)
        setMessage('Failed to connect to Django')
      })
  }, [])

  return (
    <div>
      <h1>VisionCraftStudio</h1>
      <p>{message}</p>
    </div>
  )
}

export default App