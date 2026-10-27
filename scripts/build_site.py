from pathlib import Path
import shutil


root = Path(__file__).resolve().parents[1]
target = root / "_site"
if target.exists():
    shutil.rmtree(target)
target.mkdir()
for name in ["index.html", "site.css", "app.py", "LICENSE", "favicon.svg"]:
    shutil.copy2(root / name, target / name)
shutil.copytree(root / "electrical", target / "electrical", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
shutil.copytree(root / "examples", target / "examples")
(target / ".nojekyll").touch()
print("Static Python application built in _site")
