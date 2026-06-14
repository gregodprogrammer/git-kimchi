# Git Kimchi LMS — Maintainer Guide

Quick reference for common tasks and commands.

---

## Build

```bash
# Install dependencies
pip install -r requirements.txt

# Build the static site
python site-src/build.py

# Preview locally (from repo root)
python -m http.server 8000 --directory docs
# Then open http://localhost:8000
```

## Project Structure

| Path | Purpose |
|---|---|
| `site-src/build.py` | Single build script — run this to regenerate `docs/` |
| `site-src/templates/` | Jinja2 HTML templates (base, index, lesson) |
| `site-src/static/` | CSS and JS assets |
| `*.md` | Source markdown files (lesson content) |
| `docs/` | Generated output — **do not edit directly** |
| `.github/workflows/` | CI/CD configuration |

## Add a New Lesson

1. Create a new `XX-name.md` file in the repo root (use two-digit prefix, e.g., `16-new-topic.md`)
2. Start with `# Title` as the first line
3. Add an optional first paragraph as the card description (shown on homepage)
4. Run `python site-src/build.py` to generate the HTML
5. Commit and push — CI will deploy automatically

## Edit an Existing Lesson

1. Edit the corresponding `*.md` file
2. Run `python site-src/build.py`
3. Review `docs/lessons/XX-name.html` in the browser
4. Commit and push

## Run CI/CD Locally (Optional)

```bash
# Verify a PR build without pushing
git fetch origin
git checkout -b test-branch
python site-src/build.py
test -f docs/index.html && echo "Build OK"
```

## Test Progress Tracking

```bash
# Open browser console and run:
localStorage.getItem('git-kimchi-progress')
# Output: {"visited":{"1":true},"completed":{"1":true}}

# Reset progress:
localStorage.removeItem('git-kimchi-progress')
```

## Deploy Checklist

1. Push to `main` branch → `pages.yml` runs automatically
2. Check the Actions tab for the `deploy` job status
3. Verify site URL in **Settings → Pages**
4. If 404: ensure Pages source is set to **GitHub Actions**, not branch

## Customize Colors

All design tokens are CSS custom properties in [`site-src/static/css/style.css`](site-src/static/css/style.css) under `:root`. Key tokens:

```css
--primary: #e76f51;   /* Main accent */
--secondary: #2a9d8f; /* Teal */
--accent: #e9c46a;    /* Yellow/gold */
--bg: #fdf6f0;        /* Page background */
--text: #264653;      /* Body text */
```

Change them here; no other files need updating.

## Customize Section Colors

In [`site-src/build.py`](site-src/build.py), update `SECTION_COLORS`:

```python
SECTION_COLORS = {
    "core": "linear-gradient(90deg, #e76f51, #f4a261)",
    "intermediate": "linear-gradient(90deg, #2a9d8f, #8ab17d)",
    "advanced": "linear-gradient(90deg, #264653, #2a9d8f)",
    "capstone": "linear-gradient(90deg, #e9c46a, #e76f51)",
}
```

## Documentation

| File | Purpose |
|---|---|
| `documentation/project-report.md` | Full project documentation (this folder) |
| `documentation/project-report.docx` | Word export of the above |
| `documentation/README.md` | This file — quick maintainer reference |

## Common Issues

| Issue | Fix |
|---|---|
| Lesson links 404 on local preview | Use `python -m http.server`, not `file://` |
| Build succeeds but site is blank | Check `docs/` was generated and committed |
| Fonts missing | Requires internet; no offline font fallback is bundled |
| Progress not persisting | Expected in incognito/private browsing mode |

## Links

- **Repository:** [https://github.com/gregodprogrammer/git-kimchi](https://github.com/gregodprogrammer/git-kimchi)
- **Live site:** `https://gregodprogrammer.github.io/git-kimchi/` (configure after first deploy)