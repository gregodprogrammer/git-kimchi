# Git Kimchi LMS — Project Report

**Version:** 1.0 — June 2026  
**Repository:** [https://github.com/gregodprogrammer/git-kimchi](https://github.com/gregodprogrammer/git-kimchi)  
**Live Site:** `https://gregodprogrammer.github.io/git-kimchi/` (placeholder — configure after first deploy)

---

## Section 1: Executive Summary

### What Is Git Kimchi LMS?

Git Kimchi LMS is a free, open-source learning management system website for a comprehensive Git and GitHub course. It transforms 16 source Markdown files (~11,000 lines of content) into a polished, Pinterest-inspired educational platform served statically via GitHub Pages from the `/docs` directory.

The site targets **DevOps beginners** — developers who understand basic terminal commands but have never deeply explored version control, branching workflows, or collaborative development platforms. The course is self-paced, requires no account creation, and stores all progress client-side using `localStorage`.

### Who Is It For?

- Junior developers learning version control for the first time
- Bootcamp students working through Git and GitHub fundamentals
- DevOps beginners needing a structured, hands-on reference
- Self-learners who prefer visual, card-based course navigation

### Key Features and Outcomes

| Feature | Implementation |
|---|---|
| Pinterest-style card grid | CSS Grid with `auto-fill minmax(280px, 1fr)` on warm cream background |
| Progress tracking | Client-side `localStorage` with completion percentages and ring chart |
| Lesson navigation | Sidebar nav with 4 sections, prev/next links, breadcrumbs |
| Completion marking | Per-lesson "Mark Complete" button with visual state |
| Responsive design | Mobile sidebar drawer, stacked layouts below 768px |
| Back-to-top button | Fixed floating button, scroll-triggered visibility |
| Auto-generated TOC | Per-lesson table of contents from markdown headings |
| Static site generation | Python build script using Markdown + Jinja2 |
| CI/CD on every push | GitHub Actions builds and deploys to GitHub Pages |

---

## Section 2: Project Architecture

### Directory Structure

```
git-kimchi/
├── .github/
│   └── workflows/
│       ├── pages.yml          # Build + deploy on push to main
│       └── verify.yml         # Build-only on pull requests
├── site-src/
│   ├── build.py               # Static site generator (Python)
│   ├── templates/
│   │   ├── base.html          # Shared layout (sidebar, header, footer)
│   │   ├── index.html         # Homepage template (hero + card grid)
│   │   └── lesson.html        # Individual lesson template
│   └── static/
│       ├── css/style.css      # Design system (20.7 KB)
│       └── js/app.js          # LMS interactions (9.3 KB)
├── docs/                      # Generated static output (served by GitHub Pages)
│   ├── index.html
│   ├── solutions.html
│   ├── 404.html
│   ├── lessons/
│   │   ├── 01-getting-started.html
│   │   ├── 02-staging-and-commits.html
│   │   │   └── ... (15 lesson files)
│   └── static/
│       ├── css/style.css
│       └── js/app.js
├── *.md                       # 16 source markdown files (course content)
├── requirements.txt           # Python dependencies (markdown, Jinja2)
└── documentation/             # This documentation
    ├── project-report.md
    ├── project-report.docx
    └── README.md
```

### Technology Choices and Rationale

| Choice | Decision | Rationale |
|---|---|---|
| **Language** | Python 3 | Familiar to DevOps learners; great library ecosystem |
| **Templating** | Jinja2 | Mature, battle-tested Python templating; natural fit with Flaskecosystem |
| **Markdown** | `markdown` (PyPI) | Pure-Python; extensions for tables, fenced code, TOC |
| **Styling** | Vanilla CSS | No build step, no framework lock-in, full control over design system |
| **Interactivity** | Vanilla JS | Zero dependencies, works offline, fast initial load |
| **Hosting** | GitHub Pages | Free, reliable, native CI/CD integration |
| **Deployment** | GitHub Actions | First-party, no external service needed |

### Build Pipeline

The pipeline is a single Python script: [`site-src/build.py`](site-src/build.py).

```
*.md source files
    │
    ▼
[build.py — Lesson Discovery]
    │
    ▼
[Markdown → HTML conversion]
  - Link rewriting (.md → .html)
  - Fenced code blocks
  - Tables
  - Auto TOC generation
    │
    ▼
[Jinja2 Template Rendering]
  - base.html + index.html  → docs/index.html
  - base.html + lesson.html → docs/lessons/*.html (×15)
  - base.html + lesson.html → docs/solutions.html
  - base.html + static content → docs/404.html
    │
    ▼
[Static Asset Copy]
  site-src/static/ → docs/static/
    │
    ▼
docs/  (GitHub Pages serves this folder)
```

---

## Section 3: Design System

### Pinterest-Inspired Design Philosophy

The visual language draws from Pinterest's warm, approachable aesthetic applied to educational content:

- **Warm neutral background** (`#fdf6f0`) — cream/parchment feel, easier on the eyes than pure white
- **Card-based content** — each lesson rendered as an independent, hoverable card with elevation
- **Color-coded section bars** — gradient top-border on cards signals which course section a lesson belongs to
- **Generous white space** — 28px page padding, 20px card gaps, soft 12px border radius
- **Playful accent** — 🌶️ brand icon, emoji section markers, progress ring on homepage

### Color Palette

| Token | Hex | Usage |
|---|---|---|
| `--primary` | `#e76f51` | CTAs, links, card accents, active nav borders |
| `--primary-dark` | `#d45735` | Hero gradient, link hover states |
| `--secondary` | `#2a9d8f` | Intermediate section gradient start |
| `--accent` | `#e9c46a` | Visited status dots, blockquote borders |
| `--success` | `#52b788` | Completed status, marked-complete button |
| `--bg` | `#fdf6f0` | Page background |
| `--bg-card` | `#ffffff` | Card, sidebar, header surfaces |
| `--text` | `#264653` | Body text, headings |
| `--text-light` | `#6b7b8c` | Meta text, timestamps, captions |
| `--border` | `#e8e0d8` | Dividers, card borders |
| `--code-bg` | `#2d2d2d` | Code block background (dark) |
| `--code-text` | `#f8f8f2` | Code block text (light) |

### Section Gradient Colors

| Section | Gradient |
|---|---|
| Core Git (1–4) | `linear-gradient(90deg, #e76f51, #f4a261)` — warm red to orange |
| Intermediate (5–9) | `linear-gradient(90deg, #2a9d8f, #8ab17d)` — teal to sage |
| Advanced (10–14) | `linear-gradient(90deg, #264653, #2a9d8f)` — dark teal to teal |
| Capstone (15) | `linear-gradient(90deg, #e9c46a, #e76f51)` — gold to red |

### Typography

- **Body font:** `Inter` (Google Fonts) — modern, highly readable, professional
  - Fallback: `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`
- **Mono font:** `JetBrains Mono` (Google Fonts) — developer-friendly, clear in dark backgrounds
  - Fallback: `'Fira Code', 'Courier New', monospace`
- **Scale:** `clamp()` for fluid headings (e.g., hero title scales from 2.5rem to 4.5rem)
- **Line height:** 1.7 for body, 1.1–1.3 for headings

### Layout Patterns

**Sidebar Navigation**
- Fixed left sidebar, 280px wide
- Sticky header with brand logo and close button (mobile)
- Nav items show: lesson number badge, title, status dot
- Sections: Core Git → Intermediate → Advanced → Capstone & Reference

**Masonry-Style Card Grid**
- CSS Grid: `grid-template-columns: repeat(auto-fill, minmax(280px, 1fr))`
- Each card: number badge, read-time, title, description excerpt, Start button, status dot
- Hover lifts card 4px with shadow deepening

**Lesson Page Layout**
- Two-column: sticky TOC sidebar (220px) + lesson body
- Below 900px: TOC stacks above content
- Below 768px: sidebar becomes a slide-in drawer with overlay
- Prev/Next navigation at bottom

### Responsive Design Approach

| Breakpoint | Changes |
|---|---|
| 900px | TOC moves from sticky sidebar to stacked block above content |
| 768px | Sidebar collapses to slide-in drawer; hamburger menu appears in header |
| 768px+ | Overlay hidden; hamburger hidden; sidebar always visible at full width |

---

## Section 4: LMS Features

### Progress Tracking with localStorage

All progress data lives in the browser's `localStorage` under the key `git-kimchi-progress`:

```json
{
  "visited": { "1": true, "2": true },
  "completed": { "1": true }
}
```

The [`app.js`](site-src/static/js/app.js) `loadProgress()` / `saveProgress()` helpers persist this. Progress is read on every page load to update:

- **Header progress bar** — visible on lesson pages, shows `X / 15` and animated fill bar
- **Homepage ring chart** — SVG circle with `stroke-dashoffset` animation showing percentage
- **Sidebar status dots** — gray (unseen), yellow (visited), green (completed)
- **Card status dots** — same visual language as nav dots
- **Mark Complete button** — toggles between outlined and filled green states

### Lesson Navigation and Breadcrumbs

Each lesson page renders a breadcrumb trail: `Home › Lesson Title`. Lesson pages also show a sticky table of contents (TOC) generated automatically by the Python Markdown renderer from H2/H3 headings. The TOC uses `IntersectionObserver` to highlight the currently-visible section as the user scrolls.

### Completion Marking

The "Mark Complete" button at the bottom of every lesson page:
1. Reads the current `data-lesson` attribute (lesson number as string)
2. Toggles the `completed` key in localStorage
3. If marking complete, also sets `visited`
4. Updates all UI elements to reflect new state

This requires **no server, no account, no backend**.

### Mobile Navigation

Below 768px, the sidebar slides in from the left as a drawer:
- A `.sidebar-overlay` div covers the page with a semi-transparent backdrop
- Clicking the overlay or the `×` close button dismisses the drawer
- The hamburger button in the header opens it
- `document.body.style.overflow = 'hidden'` prevents background scroll while open

### Back-to-Top Functionality

A fixed circular button (bottom-right, 28px from edges) appears after the user scrolls 300px. Clicking it smoothly scrolls to `top: 0`. It uses `passive: true` scroll listener for performance.

---

## Section 5: Build System

### How `build.py` Works

The script at [`site-src/build.py`](site-src/build.py) is the single build orchestrator. Run with:

```bash
python site-src/build.py
```

It performs the following steps:

1. **Setup** — Ensure `docs/` and `docs/lessons/` directories exist; configure Jinja2 `Environment` with `FileSystemLoader` pointing to `site-src/templates/`

2. **Lesson Discovery** — Use `Path.glob("*.md")` to find all markdown files in the repo root (excluding `README.md`). Sort them.

3. **Metadata Extraction** — For each lesson file, extract:
   - **Title** — first `^# .+$` regex match (first H1)
   - **Description** — first paragraph after the H1, stripped of markdown formatting, truncated at 160 chars
   - **Read time** — word count ÷ 200 wpm, minimum 1 minute
   - **Number** — leading integer from filename (e.g., `05-branching.md` → `5`)
   - **Section** — mapped from number ranges: 1–4=core, 5–9=intermediate, 10–14=advanced, 15=capstone

4. **Link Rewriting** — Call `convert_md_links(text, context)` which rewrites markdown link targets:
   - `./00-index.md` → `index.html` (on index pages) or `../index.html` (on lesson pages)
   - `./XX-name.md` → `lessons/XX-name.html` (on index) or `XX-name.html` (on lessons)
   - `./99-solutions.md` → `solutions.html`
   - External links (not starting with `./` or `../`) are left untouched

5. **Markdown Rendering** — Feed the rewritten markdown to Python `markdown.Markdown()` with extensions: `tables`, `fenced_code`, `toc`, `nl2br`. Returns HTML body and TOC HTML.

6. **Template Context Assembly** — Build a context dict per page type with all variables needed by each Jinja2 template (paths, nav lists, lesson data, etc.)

7. **HTML Output** — Render each template with its context; write to `docs/`

8. **Static Asset Copy** — Delete and recreate `docs/static/` by copying `site-src/static/` recursively

9. **Summary** — Print build statistics

### Static Asset Handling

The `copy_static_assets()` function removes any existing `docs/static/` directory and copies the entire `site-src/static/` tree fresh on every build. Both the CSS and JS files retain their original names and are referenced via relative paths computed from the template context (`css_path`, `js_path` vary by page depth).

---

## Section 6: CI/CD Pipeline

### GitHub Actions Workflow Overview

Two workflow files under [`.github/workflows/`](.github/workflows/):

#### [`pages.yml`](.github/workflows/pages.yml) — Build and Deploy

**Trigger:** Push to `main` branch

```
1. Checkout code
2. Set up Python 3.11
3. pip install -r requirements.txt
4. python site-src/build.py
5. test -f docs/index.html          ← verification gate
6. Upload pages-artifact (path: docs/)
7. Deploy to GitHub Pages           ← only on successful push to main
```

#### [`verify.yml`](.github/workflows/verify.yml) — Pull Request Verification

**Trigger:** Pull requests targeting `main`

```
1. Checkout code
2. Set up Python 3.11
3. pip install -r requirements.txt
4. python site-src/build.py
5. test -f docs/index.html          ← fails the PR if build is broken
```

### Build Verification on PRs

The `verify.yml` workflow ensures that every pull request is tested: the build script runs, and the presence of `docs/index.html` is asserted. If the build fails or the file is missing, the workflow exits non-zero, blocking the PR from merging.

### Automatic Deployment on Push to Main

When a commit lands on `main`, `pages.yml` runs both the `build` job and the `deploy` job. The `deploy` job uses `actions/deploy-pages@v4` and requires the `github-pages` environment. The `pages: write` and `id-token: write` permissions allow the Actions runner to obtain an OIDC token for authentication.

### Pages Configuration

The deployment targets GitHub Pages serving from the `/docs` folder of the `main` branch. This is configured in **Settings → Pages → Source → GitHub Actions** (not the deprecated branch/file source option).

---

## Section 7: Deployment

### GitHub Pages Setup Instructions

1. **Enable GitHub Pages**
   - Go to **Settings → Pages**
   - Under "Build and deployment", select **Source: GitHub Actions**

2. **Push to `main`**
   - The first push to `main` triggers `pages.yml` automatically
   - The `deploy` job waits for the `build` job and the `github-pages` environment approval (if required)

3. **Find Your Site URL**
   - After deployment, the URL is shown in the Actions run summary: `https://<username>.github.io/git-kimchi/`
   - Or in **Settings → Pages** as the live URL

### Custom Domain Configuration (Optional)

To use a custom domain (e.g., `gitkimchi.example.com`):

1. In your DNS provider, add a `CNAME` record pointing `<subdomain>` to `gregodprogrammer.github.io`
2. In **Settings → Pages → Custom Domain**, enter your domain name
3. GitHub will automatically request an SSL certificate via Let's Encrypt
4. The `docs/CNAME` file in the repo (if present) is served as a bare domain token

### Troubleshooting Common Issues

| Symptom | Likely Cause | Fix |
|---|---|---|
| Build succeeds but site shows 404 | Wrong Pages source setting | Set Pages source to "GitHub Actions", not "branch" |
| `pages.yml` deploy job skipped | Not on `main` branch | Deploy only runs on push to `main`; check branch name |
| `localStorage` not persisting | Privacy/incognito mode | Expected behavior — progress lost in private browsing |
| Lesson links 404 on local preview | Relative path issue | Always preview via a local HTTP server, not `file://` |
| Fonts not loading | CSP or network block | Fonts served from `fonts.googleapis.com` — requires internet access |
| TOC not showing | Lesson had no H2/H3 headings | `markdown.extensions.toc` only generates TOC if headings exist |

---

## Section 8: Course Content

### Complete Lesson List

The course is organized into four sections, each building on the last.

#### Core Git (Lessons 1–4)

| # | Title | Description |
|---|---|---|
| 1 | [Getting Started with Git](site-src/templates/) | Introduction to version control, installing Git, first-time configuration |
| 2 | [Staging and Commits](site-src/templates/) | `git add`, `git commit`, commit messages, the staging area |
| 3 | [History and Diff](site-src/templates/) | `git log`, `git show`, `git diff`, reading commit history |
| 4 | [Undoing Changes](site-src/templates/) | `git checkout`, `git revert`, `git reset`, recovering from mistakes |

#### Intermediate Git & GitHub (Lessons 5–9)

| # | Title | Description |
|---|---|---|
| 5 | [Branching](site-src/templates/) | Creating branches, switching with `git checkout`/`git switch`, branch listing |
| 6 | [Merging](site-src/templates/) | Fast-forward merges, three-way merges, merge conflicts and resolution |
| 7 | [Remotes](site-src/templates/) | `git remote`, `git fetch`, `git pull`, `git push`, tracking branches |
| 8 | [GitHub Repositories and Forks](site-src/templates/) | GitHub UI, forking workflow, syncing forks, pull from upstream |
| 9 | [Pull Requests and Issues](site-src/templates/) | Opening PRs, PR review process, issue tracking, task management |

#### Advanced / DevOps (Lessons 10–14)

| # | Title | Description |
|---|---|---|
| 10 | [Code Review](site-src/templates/) | Why code review matters, reviewing in GitHub, inline comments, approval workflows |
| 11 | [Branching Strategies](site-src/templates/) | GitHub Flow, GitFlow, trunk-based development, choosing a strategy |
| 12 | [GitHub Pages](site-src/templates/) | Hosting static sites on GitHub, enabling Pages, custom domains |
| 13 | [Git Hooks](site-src/templates/) | Client-side and server-side hooks, `pre-commit`, `pre-push`, automation |
| 14 | [Self-Hosted Git](site-src/templates/) | Gitea, GitLab self-hosted, SSH key management, enterprise workflows |

#### Capstone & Reference (Lessons 15)

| # | Title | Description |
|---|---|---|
| 15 | [Capstone Mini-Project](site-src/templates/) | End-to-end project applying all learned concepts |
| — | [Consolidated Solutions](site-src/templates/) | All exercise solutions in one place for reference |

### Section Organization Rationale

The progression follows a deliberate learning arc:
1. **Core** establishes fundamentals (install, configure, commit, read history)
2. **Intermediate** introduces collaboration (branching, merging, remotes, GitHub)
3. **Advanced** builds production skills (code review, branching strategies, hosting, automation)
4. **Capstone** synthesizes everything in one real project

---

## Section 9: Future Enhancements

The following features are planned or considered for future iterations:

### Search Functionality

- **Approach:** Static search index generated at build time (JSON list of lesson titles + headings + excerpts)
- **UI:** Search modal triggered by `Cmd/Ctrl+K` keyboard shortcut
- **Library:** FlexSearch or Pagefind for client-side fuzzy search with zero server dependency
- **Status:** Not yet implemented

### Quiz Integration

- **Approach:** JSON quiz files per lesson, rendered as interactive multiple-choice or fill-in-the-blank
- **Scoring:** Quiz results stored in `localStorage` alongside lesson progress
- **UI:** Expandable quiz section at the bottom of each lesson page, collapsible
- **Status:** Not yet implemented

### User Accounts

- **Approach:** GitHub OAuth via GitHub Apps — users sign in and their progress syncs across devices
- **Storage:** PostgreSQL database (self-hosted or managed) via a lightweight backend
- **Alternatives:** Firebase Auth or Supabase for faster initial implementation
- **Status:** Not yet implemented; would require a backend service

### Dark Mode Toggle

- **Approach:** CSS custom properties (already partially set up) for color tokens; toggle adds `.dark` class to `<body>`; persist preference in `localStorage`
- **Complexity:** Low — primarily involves defining a dark palette and adding a toggle button in the header
- **Status:** Not yet implemented

---

## Section 10: References & Links

### Source Files

| File | Description |
|---|---|
| [site-src/build.py](site-src/build.py) | Python static site generator — main build script |
| [site-src/templates/base.html](site-src/templates/base.html) | Base HTML layout with sidebar, header, footer |
| [site-src/templates/index.html](site-src/templates/index.html) | Homepage template with hero, card grid |
| [site-src/templates/lesson.html](site-src/templates/lesson.html) | Lesson page template with TOC, nav, actions |
| [site-src/static/css/style.css](site-src/static/css/style.css) | Full design system CSS (20.7 KB) |
| [site-src/static/js/app.js](site-src/static/js/app.js) | All client-side JavaScript (9.3 KB) |
| [requirements.txt](requirements.txt) | Python dependencies: `markdown>=3.5`, `Jinja2>=3.1` |

### GitHub Actions Workflows

| File | Purpose |
|---|---|
| [.github/workflows/pages.yml](.github/workflows/pages.yml) | Build + deploy on push to `main` |
| [.github/workflows/verify.yml](.github/workflows/verify.yml) | Build-only verification on pull requests |

### Course Content Files

| File | Lesson |
|---|---|
| [00-index.md](00-index.md) | Table of Contents |
| [01-getting-started.md](01-getting-started.md) | Getting Started with Git |
| [02-staging-and-commits.md](02-staging-and-commits.md) | Staging and Commits |
| [03-history-and-diff.md](03-history-and-diff.md) | History and Diff |
| [04-undoing-changes.md](04-undoing-changes.md) | Undoing Changes |
| [05-branching.md](05-branching.md) | Branching |
| [06-merging.md](06-merging.md) | Merging |
| [07-remotes.md](07-remotes.md) | Remotes |
| [08-github-repos-and-forks.md](08-github-repos-and-forks.md) | GitHub Repositories and Forks |
| [09-pull-requests-and-issues.md](09-pull-requests-and-issues.md) | Pull Requests and Issues |
| [10-code-review.md](10-code-review.md) | Code Review |
| [11-branching-strategies.md](11-branching-strategies.md) | Branching Strategies |
| [12-github-pages.md](12-github-pages.md) | GitHub Pages |
| [13-git-hooks.md](13-git-hooks.md) | Git Hooks |
| [14-self-hosted-git.md](14-self-hosted-git.md) | Self-Hosted Git |
| [15-capstone.md](15-capstone.md) | Capstone Mini-Project |
| [99-solutions.md](99-solutions.md) | Consolidated Solutions |

### GitHub Repository

**Repository URL:** [https://github.com/gregodprogrammer/git-kimchi](https://github.com/gregodprogrammer/git-kimchi)

### Live Site URL

> **Note:** Replace with actual deployed URL after first successful GitHub Actions run.
> Expected URL format: `https://gregodprogrammer.github.io/git-kimchi/`

### Design Inspiration

- **Pinterest** — Pinterest-inspired card grid and warm color palette
- **GitHub Docs** — Clear, technical documentation layout and navigation pattern
- **MDN Web Docs** — Content hierarchy, breadcrumb patterns, and code block styling
- **CSS Tricks** — IntersectionObserver-based TOC tracking pattern

### Technologies Used

| Technology | Version/Notes |
|---|---|
| Python | 3.11 (specified in GitHub Actions) |
| Jinja2 | >= 3.1 |
| markdown (Python) | >= 3.5 |
| Inter font | via Google Fonts |
| JetBrains Mono | via Google Fonts |
| GitHub Pages | Free hosting from `/docs` |
| GitHub Actions | Ubuntu-latest runners |