
function ThemeSelector({ theme, setTheme }) {
    return (
        <div>
            <h2>Choose Theme</h2>

            <button onClick={() => setTheme('vintage')}>
                Vintage
            </button>

            <button onClick={() => setTheme('futuristic')}>
                Futuristic
            </button>

            <button onClick={() => setTheme('retro')}>
                Retro
            </button>

            <button onClick={() => setTheme('cinematic')}>
                Cinematic
            </button>

            <button onClick={() => setTheme('noir')}>
                Noir
            </button>

            <button onClick={() => setTheme('vhs')}>
                VHS
            </button>

            <button onClick={() => setTheme('dreamy')}>
                Dreamy
            </button>

            <button onClick={() => setTheme('action')}>
                Action
            </button>

        </div>
    )
}

export default ThemeSelector
