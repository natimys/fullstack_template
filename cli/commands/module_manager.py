import re

import typer
from rich.console import Console

from cli.paths import find_project_root

app = typer.Typer(help="Discover and manage backend modules.")
console = Console()
MODULES_DIR = find_project_root() / "src" / "backend" / "modules"
MODULE_NAME = re.compile(r"^[a-z][a-z0-9_]{0,47}$")


@app.command("list")
def list_modules() -> None:
    for path in sorted(MODULES_DIR.iterdir()):
        definition = path / "module.py"
        if path.is_dir() and definition.exists():
            text = definition.read_text(encoding="utf-8")
            state = "enabled" if re.search(r"active\s*=\s*True", text) else "disabled"
            console.print(f"{path.name}: {state}")


@app.command()
def create(name: str) -> None:
    if not MODULE_NAME.fullmatch(name) or name in {"auth", "users"}:
        raise typer.BadParameter("Use a new module name matching [a-z][a-z0-9_]{0,47}.")
    module_dir = MODULES_DIR / name
    try:
        module_dir.mkdir()
    except FileExistsError:
        raise typer.BadParameter(
            f"Module {name!r} already exists; no files were changed."
        )

    files = {
        "__init__.py": "",
        "module.py": (
            "from core.modules import ModuleDefinition\n\n"
            f'module = ModuleDefinition(name="{name}", active=True, '
            f'router_prefix="/{name}", router_tags=["{name}"])\n'
        ),
        "router.py": (
            "from fastapi import APIRouter\n"
            "from .module import module\n\n"
            "router = APIRouter(prefix=module.router_prefix, tags=module.router_tags)\n\n"
            '@router.get("/")\n'
            "async def index():\n"
            '    return {"module": module.name}\n'
        ),
        "models.py": '"""Add SQLAlchemy models for this module here."""\n',
        "schemas.py": '"""Add Pydantic schemas for this module here."""\n',
    }
    for filename, contents in files.items():
        (module_dir / filename).write_text(contents, encoding="utf-8")
    console.print(f"Created discoverable module [bold]{name}[/bold].")


def _set_enabled(name: str, enabled: bool) -> None:
    if not MODULE_NAME.fullmatch(name):
        raise typer.BadParameter("Invalid module name.")
    definition = MODULES_DIR / name / "module.py"
    if not definition.is_file():
        raise typer.BadParameter(f"Module {name!r} does not exist.")
    contents = definition.read_text(encoding="utf-8")
    updated, count = re.subn(
        r"(active\s*=\s*)(True|False)", rf"\g<1>{enabled}", contents, count=1
    )
    if count != 1:
        raise typer.BadParameter("Could not find a single active flag in module.py.")
    definition.write_text(updated, encoding="utf-8")
    console.print(f"Module [bold]{name}[/bold] {'enabled' if enabled else 'disabled'}.")


@app.command()
def enable(name: str) -> None:
    _set_enabled(name, True)


@app.command()
def disable(name: str) -> None:
    _set_enabled(name, False)
