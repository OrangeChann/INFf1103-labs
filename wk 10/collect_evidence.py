"""Lab 8, sections 9 and 11: save real execution logs; never commit or push."""
import os
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
EVIDENCE = ROOT / "evidence"


def record(filename: str, command: list[str], stdin: str | None = None) -> None:
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    result = subprocess.run(command, cwd=ROOT, input=stdin, text=True,
                            encoding="utf-8", errors="replace", env=env,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    timestamp = datetime.now(timezone.utc).isoformat()
    content = (f"Lab 8 execution evidence | UTC {timestamp}\n"
               f"Working directory: {ROOT}\nCommand arguments: {command!r}\n\n"
               f"{result.stdout}\nExit code: {result.returncode}\n")
    (EVIDENCE / filename).write_text(content, encoding="utf-8")
    print(f"{filename}: exit {result.returncode}", flush=True)
    if result.returncode:
        print(result.stdout)
        raise SystemExit(result.returncode)


def main() -> None:
    EVIDENCE.mkdir(exist_ok=True)
    record("local_tests.txt", [sys.executable, "-B", "-m", "unittest", "-v"])
    record("docker_version.txt", ["docker", "version"])
    record("docker_build.txt", ["docker", "build", "--progress=plain", "-t", "inf1103-lab8", "."])
    record("docker_tests.txt", ["docker", "run", "--rm", "inf1103-lab8",
                                "python", "-B", "-m", "unittest", "-v"])
    record("demo_output.txt", ["docker", "run", "--rm", "-v", f"{ROOT}:/app",
                               "inf1103-lab8", "python", "-B", "lab8_demo.py"])
    # The menu writes a copy inside the disposable container, preserving sample JSON.
    answers = "\n".join([
        "1", "8", "1", "O1", "2", "O1", "P001", "2",
        "2", "O1", "D001", "1", "3", "O1", "4", "O1", "1",
        "3", "O1", "5", "O1", "3", "O1", "6", "6", "",
    ])
    record("docker_menu.txt", [
        "docker", "run", "--rm", "-i", "-v", f"{ROOT}:/app",
        "-e", "INVENTORY_FILE=/tmp/lab8-menu-inventory.json", "inf1103-lab8",
        "sh", "-c", "cp /app/inventory.json /tmp/lab8-menu-inventory.json && python -B main.py",
    ], answers)
    record("git_before_commit.txt", ["git", "status", "--short", "--branch"])
    record("git_history_before_commit.txt", ["git", "log", "-10", "--oneline"])
    print("All checks passed. These are logs, not screenshots. No commit or push was performed.")


if __name__ == "__main__":
    main()
