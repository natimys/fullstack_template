import subprocess

import typer
from rich.console import Console

from cli.config import ROOT

app = typer.Typer(help="Manage Docker Compose project")
console = Console()


def _compose(*args: str) -> int:
    return subprocess.call(
        ["docker", "compose", *args],
        cwd=ROOT,
    )


@app.command()
def up(
    services: list[str] = typer.Argument(None, help="Services to start (default: all)"),
    build: bool = typer.Option(False, "--build", "-b", help="Rebuild images before starting"),
):
    cmd = ["up", "-d"]
    if build:
        cmd.append("--build")
    cmd.extend(services or [])
    _compose(*cmd)


@app.command()
def down(
    volumes: bool = typer.Option(False, "--volumes", "-v", help="Remove volumes"),
):
    cmd = ["down"]
    if volumes:
        cmd.append("--volumes")
    _compose(*cmd)


@app.command()
def restart(
    services: list[str] = typer.Argument(None, help="Services to restart (default: all)"),
):
    _compose("down")
    cmd = ["up", "-d"]
    cmd.extend(services or [])
    _compose(*cmd)


@app.command()
def logs(
    service: str = typer.Argument(None, help="Service name"),
    follow: bool = typer.Option(True, "--follow/--no-follow", "-f", help="Follow log output"),
    tail: int = typer.Option(100, "--tail", "-t", help="Number of lines to show"),
):
    cmd = ["logs"]
    if follow:
        cmd.append("--follow")
    cmd.extend(["--tail", str(tail)])
    if service:
        cmd.append(service)
    _compose(*cmd)


@app.command()
def status():
    _compose("ps")


@app.command()
def rebuild(
    services: list[str] = typer.Argument(None, help="Services to rebuild (default: all)"),
):
    _compose("build", *(services or []))
    _compose("up", "-d", "--force-recreate", *(services or []))


@app.command()
def init(
    env: bool = typer.Option(True, help="Create .env from .env.example if missing"),
):
    if env:
        env_file = ROOT / ".env"
        env_example = ROOT / ".env.example"
        if not env_file.exists() and env_example.exists():
            env_file.write_text(env_example.read_text(encoding="utf-8"), encoding="utf-8")
            console.print("[green].env created from .env.example[/green]")
        else:
            console.print("[yellow].env already exists or .env.example missing[/yellow]")
