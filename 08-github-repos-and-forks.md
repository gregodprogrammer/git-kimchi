# GitHub Repositories and Forks

[← Previous: Remotes](./07-remotes.md) | [← Back to Index](./00-index.md)

In the [Remotes](./07-remotes.md) section, you learned how to work with remote repositories using local bare repositories as stand-ins. Now it's time to use a real remote hosting service: **GitHub**. GitHub is the most popular Git hosting platform, and understanding how to create repositories, fork projects, and manage collaboration will be central to your DevOps workflow.

This section covers creating repositories on GitHub, understanding key files like README and LICENSE, using `.gitignore`, and the fork-and-sync workflow that enables contributions to open-source projects.

## Why GitHub?

GitHub hosts over 100 million repositories and is the default platform for open-source collaboration. It provides:

- **Remote storage** for your Git repositories (the "remote" you've been connecting to)
- **Web interface** for viewing code, history, and branches
- **Issue tracking** for bugs and feature requests
- **Pull Request system** for code review before merging (covered in the next section)
- **Actions** for CI/CD pipelines (covered in the Advanced DevOps section)
- **GitHub Pages** for hosting documentation or websites (covered later)

Even if your team uses GitLab or Bitbucket, the concepts on GitHub apply everywhere.

## Creating a GitHub Repository

You can create a repository in two ways: through the GitHub web interface or via the command line with GitHub CLI.

### Option 1: Via the GitHub Web Interface

**Step-by-step:**

1. Log in to GitHub at `https://github.com`
2. Click the **+** icon in the top-right corner
3. Select **New repository** from the dropdown menu
4. You'll see the Create a new repository page:
   - **Owner**: Your username (or an organization you belong to)
   - **Repository name**: Choose something descriptive (e.g., `my-webapp`, `devops-scripts`)
   - **Description**: A brief explanation of what the repo contains (optional)
   - **Visibility**: Choose **Public** (anyone can see) or **Private** (only you and collaborators can see)
   - **Add a README**: Check this to create a starter `README.md` file
   - **Add .gitignore**: Check this to select a `.gitignore` template for your language/framework
   - **Choose a license**: Optional — see the LICENSE section below

5. Click **Create repository**

**Screenshot description:**
```
┌─────────────────────────────────────────────────────────────────┐
│  GitHub Header: [Logo] [Search] [+] [Your Avatar ▼]             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   + New repository                                             │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │ Owner:    [ username ▼ ]                                 │  │
│   │ Repository name: [ _________________ ]                   │  │
│   │ Description:  [ _________________ ]                     │  │
│   │                                                     ▼    │  │
│   │ ○ Public  ● Private                                     │  │
│   │                                                     ▼    │  │
│   │ ☑ Add a README file                                     │  │
│   │ ☑ Add .gitignore: [ None ▼ ] → [Python]                 │  │
│   │ ☑ Choose a license: [ None ▼ ] → [MIT License]          │  │
│   │                                                     ▼    │  │
│   │           [ Create repository ]                         │  │
│   └─────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Option 2: Via GitHub CLI

If you prefer the terminal, GitHub CLI (`gh`) makes this seamless:

```bash
# Install GitHub CLI first (macOS)
brew install gh

# Or on Ubuntu/Debian
sudo apt install gh

# Authenticate with GitHub
gh auth login
```

```text
? What account do you want to log into?  [Use arrows to move, Enter to select]
  > GitHub.com
    GitHub Enterprise Server
```

```text
? How would you like to authenticate?  [Use arrows to move, Enter to select]
  > Login with a web browser
    Paste an authentication token
```

Once authenticated, create a repository:

```bash
# Create a new public repository with a README
gh repo create my-new-repo --public --clone

# Or create with specific options:
# --private for private repo
# --description "Your description here"
# --gitignore-template Python (or Node, Go, etc.)
# --license MIT (or Apache-2.0, GPL-3.0, etc.)

# Example: Create a Python project repo
gh repo create my-python-project \
  --public \
  --description "Python project with CI/CD setup" \
  --gitignore-template Python \
  --license MIT \
  --clone
```

```text
- Creating repository username/my-python-project on GitHub...
  ✓ Created repository username/my-python-project
  ✓ Cloned repository
  ✓ Initialized git repository
```

The `--clone` flag automatically clones the new repository into a local directory, so you're ready to start working immediately.

### What's Included When You Check "Add a README"?

A README file is the face of your repository. GitHub displays it prominently at the root of your repo. It tells visitors:

- What the project does
- How to install it
- How to use it
- How to contribute

When you initialize with a README, GitHub creates a bare-bones template. You'll customize it to fit your project.

## Cloning a Repository

"Cloning" downloads a remote repository to your local machine, including all its history and branches. After cloning, you have a fully functional local Git repository connected to its remote.

### Using `git clone`

```bash
git clone https://github.com/username/repository.git
```

```text
Cloning into 'repository'...
remote: Enumerating objects: 12, done.
remote: Counting objects: 100% (12/12), done.
remote: Compressing objects: 100% (8/8), done.
Receiving objects: 100% (12/12), done.
remote: Total 12 (delta 0), reused 0 (delta 0)
```

By default, Git creates a folder named after the repository (e.g., `repository/`). To clone into a custom folder:

```bash
git clone https://github.com/username/repository.git my-custom-folder
```

### Using `gh repo clone`

If you're authenticated with GitHub CLI, you can use `gh`:

```bash
gh repo clone username/repository
```

```text
- Cloning from https://github.com/username/repository
Cloning into 'repository'...
remote: Enumerating objects: 12, done.
```

The `gh` command also works for repositories you don't own (if they're public) and for forking workflows.

### HTTPS vs. SSH URLs

When you view a repository on GitHub, you can switch between two clone URLs:

**HTTPS:**
```
https://github.com/username/repository.git
```
- **Pros**: Works immediately on any machine, no SSH key setup needed
- **Cons**: Requires username/password or personal access token for private repos
- **Best for**: Beginners, CI/CD systems (easier authentication)

**SSH:**
```
git@github.com:username/repository.git
```
- **Pros**: No password prompts after SSH key is configured
- **Cons**: Requires generating and uploading an SSH key first
- **Best for**: Daily development on your own machines

```
┌─────────────────────────────────────────────────────────────────┐
│  On GitHub repository page:                                     │
│                                                                 │
│  ┌────────────────────┐  ┌────────────────────┐                │
│  │ CODE ▼             │  │ SSH                │                │
│  │                    │  │ git@github.com:    │                │
│  │ HTTPS   SSH  GitHub CLI │ username/repo.git │                │
│  └────────────────────┘  └────────────────────┘                │
│                                                                 │
│  Click the clipboard icon to copy the URL                       │
└─────────────────────────────────────────────────────────────────┘
```

For this tutorial, we use HTTPS URLs for simplicity. See the **Advanced Git** section for SSH key setup.

## README Files: Your Project's Front Door

The README is the first thing visitors see. A good README answers:

- **What** does this project do?
- **Why** would someone use it?
- **How** do they get started?
- **Where** can they get help?

### A README Template

Here's a template you can adapt for any project:

```markdown
# Project Name

A brief description of what this project does and who it's for.

## Features

- Feature 1: Description
- Feature 2: Description
- Feature 3: Description

## Installation

```bash
# Clone the repository
git clone https://github.com/username/repository.git

# Navigate into the directory
cd repository

# Install dependencies
pip install -r requirements.txt
# or: npm install
# or: go mod download
```

## Usage

```bash
# Example command
python main.py --option value
```

## Configuration

Explain any environment variables or configuration files needed.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to contributor 1
- Thanks to contributor 2
```

### README Best Practices

- **Keep it concise but complete** — cover the essentials without overwhelming
- **Add badges** — CI/CD status, license, version numbers
- **Include examples** — show real commands and expected output
- **Update it** — when features change, update the README too

## LICENSE Files: Legal Protection

Without a license, GitHub's default rules apply: **no one can use your code** in any meaningful way. Adding a license clarifies how others may (or may not) use your work.

### Why Licenses Matter in DevOps

In DevOps, you often:
- Use open-source tools in your pipelines
- Share automation scripts publicly
- Contribute to or maintain open-source projects

Understanding licenses helps you:
- **Avoid legal issues** — know what you can embed in proprietary code
- **Choose appropriate tools** — some licenses conflict with each other
- **Contribute properly** — many projects require a signed Developer Certificate of Origin (DCO)

### Common DevOps-Friendly Licenses

| License | Use Case | Key Terms |
|---------|----------|-----------|
| **MIT** | Most popular, extremely permissive | Can do almost anything with the code as long as you include the copyright notice |
| **Apache-2.0** | Corporate-friendly projects | Like MIT, but also grants explicit patent rights; requires NOTICE file for modifications |
| **GPL-3.0** | Strong copyleft (share-alike) | If you modify and distribute the code, you must release your version under GPL too |
| **BSD-3-Clause** | Academic/networking code | Like MIT, but forbids using contributors' names for endorsement without permission |

### Adding a License

When creating a repository on GitHub, you can select a license from the dropdown. After creation, the license file appears at the root of your repository:

```bash
# View the license file
cat LICENSE
```

```text
MIT License

Copyright (c) 2024 Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### When to Add a License

- **Public repositories**: Always add a license so people know how to use your code
- **Private repositories**: Less critical, but good practice before making public
- **Forking**: If you're modifying someone else's code, check the license first

## The `.gitignore` File: Ignoring Unnecessary Files

Not everything belongs in your repository. Generated files, secrets, and build artifacts should stay local. `.gitignore` tells Git which files to ignore.

### Common Patterns

```bash
# Environment variables (never commit secrets!)
.env

# Dependencies
node_modules/
__pycache__/
venv/
.env/

# Build artifacts
dist/
build/
*.o
*.class
*.pyc

# Logs
*.log
logs/

# IDE settings
.vscode/
.idea/
*.swp
*.swo

# OS files
.DS_Store
Thumbs.db
```

### GitHub's `.gitignore` Templates

Instead of writing from scratch, GitHub provides templates for common languages and frameworks:

```
┌─────────────────────────────────────────────────────────────────┐
│  On GitHub when creating a new repository:                      │
│                                                                 │
│  Add .gitignore: [ None ▼ ]                                     │
│                      ├── Python                                  │
│                      ├── Node                                   │
│                      ├── Go                                      │
│                      ├── Ruby                                   │
│                      ├── Rust                                   │
│                      └── ...                                     │
└─────────────────────────────────────────────────────────────────┘
```

You can also fetch templates manually:

```bash
# View available templates
gh api repos/github/gitignore/contents | jq '.[].name'

# Download a specific template
gh api repos/github/gitignore/contents/Python > .gitignore
```

### How `.gitignore` Works

When you add a file to `.gitignore`, Git pretends it doesn't exist:

```bash
# Create a .gitignore file
echo "*.log" > .gitignore

# Git status won't show *.log files
git status
```

```text
On branch main
Untracked files:
  .gitignore

nothing else to show (working tree clean)
```

Even though `debug.log` exists in the directory, Git ignores it. If a file was already tracked before you added it to `.gitignore`, you need to unstage it:

```bash
# Remove from tracking but keep the file
git rm --cached debug.log
git commit -m "Stop tracking debug.log"
```

## Forking: Contributing Without Write Access

A **fork** is your personal copy of someone else's repository, hosted under your GitHub account. You have full control over your fork — make any changes you want, no permission needed.

### Why Fork?

```
┌─────────────────────────────────────────────────────────────────┐
│           ORIGINAL REPOSITORY                                    │
│     (owned by another user or organization)                     │
│                                                                 │
│   You CANNOT push directly to this repo                         │
│   You CAN submit Pull Requests                                  │
└─────────────────────────────────────────────────────────────────┘
                            │
                            │ Fork (creates copy under YOUR account)
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│           YOUR FORK                                             │
│   (your GitHub account / your-username/repository)              │
│                                                                 │
│   You HAVE full control — push, branch, delete freely           │
└─────────────────────────────────────────────────────────────────┘
```

Forks are the foundation of GitHub's contribution model:

1. **Open-source projects** rarely give direct commit access to strangers
2. Fork the project → make changes → submit a Pull Request
3. The maintainer reviews your PR and decides whether to merge

### Option 1: Fork via GitHub Web Interface

1. Navigate to the repository you want to fork
2. Click the **Fork** button in the top-right corner
3. Select your account as the owner
4. GitHub creates a copy under your account

```
┌─────────────────────────────────────────────────────────────────┐
│  Original Repository Page:                                      │
│                                                                 │
│  [ Watch ▼ ]  [ Fork ▲ ]  [ Code ▼ ]                           │
│                                  ↑                               │
│                        Click "Fork" here                        │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Create a new fork                                       │   │
│  │                                                         │   │
│  │ Where should we fork this repository?                  │   │
│  │                                                         │   │
│  │ [ your-username ▼ ]                                     │   │
│  │                                                         │   │
│  │          [ Create fork ]                                │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### Option 2: Fork via GitHub CLI

```bash
# Fork a repository
gh repo fork owner/repository
```

```text
- Forking owner/repository...
  ✓ Created fork as your-username/repository
  ✓ Cloned repository
```

The `gh repo fork` command both forks on GitHub AND clones your fork locally. You're immediately ready to start making changes.

## Syncing a Fork: Keeping Your Fork Up-to-Date

The original repository (the "upstream") continues to evolve after you fork. To keep your fork in sync, you need to add the original as a remote and pull from it.

### The Upstream Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│  UPSTREAM (original repo)                                       │
│  owner/original-repo                                            │
│                                                                 │
│  ── commit A ── commit B ── commit C ── commit D (newer)        │
└─────────────────────────────────────────────────────────────────┘
                            │
              git remote add upstream <original-url>
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│  YOUR LOCAL REPOSITORY                                          │
│                                                                 │
│  origin  ── commit A ── commit B ── commit E (your changes)     │
│  upstream ── commit A ── commit B ── commit C ── commit D       │
│                                                                 │
│  git fetch upstream → git merge upstream/main → git push        │
└─────────────────────────────────────────────────────────────────┘
```

### Step 1: Add the Upstream Remote

```bash
# Navigate to your forked repository
cd your-fork

# Add the original repository as 'upstream'
git remote add upstream https://github.com/owner/original-repository.git

# Verify the remotes
git remote -v
```

```text
origin    https://github.com/your-username/repository.git (fetch)
origin    https://github.com/your-username/repository.git (push)
upstream  https://github.com/owner/original-repository.git (fetch)
upstream  https://github.com/owner/original-repository.git (push)
```

### Step 2: Fetch and Merge Upstream Changes

```bash
# Download commits from upstream
git fetch upstream
```

```text
remote: Enumerating objects: 8, done.
remote: Counting objects: 100% (8/8), done.
remote: Compressing objects: 100% (5/5), done.
Receiving objects: 100% (5/5), done.
```

```bash
# Switch to your main branch
git checkout main

# Merge upstream changes into your local main
git merge upstream/main
```

```text
Merge made by the 'ort' strategy.
 README.md | 2 ++
 1 file changed, 2 insertions(+)
```

### Step 3: Push to Your Fork

```bash
# Push the synced changes to your fork on GitHub
git push origin main
```

```text
Enumerating objects: 3, done.
Counting objects: 100% (3/3), done.
Writing objects: 100% (3/3), 200 bytes | 200.00 KiB/s, done.
To https://github.com/your-username/repository.git
   5a2c1d3..e7f8g9h  main -> main
```

### Pull vs. Merge for Syncing

You can also use `git pull upstream main` instead of fetch + merge:

```bash
git pull upstream main
```

```text
From https://github.com/owner/original-repository
 * branch            main       -> FETCH_HEAD
Merge made by the 'ort' strategy.
 README.md | 2 ++
 1 file changed, 2 insertions(+)
```

Both approaches work. The fetch + merge pattern gives you more visibility into what's changing.

## The Complete Fork-to-PR Workflow

Here's the full cycle for contributing to an open-source project:

```bash
# 1. Fork on GitHub (via web or gh repo fork)

# 2. Clone your fork
git clone https://github.com/your-username/repository.git
cd repository

# 3. Add upstream remote (so you can sync later)
git remote add upstream https://github.com/owner/original-repository.git

# 4. Create a feature branch (never work directly on main)
git checkout -b feature/my-contribution

# 5. Make your changes
# (edit files, add tests, etc.)

# 6. Commit your changes
git add README.md  # replace with your actual file names
git commit -m "Add my contribution"

# 7. Push to YOUR fork
git push origin feature/my-contribution

# 8. Go to GitHub and open a Pull Request
# Click "Compare & pull request" on your fork's page

# 9. After PR is merged, sync your fork:
git checkout main
git pull upstream main
git push origin main
```

You'll learn more about Pull Requests in the next section, but the key point is: **always create a branch for your changes**. This keeps your `main` clean and makes it easy to submit multiple contributions.

---

## Exercise

In this exercise, you'll create a GitHub repository from scratch, set it up with a README and `.gitignore`, then fork an existing public repository and sync it.

### Scenario

You're starting a new DevOps automation project. You've decided to host it on GitHub. After making your initial commits, you find a public repository with useful scripts that you want to incorporate. You'll fork it, explore the code, and practice the sync workflow.

### Tasks

**Part 1: Create Your Own Repository**

1. Create a new public repository on GitHub called `my-devops-scripts` with a README, Python `.gitignore`, and MIT license.

2. Clone the repository to your local machine.

3. Replace the default README with a custom one that includes:
   - Project title: "My DevOps Scripts"
   - Description: "A collection of automation scripts for CI/CD pipelines"
   - Installation section with `pip install -r requirements.txt`

4. Create a `.gitignore` file (if not created) with entries for `*.log`, `node_modules/`, and `.env`.

5. Commit and push your changes.

6. Verify on GitHub that your README and `.gitignore` appear correctly.

**Part 2: Fork and Sync**

1. Fork the repository: `https://github.com/github/gitignore` (this is GitHub's official collection of `.gitignore` templates).

2. Clone your fork locally.

3. Add the original repository as `upstream`.

4. In the upstream repo, check what branches exist and note one that looks interesting (e.g., `Python` or `Node`).

5. Fetch and merge changes from `upstream/main` into your local `main`.

6. Push the merged changes to your fork.

7. Verify on GitHub that your fork shows the latest commits from upstream.

### Success Criteria

- Your `my-devops-scripts` repository has a customized README with the specified sections
- Your `.gitignore` contains `*.log`, `node_modules/`, and `.env`
- `git log` on your fork shows commits from upstream after syncing
- `git remote -v` shows both `origin` and `upstream` remotes correctly

---

## Solution

### Part 1: Create Your Own Repository

```bash
# Using GitHub CLI to create the repository
gh repo create my-devops-scripts \
  --public \
  --description "A collection of automation scripts for CI/CD pipelines" \
  --gitignore-template Python \
  --license MIT \
  --clone
```

```text
- Creating repository username/my-devops-scripts on GitHub...
  ✓ Created repository username/my-devops-scripts
  ✓ Cloned repository
  ✓ Initialized git repository
```

```bash
# Navigate into the repo
cd my-devops-scripts

# Check what was created
ls -la
```

```text
.git
.gitignore
LICENSE
README.md
```

```bash
# Replace the default README with a custom one
cat > README.md << 'EOF'
# My DevOps Scripts

A collection of automation scripts for CI/CD pipelines.

## Installation

```bash
# Clone the repository
git clone https://github.com/username/my-devops-scripts.git

# Install dependencies
pip install -r requirements.txt
```

## Usage

Run any script from the `scripts/` directory:

```bash
python scripts/deploy.py --env production
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first.
EOF
```

```bash
# Create .gitignore with specific patterns (or verify/edit existing)
cat >> .gitignore << 'EOF'

# DevOps specific
*.log
node_modules/
.env
.env.*
```

```bash
# Check git status
git status
```

```text
On branch main
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
        modified:   README.md

Untracked files:
  .gitignore
```

```bash
# Commit and push
git add README.md .gitignore
git commit -m "Customize README and add DevOps .gitignore patterns"
git push origin main
```

```text
[main abc1234] Customize README and add DevOps .gitignore patterns
 2 files changed, 24 insertions(+), 3 deletions(-)
To https://github.com/username/my-devops-scripts.git
   def5678..abc1234  main -> main
```

### Part 2: Fork and Sync

```bash
# Fork the official gitignore repository
gh repo fork github/gitignore
```

```text
- Forking github/gitignore...
  ✓ Created fork as username/gitignore
  ✓ Cloned repository
```

```bash
# Navigate into the fork
cd gitignore

# Verify remotes
git remote -v
```

```text
origin  https://github.com/username/gitignore.git (fetch)
origin  https://github.com/username/gitignore.git (push)
```

```bash
# Add the original as upstream
git remote add upstream https://github.com/github/gitignore.git

# Verify both remotes
git remote -v
```

```text
origin    https://github.com/username/gitignore.git (fetch)
origin    https://github.com/username/gitignore.git (push)
upstream  https://github.com/github/gitignore.git (fetch)
upstream  https://github.com/github/gitignore.git (push)
```

```bash
# View available branches in upstream
git fetch upstream
git branch -r
```

```text
  upstream/main
  upstream/Python
  upstream/Node
  upstream/Terraform
  upstream/Go
```

```bash
# Check a sample of what's in the Python template
git show upstream/Python:.gitignore | head -20
```

```text
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Distribution / packaging
.Python
build/
...
```

```bash
# Sync upstream/main to your fork's main
git checkout main
git pull upstream main
```

```text
From https://github.com/github/gitignore
 * branch            main       -> FETCH_HEAD
Merge made by the 'ort' strategy.
 .gitignore | 4 ++-
 README.md  | 6 +++-
 ...
```

```bash
# Push the synced changes to your fork
git push origin main
```

```text
Enumerating objects: 15, done.
Counting objects: 100% (15/15), done.
Writing objects: 100% (15/15), 350 bytes | 350.00 KiB/s, done.
To https://github.com/username/gitignore.git
   5a2c1d3..e7f8g9h  main -> main
```

```bash
# Verify the sync worked
git log --oneline origin/main | head -10
```

```text
e7f8g9h Merge branch 'upstream/main'
a1b2c3d Update README with new contributors
...
```

You now have:
- Your own `my-devops-scripts` repository with a proper README and `.gitignore`
- A forked copy of `github/gitignore` with the upstream remote configured
- Practiced the sync workflow that you'll use for every open-source contribution

---

## Key Takeaways

| Concept | Command | When to Use |
|---------|---------|-------------|
| Create repo (CLI) | `gh repo create <name> --public --gitignore-template Python --license MIT` | When you prefer terminal workflow |
| Clone repo | `git clone <url>` or `gh repo clone owner/repo` | When starting work on a new project |
| Fork a repo | `gh repo fork owner/repo` | When you want to contribute without write access |
| Add upstream | `git remote add upstream <original-url>` | When setting up fork sync |
| Sync fork | `git fetch upstream && git merge upstream/main && git push origin main` | When keeping your fork up-to-date |
| HTTPS vs SSH | — | HTTPS for simplicity; SSH for passwordless daily use |

**Remember**: Forks are your personal copies of someone else's repository. Always add the original as `upstream` so you can sync changes. Never commit secrets to repositories — use `.gitignore` and environment variables.

---

[← Previous: Remotes](./07-remotes.md) | [Next: Pull Requests and Issues →](./09-pull-requests-and-issues.md) | [← Back to Index](./00-index.md)