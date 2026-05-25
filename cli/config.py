from pathlib import Path

def get_project_root() -> Path:
    current_dir = Path(__file__).resolve()
    for parent in current_dir.parents:
        if (parent / "uv.lock").exists() or (parent / "pyproject.toml").exists():
            return parent
    return Path(__file__).resolve().parents[2]

root = get_project_root()

CLI_DIR = root / "cli"
TEMPLATE_DIR = CLI_DIR / "templates" / "backend"