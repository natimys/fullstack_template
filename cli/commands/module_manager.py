import typer
from rich import print
from pathlib import Path

app = typer.Typer()

def get_project_root() -> Path:
    current_dir = Path(__file__).resolve()
    for parent in current_dir.parents:
        if (parent / "uv.lock").exists() or (parent / "pyproject.toml").exists():
            return parent
    return Path(__file__).resolve().parents[2]

path = get_project_root

@app.command()
def create_module(module_name: str)
    pass