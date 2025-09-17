
# Running Tetris with Python Virtual Environment

## 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ASE420-Tetris.git
cd ASE420-Tetris
```

## 2. Create a Virtual Environment

### Windows

Open Command Prompt or PowerShell:

```powershell
python -m venv venv
venv\Scripts\activate
```

### Linux / WSL

Open your terminal:

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Run the Game

Navigate to the `tetris/new_code/tetris_game` directory and run the provided script:

### Windows (using WSL) or Linux

```bash
cd tetris/new_code/tetris_game
source /path/to/your/venv/bin/activate  # Activate your venv
./run_pip.sh
```

### Windows (native)

Open PowerShell and run:

```powershell
cd tetris\new_code\tetris_game
venv\Scripts\activate
bash run_pip.sh
```

---

**Note:**
- Make sure you have Python 3 installed.
- The script will install pygame and run the game automatically.
- To deactivate the virtual environment, use `deactivate` in your terminal.
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
