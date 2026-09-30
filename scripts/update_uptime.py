from datetime import date
from html import escape
from pathlib import Path
import re


BIRTHDAY = date(2004, 10, 3)
LINE_WIDTH = 68
SVG_FILES = (Path("dark_mode.svg"), Path("light_mode.svg"))


def uptime(today: date | None = None) -> str:
    today = today or date.today()
    months_total = (today.year - BIRTHDAY.year) * 12 + today.month - BIRTHDAY.month
    if today.day < BIRTHDAY.day:
        months_total -= 1
    years, months = divmod(months_total, 12)
    anchor_month_index = BIRTHDAY.month - 1 + months_total
    anchor = date(
        BIRTHDAY.year + anchor_month_index // 12,
        anchor_month_index % 12 + 1,
        BIRTHDAY.day,
    )
    days = (today - anchor).days
    return f"{years} years, {months} months, {days} days"


def replace_tspan(svg: str, element_id: str, value: str) -> str:
    pattern = rf'(<tspan[^>]*\bid="{re.escape(element_id)}"[^>]*>).*?(</tspan>)'
    updated, count = re.subn(pattern, rf"\g<1>{escape(value)}\g<2>", svg, count=1)
    if count != 1:
        raise RuntimeError(f"Could not find exactly one SVG element with id={element_id!r}")
    return updated


def update(path: Path, value: str) -> None:
    prefix = ". Uptime:"
    dot_count = max(2, LINE_WIDTH - len(prefix) - len(value) - 1)
    dots = "." * max(1, dot_count - 1) + " "

    svg = path.read_text(encoding="utf-8")
    svg = replace_tspan(svg, "uptime_data_dots", dots)
    svg = replace_tspan(svg, "uptime_data", value)
    path.write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    current = uptime()
    for svg_file in SVG_FILES:
        update(svg_file, current)
    print(current)
