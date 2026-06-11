import typer
from rich.console import Console
from cli.config import (root, CLI_DIR, TEMPLATE_DIR)

app = typer.Typer()

console = Console()

@app.command()
def create(module_name: str):
    console.print(root, style="magenta")
    console.print(f"created {module_name}!", style="bold green")
