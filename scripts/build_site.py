from pathlib import Path
import shutil
from hashlib import sha256


root = Path(__file__).resolve().parents[1]
target = root / "_site"
if target.exists():
    shutil.rmtree(target)
target.mkdir()
for name in ["index.html", "site.css", "app.py", "LICENSE", "favicon.svg"]:
    shutil.copy2(root / name, target / name)
page = (target / "index.html").read_text()
for asset in ["site.css", "favicon.svg"]:
    version = sha256((target / asset).read_bytes()).hexdigest()[:12]
    page = page.replace('href="' + asset + '"', 'href="' + asset + '?v=' + version + '"')
(target / "index.html").write_text(page)
shutil.copytree(root / "electrical", target / "electrical", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
shutil.copytree(root / "examples", target / "examples")
(target / ".nojekyll").touch()
print("Static Python application built in _site")
