import subprocess

import typer
from rich.console import Console
from cli.paths import find_project_root

app = typer.Typer(help="Create the first administrator inside the backend container.")
console = Console()
PROJECT_ROOT = find_project_root()


@app.command("create")
def create_admin(email: str, name: str = "Administrator") -> None:
    if not typer.confirm(
        f"Create administrator {email!r} in the current Compose database?",
        default=False,
    ):
        raise typer.Abort()
    password = typer.prompt(
        "Password (minimum 12 characters)", hide_input=True, confirmation_prompt=True
    )
    if len(password) < 12:
        raise typer.BadParameter("Password must be at least 12 characters.")
    result = subprocess.run(
        [
            "docker",
            "compose",
            "exec",
            "-T",
            "backend",
            "python",
            "-m",
            "core.admin",
            "create",
            "--email",
            email,
            "--name",
            name,
        ],
        input=password + "\n",
        text=True,
        cwd=PROJECT_ROOT,
    )
    if result.returncode:
        raise typer.Exit(result.returncode)
    console.print("Administrator created.")
