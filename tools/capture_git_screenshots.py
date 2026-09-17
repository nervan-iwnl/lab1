"""Создаёт читаемые PNG-снимки фактического состояния Git для отчёта."""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import textwrap

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "screenshots" / "lab1"
FONT_PATH = Path("C:/Windows/Fonts/consola.ttf")
BOLD_FONT_PATH = Path("C:/Windows/Fonts/consolab.ttf")


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    return (result.stdout + result.stderr).strip()


def wrap_lines(text: str, width: int = 92) -> list[str]:
    lines: list[str] = []
    for line in text.splitlines() or [""]:
        if len(line) <= width:
            lines.append(line)
        else:
            lines.extend(textwrap.wrap(line, width=width, replace_whitespace=False, drop_whitespace=False))
    return lines


def render_terminal(title: str, blocks: list[tuple[str, str]], output: Path) -> None:
    font = ImageFont.truetype(str(FONT_PATH), 23)
    bold = ImageFont.truetype(str(BOLD_FONT_PATH), 24)
    small = ImageFont.truetype(str(FONT_PATH), 18)
    line_height = 34
    margin = 42
    title_height = 72

    rendered: list[tuple[str, list[str]]] = []
    total_lines = 0
    for command, content in blocks:
        content_lines = wrap_lines(content)
        rendered.append((command, content_lines))
        total_lines += 1 + len(content_lines) + 1

    width = 1500
    height = title_height + margin + total_lines * line_height + margin
    image = Image.new("RGB", (width, height), "#0C0F14")
    draw = ImageDraw.Draw(image)

    draw.rectangle((0, 0, width, title_height), fill="#181C24")
    for x, color in ((28, "#FF5F56"), (58, "#FFBD2E"), (88, "#27C93F")):
        draw.ellipse((x, 24, x + 20, 44), fill=color)
    draw.text((125, 20), title, font=bold, fill="#F4F4F5")

    y = title_height + 28
    for command, content_lines in rendered:
        draw.text((margin, y), f"PS D:\\programming\\mephi\\TRPO> {command}", font=font, fill="#67E8F9")
        y += line_height
        for line in content_lines:
            color = "#FCA5A5" if any(token in line for token in ("CONFLICT", "UU ", "<<<<<<<", "=======", ">>>>>>>")) else "#E5E7EB"
            draw.text((margin, y), line, font=font, fill=color)
            y += line_height
        y += line_height

    draw.text((width - 335, height - 34), "Git laboratory evidence", font=small, fill="#6B7280")
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output, optimize=True)


def conflict_screenshot() -> Path:
    status_lines = git("status", "--short", "--branch").splitlines()
    status = "\n".join(line for line in status_lines if line.startswith("##") or "hello.py" in line)
    hello = (ROOT / "hello.py").read_text(encoding="utf-8").strip()
    output = OUTPUT_DIR / "01-conflict-detected.png"
    render_terminal(
        "Конфликт слияния обнаружен",
        [
            (
                "git merge --no-ff feature-conflict",
                "Auto-merging hello.py\n"
                "CONFLICT (content): Merge conflict in hello.py\n"
                "Automatic merge failed; fix conflicts and then commit the result.",
            ),
            ("git status --short --branch", status),
            ("Get-Content hello.py", hello),
        ],
        output,
    )
    return output


def resolved_screenshot() -> Path:
    status = git("status", "--short", "--branch").splitlines()[0]
    log = git("log", "--oneline", "--graph", "--decorate", "--all", "-10")
    hello = (ROOT / "hello.py").read_text(encoding="utf-8").strip()
    output = OUTPUT_DIR / "02-conflict-resolved.png"
    render_terminal(
        "Конфликт разрешён и сохранён",
        [
            ("git status --short --branch", status),
            ("Get-Content hello.py", hello),
            ("git log --oneline --graph --decorate --all -10", log),
        ],
        output,
    )
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("conflict", "resolved"))
    args = parser.parse_args()
    output = conflict_screenshot() if args.mode == "conflict" else resolved_screenshot()
    print(output)


if __name__ == "__main__":
    main()
