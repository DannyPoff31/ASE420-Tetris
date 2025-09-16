# ASE420-Tetris
Repository for our Tetris project
## Quick Virtual Environment Activation

Set these environment variables to easily activate your Python virtual environment:

### Windows (PowerShell)
Add this to your PowerShell profile (e.g., `$PROFILE`):

```powershell
function WINDOWS_ACTIVATE {
	& "${PWD}\tetris\venv\Scripts\Activate.ps1"
}
```

Usage: Just type `WINDOWS_ACTIVATE` in your repo root.

### Linux/macOS (WSL, Bash)
Add this to your `.bashrc` or `.zshrc`:

```bash
function LINUX_ACTIVATE() {
	source "$PWD/tetris/venv/bin/activate"
}
```

Usage: Just type `LINUX_ACTIVATE` in your repo root.
