"""
Runs every project script in order and reports which ones succeeded.
Useful for regenerating the whole outputs/ gallery after a parameter change.
"""
import subprocess
import sys
from pathlib import Path

PROJECTS_DIR = Path(__file__).resolve().parent / "projects"


def main():
    scripts = sorted(PROJECTS_DIR.glob("*.py"))
    failures = []
    for script in scripts:
        print(f"\n=== Running {script.name} ===")
        result = subprocess.run([sys.executable, str(script)])
        if result.returncode != 0:
            failures.append(script.name)

    print("\n\nSummary")
    print("-------")
    print(f"{len(scripts) - len(failures)}/{len(scripts)} succeeded")
    if failures:
        print("Failed:")
        for f in failures:
            print(f"  - {f}")


if __name__ == "__main__":
    main()
