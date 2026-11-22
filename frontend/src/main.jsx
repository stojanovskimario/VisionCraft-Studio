import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import StudioShell from './components/StudioShell.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <StudioShell />
  </StrictMode>,
)
