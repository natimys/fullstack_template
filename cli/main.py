import typer
from .commands.module_manager import app as module_manager
from .commands.db import app as db_commands
from .commands.admin import app as admin_commands
from .commands.project import doctor, dev, test

app = typer.Typer(help="Fullstack Template developer tools.")
app.add_typer(module_manager, name="module")
app.add_typer(db_commands, name="db")
app.add_typer(admin_commands, name="admin")
app.command()(doctor)
app.command()(dev)
app.command()(test)


if __name__ == "__main__":
    app()
