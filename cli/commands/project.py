import shutil
import subprocess

import typer
from rich.console import Console

from cli.paths import find_project_root

app_root = find_project_root()
console = Console()


def doctor() -> None:
    checks = {
        "Docker CLI": shutil.which("docker") is not None,
        "Compose file": (app_root / "docker-compose.yml").is_file(),
        "Frontend lockfile": (
            app_root / "src" / "frontend" / "package-lock.json"
        ).is_file(),
        "Local .env": (app_root / ".env").is_file(),
    }
    for label, passed in checks.items():
        console.print(
            f"{'[green]OK[/green]' if passed else '[red]MISSING[/red]'} {label}"
        )
    if shutil.which("docker"):
        result = subprocess.run(
            ["docker", "compose", "config", "--quiet"], cwd=app_root
        )
        console.print(
            f"{'[green]OK[/green]' if result.returncode == 0 else '[red]FAIL[/red]'} Compose configuration"
        )
        if result.returncode:
            raise typer.Exit(result.returncode)


def dev() -> None:
    result = subprocess.run(["docker", "compose", "up", "--build"], cwd=app_root)
    if result.returncode:
        raise typer.Exit(result.returncode)


def test() -> None:
    result = subprocess.run(["uv", "run", "pytest"], cwd=app_root)
    if result.returncode:
        raise typer.Exit(result.returncode)
