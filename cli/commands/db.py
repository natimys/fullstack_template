import subprocess

import typer
from cli.paths import find_project_root

app = typer.Typer(help="Run Alembic against the Compose database.")
PROJECT_ROOT = find_project_root()


def _alembic(*args: str) -> None:
    result = subprocess.run(
        ["docker", "compose", "exec", "-T", "backend", "alembic", *args],
        cwd=PROJECT_ROOT,
    )
    if result.returncode:
        raise typer.Exit(result.returncode)


@app.command()
def upgrade(revision: str = "head") -> None:
    _alembic("upgrade", revision)


@app.command()
def revision(message: str, autogenerate: bool = True) -> None:
    args = ["revision", "-m", message]
    if autogenerate:
        args.append("--autogenerate")
    _alembic(*args)


@app.command()
def downgrade(revision: str = "-1") -> None:
    _alembic("downgrade", revision)
