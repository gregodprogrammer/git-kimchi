#!/usr/bin/env python3
"""
Git Kimchi — Static Site Generator
Converts markdown lesson files into a beautiful LMS website.
"""

import os
import re
import shutil
import sys
from pathlib import Path

import markdown
from jinja2 import Environment, FileSystemLoader

# Configuration
REPO_ROOT = Path(__file__).resolve().parent.parent
SITE_SRC = REPO_ROOT / "site-src"
DOCS_DIR = REPO_ROOT / "docs"
TEMPLATES_DIR = SITE_SRC / "templates"
STATIC_DIR = SITE_SRC / "static"

# Color mapping for card top bars by section
SECTION_COLORS = {
    "core": "linear-gradient(90deg, #e76f51, #f4a261)",
    "intermediate": "linear-gradient(90deg, #2a9d8f, #8ab17d)",
    "advanced": "linear-gradient(90deg, #264653, #2a9d8f)",
    "capstone": "linear-gradient(90deg, #e9c46a, #e76f51)",
}


def get_lesson_section(number: int) -> str:
    """Map lesson number to section name."""
    if 1 <= number <= 4:
        return "core"
    elif 5 <= number <= 9:
        return "intermediate"
    elif 10 <= number <= 14:
        return "advanced"
    elif number == 15:
        return "capstone"
    return "reference"


def get_section_name(section_key: str) -> str:
    """Return human-readable section name."""
    names = {
        "core": "Core Git",
        "intermediate": "Intermediate Git & GitHub",
        "advanced": "Advanced / DevOps",
        "capstone": "Capstone & Reference",
    }
    return names.get(section_key, "Reference")


def slugify_filename(name: str) -> str:
    """Remove .md extension."""
    return name[:-3] if name.endswith(".md") else name


def estimate_read_time(text: str) -> str:
    """Estimate reading time in minutes (200 wpm)."""
    words = len(text.split())
    minutes = max(1, round(words / 200))
    return f"{minutes} min read"


def extract_first_h1(md_text: str) -> str:
    """Extract the first H1 heading content."""
    m = re.search(r"^# (.+)$", md_text, re.MULTILINE)
    return m.group(1).strip() if m else "Untitled"


def extract_first_paragraph(md_text: str) -> str:
    """Extract the first non-empty paragraph after the first H1."""
    # Remove the first H1
    text = re.sub(r"^# .+$", "", md_text, count=1, flags=re.MULTILINE)
    # Find first paragraph
    m = re.search(r"\n\n([^\n#].{0,300})", text, re.DOTALL)
    if m:
        para = m.group(1).strip()
        # Strip markdown links and formatting
        para = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", para)
        para = re.sub(r"[\*_`#]", "", para)
        para = re.sub(r"\s+", " ", para).strip()
        # Truncate nicely
        if len(para) > 160:
            para = para[:157].rsplit(" ", 1)[0] + "..."
        return para
    return ""


def convert_md_links(md_text: str, context: str) -> str:
    """
    Convert internal ./XX-filename.md links to .html equivalents.
    context is one of: 'index', 'lesson', 'solutions'
    """
    # Pattern matches markdown links like [text](./file.md)
    def repl(m):
        text = m.group(1)
        url = m.group(2)
        if not url.startswith(("./", "../")):
            return m.group(0)
        if not url.endswith(".md"):
            return m.group(0)

        filename = os.path.basename(url)
        slug = slugify_filename(filename)

        if context == "index":
            if filename == "00-index.md":
                return f"[{text}](index.html)"
            elif filename == "99-solutions.md":
                return f"[{text}](solutions.html)"
            else:
                return f"[{text}](lessons/{slug}.html)"
        elif context == "lesson":
            if filename == "00-index.md":
                return f"[{text}](../index.html)"
            elif filename == "99-solutions.md":
                return f"[{text}](../solutions.html)"
            else:
                return f"[{text}]({slug}.html)"
        elif context == "solutions":
            if filename == "00-index.md":
                return f"[{text}](index.html)"
            else:
                return f"[{text}](lessons/{slug}.html)"
        return m.group(0)

    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", repl, md_text)


def render_markdown(md_text: str) -> tuple:
    """Render markdown to HTML and return (html_body, toc_html)."""
    md = markdown.Markdown(
        extensions=[
            "tables",
            "fenced_code",
            "toc",
            "nl2br",
        ]
    )
    html = md.convert(md_text)
    toc = getattr(md, "toc", "")
    return html, toc


def copy_static_assets():
    """Copy site-src/static to docs/static."""
    src = STATIC_DIR
    dst = DOCS_DIR / "static"
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def build():
    """Main build orchestrator."""
    # Ensure output directory exists
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    (DOCS_DIR / "lessons").mkdir(parents=True, exist_ok=True)

    # Setup Jinja2
    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)), trim_blocks=True, lstrip_blocks=True)
    base_tmpl = env.get_template("base.html")
    index_tmpl = env.get_template("index.html")
    lesson_tmpl = env.get_template("lesson.html")

    # Discover markdown files
    md_files = sorted(REPO_ROOT.glob("*.md"))

    # Collect lesson metadata first
    lessons = []
    for md_path in md_files:
        if md_path.name in ("README.md",):
            continue
        text = md_path.read_text(encoding="utf-8")
        slug = slugify_filename(md_path.name)
        title = extract_first_h1(text)
        description = extract_first_paragraph(text)
        readtime = estimate_read_time(text)

        # Determine number and section
        m = re.match(r"^(\d+)-", md_path.name)
        number = int(m.group(1)) if m else 0
        section = get_lesson_section(number)

        lessons.append({
            "path": md_path,
            "filename": md_path.name,
            "slug": slug,
            "title": title,
            "description": description,
            "readtime": readtime,
            "number": number,
            "section": section,
            "section_name": get_section_name(section),
            "text": text,
        })

    # Separate special files
    index_md = next((l for l in lessons if l["filename"] == "00-index.md"), None)
    solutions_md = next((l for l in lessons if l["filename"] == "99-solutions.md"), None)
    lesson_items = [l for l in lessons if l["number"] in range(1, 16)]
    lesson_items.sort(key=lambda x: x["number"])

    # Prepare grouped sections for index template
    sections_map = {}
    for l in lesson_items:
        sk = l["section"]
        if sk not in sections_map:
            sections_map[sk] = {
                "name": get_section_name(sk),
                "key": sk,
                "lessons": [],
            }
        sections_map[sk]["lessons"].append(l)

    # Ordered sections
    section_order = ["core", "intermediate", "advanced", "capstone"]
    sections = [sections_map[k] for k in section_order if k in sections_map]

    # Prepare nav lesson lists for base template
    lessons_core = [l for l in lesson_items if l["section"] == "core"]
    lessons_intermediate = [l for l in lesson_items if l["section"] == "intermediate"]
    lessons_advanced = [l for l in lesson_items if l["section"] == "advanced"]
    lessons_capstone = [l for l in lesson_items if l["section"] == "capstone"]

    # --- Build Index (Homepage) ---
    if index_md:
        md_text = convert_md_links(index_md["text"], "index")
        html_body, _ = render_markdown(md_text)
        ctx = {
            "page_title": "",
            "page_type": "index",
            "css_path": "static/css/style.css",
            "js_path": "static/js/app.js",
            "root_path": "",
            "lessons_path": "lessons/",
            "sections": sections,
            "lessons_core": lessons_core,
            "lessons_intermediate": lessons_intermediate,
            "lessons_advanced": lessons_advanced,
            "lessons_capstone": lessons_capstone,
            "content": html_body,
        }
        output = index_tmpl.render(ctx)
        (DOCS_DIR / "index.html").write_text(output, encoding="utf-8")
        print("  → docs/index.html")

    # --- Build Lesson Pages ---
    for idx, lesson in enumerate(lesson_items):
        md_text = convert_md_links(lesson["text"], "lesson")
        html_body, toc_html = render_markdown(md_text)

        prev_item = lesson_items[idx - 1] if idx > 0 else None
        next_item = lesson_items[idx + 1] if idx < len(lesson_items) - 1 else None

        ctx = {
            "page_title": lesson["title"],
            "page_type": "lesson",
            "css_path": "../static/css/style.css",
            "js_path": "../static/js/app.js",
            "root_path": "../",
            "lessons_path": "",
            "lesson_number": str(lesson["number"]),
            "readtime": lesson["readtime"],
            "lesson_html": html_body,
            "toc_html": toc_html,
            "prev_slug": prev_item["slug"] if prev_item else None,
            "prev_title": prev_item["title"] if prev_item else None,
            "next_slug": next_item["slug"] if next_item else None,
            "next_title": next_item["title"] if next_item else None,
            "lessons_core": lessons_core,
            "lessons_intermediate": lessons_intermediate,
            "lessons_advanced": lessons_advanced,
            "lessons_capstone": lessons_capstone,
        }
        output = lesson_tmpl.render(ctx)
        out_path = DOCS_DIR / "lessons" / f"{lesson['slug']}.html"
        out_path.write_text(output, encoding="utf-8")
        print(f"  → docs/lessons/{lesson['slug']}.html")

    # --- Build Solutions Page ---
    if solutions_md:
        md_text = convert_md_links(solutions_md["text"], "solutions")
        html_body, toc_html = render_markdown(md_text)
        ctx = {
            "page_title": solutions_md["title"],
            "page_type": "solutions",
            "css_path": "static/css/style.css",
            "js_path": "static/js/app.js",
            "root_path": "",
            "lessons_path": "lessons/",
            "lesson_number": "solutions",
            "readtime": solutions_md["readtime"],
            "lesson_html": html_body,
            "toc_html": toc_html,
            "prev_slug": lesson_items[-1]["slug"] if lesson_items else None,
            "prev_title": lesson_items[-1]["title"] if lesson_items else None,
            "next_slug": None,
            "next_title": None,
            "lessons_core": lessons_core,
            "lessons_intermediate": lessons_intermediate,
            "lessons_advanced": lessons_advanced,
            "lessons_capstone": lessons_capstone,
        }
        output = lesson_tmpl.render(ctx)
        (DOCS_DIR / "solutions.html").write_text(output, encoding="utf-8")
        print("  → docs/solutions.html")

    # --- Build 404 Page ---
    ctx_404 = {
        "page_title": "Page Not Found",
        "page_type": "404",
        "css_path": "static/css/style.css",
        "js_path": "static/js/app.js",
        "root_path": "",
        "lessons_path": "lessons/",
        "lessons_core": lessons_core,
        "lessons_intermediate": lessons_intermediate,
        "lessons_advanced": lessons_advanced,
        "lessons_capstone": lessons_capstone,
    }
    content_404 = """
<div class="page-404">
  <h1>404</h1>
  <h2>Page Not Found</h2>
  <p>Sorry, the page you're looking for doesn't exist. It might have been moved or deleted.</p>
  <a href="index.html" class="hero-cta">Back to Home</a>
</div>
"""
    output_404 = base_tmpl.render({**ctx_404, "content": content_404})
    (DOCS_DIR / "404.html").write_text(output_404, encoding="utf-8")
    print("  → docs/404.html")

    # Copy static assets
    copy_static_assets()
    print("  → docs/static/ copied")

    # Summary
    print("\nBuild complete!")
    print(f"  Lessons: {len(lesson_items)}")
    print(f"  Homepage: docs/index.html")
    print(f"  Solutions: docs/solutions.html")
    print(f"  404: docs/404.html")
    print(f"  Static assets: docs/static/")


if __name__ == "__main__":
    build()
