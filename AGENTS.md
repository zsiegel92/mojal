# AGENTS.md - Development Guidelines

## Build/Lint/Test Commands
- **Lint Python**: `ruff check .` and `ruff format .`
- **Run Mojo locally**: `cd mojo_app && pixi run mojo mojo_module.mojo`
- **Run Python locally**: `python call_mojo_from_python_in_folder.py`
- **Run on Modal**: `python -m modal run python_app/main.py`
- **Install dependencies**: `uv sync` (Python) or `cd mojo_app && pixi install` (Mojo)

## Project Structure
- `mojo_app/`: Mojo modules and Pixi environment
- `python_app/`: Modal deployment code
- Root: Python scripts that call Mojo from different contexts

## Code Style Guidelines
- **Python**: Follow PEP 8, use type hints, use `# type: ignore` for Mojo imports
- **Mojo**: Use `fn` for functions, `var` for variables, explicit types when possible
- **Imports**: Group standard library, third-party, then local imports
- **Error handling**: Use `raises` in Mojo functions, try/except in Python
- **Naming**: snake_case for variables/functions, PascalCase for classes

## Dependencies
- Python: Modal, Modular SDK, Ruff for linting
- Mojo: Modular toolchain via Pixi package manager