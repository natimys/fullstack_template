import typer

from cli.commands.module_manager import app as module_app
from cli.commands.project import app as project_app
from cli.commands.db import app as db_app

app = typer.Typer(help="Fullstack Template CLI")
app.add_typer(module_app, name="module", help="Manage backend modules")
app.add_typer(project_app, name="project", help="Manage Docker Compose project")
app.add_typer(db_app, name="db", help="Database migrations")

if __name__ == "__main__":
    app()
