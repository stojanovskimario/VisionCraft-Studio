function ThemeSelector({ theme, setTheme }) {
  return (
    <div>
      <h2>Choose Theme</h2>

      <button onClick={() => setTheme('vintage')}>
        Vintage
      </button>
    </div>
  )
}

export default ThemeSelector