"""Prepare an isolated, correctly named Arduino sketch for one build variant."""
import argparse
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--destination", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--language", choices=("en", "zh-CN"), required=True)
    args = parser.parse_args()

    project = args.project.resolve()
    sketches = list(project.glob("*.ino"))
    if len(sketches) != 1:
        raise SystemExit("Expected exactly one root .ino file")

    output_root = args.output_root.resolve()
    excluded = {output_root, (project / "Final-Build").resolve()}

    def ignore(directory, names):
        ignored = {
            ".git", "build", "build_variants", "Final-Build",
            "__pycache__", ".pio"
        }
        return [
            name for name in names
            if name in ignored or (Path(directory) / name).resolve() in excluded
        ]

    args.destination.mkdir(parents=True, exist_ok=True)
    work = Path(tempfile.mkdtemp(
        prefix=f"{args.language}-", dir=args.destination.resolve()
    ))
    sketch = work / sketches[0].stem
    shutil.copytree(project, sketch, ignore=ignore)

    if args.language == "zh-CN":
        chinese = project / "zh-CN" / "dashboard_source.zh-CN.html"
        if not chinese.is_file():
            raise SystemExit(f"Missing Chinese dashboard: {chinese}")
        shutil.copyfile(chinese, sketch / "dashboard_source.html")
        subprocess.run(
            [sys.executable, str(sketch / "tools" / "build_dashboard.py")],
            check=True,
            stdout=subprocess.DEVNULL,
        )

    staged_ino = sketch / sketches[0].name
    if not staged_ino.is_file():
        raise SystemExit(f"Staged sketch is missing its main file: {staged_ino}")

    print(sketch)


if __name__ == "__main__":
    main()
