import typer
from commands.module_manager import app as module_manager

app = typer.Typer()
app.add_typer(module_manager)


if __name__ == "__main__":
    app()