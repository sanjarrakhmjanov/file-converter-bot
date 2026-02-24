from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)


def safe_unlink(path: Path) -> None:
    if path.exists():
        path.unlink()


def safe_rmdir(path: Path) -> None:
    if path.exists() and not any(path.iterdir()):
        path.rmdir()
