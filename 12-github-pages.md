# GitHub Pages

[← Previous: Branching Strategies](./11-branching-strategies.md) | [← Back to Index](./00-index.md)

GitHub Pages is GitHub's free static site hosting service. It turns a repository into a live website with no servers to manage, no infrastructure costs, and automatic HTTPS. This makes it the default choice for project documentation, portfolios, and any developer content that lives alongside source code.

---

## What is GitHub Pages?

GitHub Pages takes files from a GitHub repository and publishes them as a website. The site rebuilds automatically every time you push to the linked branch. It is:

- **Free** — no paid plans required for public repositories
- **Automatic** — push triggers a rebuild, no manual deploy steps
- **Simple** — no database, no server configuration, no runtime
- **Version-controlled** — your site content is in Git, with full history

Because GitHub Pages serves **static files**, it works best for sites that do not require server-side logic. Think documentation, READMEs rendered as web pages, portfolios, and landing pages. It does not run Node.js, Ruby, Python, or any backend — it runs Jekyll, a static site generator.

---

## Types of GitHub Pages Sites

GitHub Pages supports two hosting patterns. The difference matters for URL structure and repository naming rules.

### User Site

A user site lives in a repository named `username.github.io`. When you enable Pages on that repository, GitHub publishes it at:

```
https://username.github.io
```

You are limited to **one user site** — it must be the `username.github.io` repo associated with your account.

### Project Site

Any other repository can host a project site. GitHub publishes it at:

```
https://username.github.io/repo-name/
```

You can have **unlimited project sites**, one per repository.

### URL Comparison

| Repository Name | Site Type | Published URL |
|---|---|---|
| `johndoe.github.io` | User site | `https://johndoe.github.io` |
| `my-api-docs` | Project site | `https://johndoe.github.io/my-api-docs/` |
| `portfolio` | Project site | `https://johndoe.github.io/portfolio/` |

The repository containing your actual project source code **does not** need to match the site URL. You can keep your code private in `my-api-docs` while publishing docs from a `my-api-docs-docs` repository if you prefer separation.

---

## Setting Up from a Branch

The simplest Pages deployment uses a dedicated branch as the site source. GitHub reads the branch contents and publishes them directly.

### Step-by-Step Setup

1. **Go to your repository** on GitHub.com
2. Click the **Settings** tab (the gear icon)
3. In the left sidebar, click **Pages**
4. Under **Build and deployment**, confirm **Source** is set to **Deploy from a branch**
5. Select your **branch**:
   - `main` — the most common choice for project sites
   - `gh-pages` — a convention for dedicated documentation branches
6. Select the **folder** to publish:
   - `/ (root)` — publishes the entire branch root
   - `/docs` — publishes only the `docs/` folder within the branch

   Using `/docs` keeps site files alongside source code in a subdirectory rather than cluttering the repository root.
7. Click **Save**

After a minute or two, GitHub activates Pages and shows the live URL in a green banner at the top of the Settings → Pages panel.

### UI Path Reference

```
Settings → Pages → Source: Deploy from a branch
                                         ├── Branch: [main] ▼
                                         └── Folder: [/ (root)] ▼
```

### Branch and Folder Combinations

| Branch | Folder | Use Case |
|---|---|---|
| `main` | `/ (root)` | Single-purpose repos where root contains only site content |
| `main` | `/docs` | Code repo where `docs/` folder contains the site |
| `gh-pages` | `/ (root)` | Dedicated docs repository; source code lives elsewhere |

---

## Creating a Simple Site

Once Pages is enabled on a branch and folder, any HTML or Markdown file in that location becomes part of the site.

### What GitHub Pages Serves

GitHub Pages serves files exactly as they exist in the published branch and folder. An `index.html` in the root of the branch becomes the homepage. A `README.md` with YAML front matter becomes a fully rendered page.

### Workflow: Serving a Markdown File

If you already have a `README.md` in your repository and your Pages source is set to the root of `main`, that README can become your website homepage with minimal changes.

```bash
# Clone or navigate to your repository
git clone https://github.com/yourname/your-repo.git
cd your-repo

# Create a simple index page using Markdown
cat > index.md << 'EOF'
---
title: Welcome to My Site
---

# Hello, World!

This page is served from a Markdown file in GitHub Pages.
EOF

# Commit and push to the branch that powers GitHub Pages
git add index.md
git commit -m "Add GitHub Pages homepage"
git push origin main
```

After pushing, wait 1–2 minutes for the site to build, then visit:

```
https://yourname.github.io/repo-name/
```

### Jekyll Auto-Conversion

GitHub Pages processes Markdown files through **Jekyll** automatically. Jekyll reads YAML front matter at the top of a file (the `---` delimiters) and converts the rest from Markdown to HTML. This means `index.md` with valid front matter becomes `index.html` on the live site — no build pipeline needed on your side.

If you push a plain HTML file, Jekyll passes it through unchanged. Either approach works.

---

## Jekyll Basics (Conceptual)

Jekyll is a static site generator that GitHub Pages runs server-side on every push. Understanding its basic conventions lets you control page titles, choose themes, and organize content without installing Jekyll locally.

### How Jekyll Works

When you push to the Pages branch, GitHub:

1. Detects a Jekyll site (presence of `_config.yml` or Markdown files)
2. Runs Jekyll to convert Markdown to HTML
3. Applies the configured theme's templates and styles
4. Publishes the generated HTML

This means you do not need to run `jekyll build` yourself. GitHub handles it.

### Front Matter

Front matter is YAML metadata at the top of a file, between two `---` lines:

```markdown
---
title: My Page Title
layout: default
---
```

Front matter variables Jekyll reads:

| Variable | Effect |
|---|---|
| `title` | Sets the page `<title>` tag and often appears in the theme |
| `layout` | Which theme template wraps the page content |
| `permalink` | Overrides the default URL path for this file |

Every page you want Jekyll to process needs front matter. Even an empty block `---` above the content is enough to trigger Jekyll processing:

```markdown
---
---
# This heading is now rendered by Jekyll
```

### The _config.yml File

The `_config.yml` file in your site root configures Jekyll globally. It sets the theme, site title, description, and URL:

```yaml
title: My Developer Portfolio
description: A showcase of projects and writing
theme: minimal
url: "https://yourname.github.io"
```

GitHub Pages supports a fixed list of built-in themes:

| Theme Name | Gem Name |
|---|---|
| Minimal | `minimal` |
| Cayman | `cayman` |
| Slate | `slate` |
| Tactile | `tactile` |
| Merlot | `merlot` |
| Architect | `architect` |
| Dinky | `dinky` |

You enable a theme by setting `theme: name` in `_config.yml` where `name` is the gem name from the table above. GitHub Pages handles the rest.

### File Organization

Jekyll treats directories with special names as having specific purposes:

| Directory | Purpose |
|---|---|
| `_layouts/` | HTML wrappers that wrap each page's content |
| `_includes/` | Reusable HTML snippets (headers, footers, sidebars) |
| `_posts/` | Blog posts, named `YYYY-MM-DD-title.md` |
| `_drafts/` | Unpublished posts, not rendered unless built locally |
| `css/` | CSS files, merged into the site output |

For a simple documentation or portfolio site, you rarely need any of these beyond placing Markdown files in the root. Jekyll's defaults handle everything.

### Building Locally (Optional)

While GitHub runs Jekyll for you, installing it locally lets you preview changes before pushing. Install Ruby and Bundler, then:

```bash
# Clone your repository
git clone https://github.com/yourname/your-repo.git
cd your-repo

# Install Jekyll and dependencies
gem install bundler
bundle install

# Serve locally (auto-rebuilds on file changes)
bundle exec jekyll serve
```

The preview site appears at `http://localhost:4000`. This is entirely optional — GitHub Pages always rebuilds on push, so local previewing is a convenience, not a requirement.

---

## Custom Domains (Conceptual)

GitHub Pages supports custom domains so your site can live at `docs.yourproject.com` instead of `yourname.github.io`.

### What You Need

1. **A CNAME file** — placed in the root of your Pages branch, it contains your custom domain as plain text:

   ```text
   docs.yourproject.com
   ```

2. **DNS records** — your DNS provider must point the domain to GitHub's servers:

   - For `yourproject.com`: an **A record** pointing to GitHub's IPs, or an **ALIAS record** to `yourname.github.io`
   - For a subdomain like `docs.yourproject.com`: a **CNAME record** pointing to `yourname.github.io`

3. **HTTPS** — GitHub Pages automatically provisions a Let's Encrypt certificate once the DNS change propagates and the domain is verified via the CNAME file. This process can take up to 24 hours.

Enabling a custom domain is a one-time configuration in Settings → Pages. The CNAME file persists in your repository, so it survives future pushes.

---

## Checking Pages Status

After enabling Pages and pushing content, you verify that the site is live in two places.

### In the Repository Settings

Go to **Settings → Pages**. GitHub displays:

- The **green checkmark** and status message when the site is published
- The **live URL** (clickable) where your site is published
- The **last deploy time** showing when GitHub last rebuilt the site

If the build fails, GitHub shows an error message here with details about what went wrong (a broken Markdown file, invalid front matter, etc.).

### From the Command Line

GitHub CLI can open the Pages URL directly:

```bash
# Open the published GitHub Pages URL in your browser
gh repo view --web
```

If your repository has Pages enabled, the Pages URL is shown at the top of the repo view page.

### Common Status Issues

| Symptom | Likely Cause | Fix |
|---|---|---|
| Page shows 404 after push | Wrong branch or folder selected in Settings | Re-check Settings → Pages → Source |
| "Page build failure" email | Syntax error in `_config.yml` or invalid front matter | Check Settings → Pages for error details |
| Stale content | Build is still in progress | Wait 1–2 minutes after push |
| Custom domain shows 404 | DNS records not yet propagated | Wait up to 24 hours for DNS |

---

## Exercise

### Scenario

You want to publish a simple documentation page for a new open-source tool called `git-fruit`. You will:

1. Create a new **public** repository on GitHub
2. Enable GitHub Pages using the **main branch root** as the source
3. Create an `index.md` file with proper Jekyll front matter
4. Push and verify the live site loads

### Tasks

1. Create the repository `git-fruit` on GitHub (use your own username in the remote URL)
2. Clone it locally
3. Create an `index.md` with a heading, a short description, and at least one section
4. Enable GitHub Pages from Settings → Pages, source: `main` branch, folder: `/ (root)`
5. Push the changes
6. Verify the site is live by checking the URL

---

## Solution

### Step 1: Create the Repository

```bash
# Replace YOUR_USERNAME with your GitHub username
gh repo create git-fruit --public --clone
```

```text
✓ Created repository YOUR_USERNAME/git-fruit
✓ Cloned repository
```

```bash
cd git-fruit
```

### Step 2: Create the index.md File

```bash
cat > index.md << 'EOF'
---
title: git-fruit
description: A delightful Git extension for tracking project milestones
---

# Welcome to git-fruit

**git-fruit** is a fictional Git extension that helps you track project milestones directly in your commit history using annotated tags.

## Features

- Lightweight milestone tracking via annotated tags
- Automatic changelog generation
- Integration with standard Git workflows

## Quick Start

```bash
git fruit init
git fruit milestone "v1.0.0"
git fruit log
```

For full documentation, visit the project README.
EOF
```

```bash
git add index.md
git commit -m "Add GitHub Pages homepage"
```

```text
[main (root-commit) a1b2c3d] Add GitHub Pages homepage
 1 file changed, 1 insertion(+)
```

### Step 3: Enable GitHub Pages

Open Settings → Pages in your browser:

```bash
gh repo view --web
```

Navigate to **Settings → Pages**. Set:
- **Source**: Deploy from a branch
- **Branch**: `main`
- **Folder**: `/ (root)`

Click **Save**. GitHub will show the Pages URL after a moment.

### Step 4: Push and Wait

```bash
git push origin main
```

```text
Enumerating objects: 3, done.
Counting objects: 100%
Writing objects: 100%
To https://github.com/YOUR_USERNAME/git-fruit.git
   a1b2c3d..d4e5f6  main -> main
```

### Step 5: Verify the Site

```bash
# Wait about 1-2 minutes for GitHub to build, then open the Pages URL
echo "Your site will be at: https://YOUR_USERNAME.github.io/git-fruit/"
```

```text
Your site will be at: https://YOUR_USERNAME.github.io/git-fruit/
```

Visit that URL in your browser. You should see the rendered Markdown page with:
- The title from the `title` front matter variable
- Your heading and section content styled by the theme

### What You Just Did

You created a GitHub repository, added a single Markdown file with Jekyll front matter, enabled GitHub Pages from the main branch, and pushed. GitHub automatically detected the Markdown file, processed it through Jekyll, and published it as a live website — no servers, no builds, no cost.

---

## Key Takeaways

- **GitHub Pages** serves static files from any GitHub repository, free of charge for public repos
- **User sites** use `username.github.io` as the canonical URL; **project sites** append the repository name
- Enabling Pages is a Settings → Pages click-through; no CLI required
- **Jekyll** runs server-side on GitHub — front matter (`---`) on any Markdown file triggers Jekyll processing
- `_config.yml` controls the theme and site-wide settings; built-in themes include `minimal`, `cayman`, and `slate`
- Pages rebuilds automatically on every push; wait 1–2 minutes before checking the live URL
- **Custom domains** are configured via a `CNAME` file in the repository root plus DNS records

---

[Next: Git Hooks →](./13-git-hooks.md)