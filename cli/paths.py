from pathlib import Path


def find_project_root() -> Path:
    candidates = (Path.cwd(), *Path(__file__).resolve().parents)
    for candidate in candidates:
        if (candidate / "docker-compose.yml").is_file() and (
            candidate / "src" / "backend"
        ).is_dir():
            return candidate
    raise RuntimeError("Run this command from a Fullstack Template checkout.")
