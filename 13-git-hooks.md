# Git Hooks

Git hooks are scripts that Git executes automatically before or after specific events such as commits, pushes, and merges. They live in the `.git/hooks/` directory of every Git repository and let you automate tasks, enforce policies, and improve code quality without manual intervention.

[← Back to Index](./00-index.md) | [← Previous: GitHub Pages](./12-github-pages.md) | [Next: Self-Hosted Git →](./14-self-hosted-git.md)

---

## What Are Git Hooks?

When you initialize a Git repository with `git init`, Git populates a special directory:

```bash
ls -la .git/hooks/
```

```text
.total 8
drwxr-xr-x 12 codespace  4096 Jun 13 10:00  .
drwxr-xr-x 14 codespace  4096 Jun 13 10:00  .
drwxr-x 8 codespace  4096 Jun 13 10:00  .
drwxr-xr-x  1 codespace  4096 Jun 13 10:00  applypatch-msg.sample
drwxr-xr-x  1 codespace  4096 Jun 13 10:00  commit-msg.sample
drwxr-xr-x  1 codespace  4096 Jun 13 10:00  post-update.sample
drwxr-xr-x  1 codespace  4096 Jun 13 10:00  pre-applypatch.sample
drwxr-xr-x  1 codespace  4096 Jun 13 10:00  pre-commit.sample
drwxr-xr-x  1 codespace  4096 Jun 13 10:00  pre-merge-commit.sample
drwxr-xr-x  1 codespace  4096 Jun 13 10:00  pre-push.sample
drwxr-xr-x  3 codespace  4096 Jun 13 10:00  pre-rebase.sample
drwxr-xr-x  1 codespace  4096 Jun 13 10:00  prepare-commit-msg.sample
```

Git ships these as `.sample` files — inactive by default. To activate a hook, remove the `.sample` suffix and make the file executable:

```bash
mv .git/hooks/pre-commit.sample .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

### Key Properties of Git Hooks

| Property | Description |
|----------|-------------|
| **Location** | Stored in `.git/hooks/` — not version-controlled |
| **Not copied on clone** | Hooks exist only in the local `.git` directory |
| **Blocking** | A non-zero exit code aborts the operation |
| **Client-side only (by default)** | GitHub does not execute custom client hooks on its servers |
| **Language-agnostic** | Can be written in any scripting language (Bash, Python, Node.js, etc.) |

---

## Client-Side Hooks

Client-side hooks run on your local machine. They are triggered by operations you perform in your repository.

### pre-commit — The Most Important Hook

The `pre-commit` hook runs before `git commit` is finalized, after you stage your changes. This is your first line of defense against bad commits.

**Use cases:**
- Run linters (ESLint, Prettier, ShellCheck)
- Run unit tests
- Prevent commits containing secrets, API keys, or passwords
- Block `TODO` or `FIXME` comments in code
- Enforce file naming conventions

If the script exits with a non-zero code, the commit is aborted.

```bash
git commit -m "Add new feature"
# pre-commit hook runs here
# If it returns 0 → commit proceeds
# If it returns non-zero → commit is BLOCKED
```

### prepare-commit-msg — Edit the Commit Message Template

This hook runs before the commit message editor opens, and before the default message is generated. It receives the commit message file path as an argument.

**Use cases:**
- Auto-insert the current Git branch name
- Pre-fill the issue or ticket number from the branch name
- Add a standardized template

```bash
# Example: Extract issue number from branch name "feature/PROJ-123-add-login"
# and inject it into the commit message
```

### commit-msg — Validate Commit Message Format

The `commit-msg` hook runs after you save the commit message but before the commit is created. It receives the message file path.

**Use cases:**
- Enforce Conventional Commits format (`feat:`, `fix:`, `docs:`)
- Ensure every commit references a ticket number
- Block empty commit messages

```bash
# Conventional Commits check example
# Valid: feat: add user authentication
# Invalid: fixed the thing
```

### post-commit — Notifications and Auditing

This hook runs after the commit is created successfully. It cannot block anything — the commit has already happened.

**Use cases:**
- Send notifications (Slack, email) after each commit
- Update external issue trackers
- Trigger CI builds locally

### pre-push — Final Safety Check Before Push

The `pre-push` hook runs during `git push`, before objects are sent to the remote. It receives the remote name and URL.

**Use cases:**
- Run the full test suite before pushing
- Block pushes to `main` directly (enforce code review policy)
- Check that local branch name matches remote naming conventions

```bash
git push origin feature/my-branch
# pre-push hook runs here
# Run tests, block if tests fail
# If blocked → push does NOT happen
```

### post-merge — Restore State After a Merge

The `post-merge` hook runs after a `git merge` completes successfully. It receives a flag indicating whether the merge was a squash merge.

**Use cases:**
- Automatically install dependencies after a merge (`npm install`, `pip install -r requirements.txt`)
- Restore IDE settings or git hooks after a fresh clone via `git pull`
- Copy sample configuration files if they are missing

### pre-rebase — Prevent Rebasing Shared Branches

The `pre-rebase` hook runs before `git rebase` starts. It can prevent you from rebasing branches that others may have based work on.

**Use cases:**
- Block `git rebase` on `main` or `develop` to prevent rewriting shared history
- Warn before rebasing branches that are published

```bash
git rebase main feature/my-branch
# pre-rebase hook checks: is feature/my-branch shared?
# If shared → block the rebase
```

### Hook Execution Order Summary

```
git commit
├── pre-commit         ← Run linters, tests, block bad commits
├── prepare-commit-msg ← Modify the commit message template
├── commit-msg         ← Validate the commit message format
└── post-commit        ← Notifications, after commit is complete

git push
└── pre-push           ← Run tests, block push if checks fail

git merge
└── post-merge         ← Install dependencies, restore state

git rebase
└── pre-rebase         ← Block rebasing of shared branches
```

---

## A Real pre-commit Hook: Blocking TODO/FIXME

Let's create a real `pre-commit` hook that blocks commits containing `TODO` or `FIXME` in any staged file. This is a common pattern to prevent forgotten tasks from sneaking into the codebase.

### Step 1: Create the Hook Script

```bash
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
# pre-commit hook: Block commits containing TODO or FIXME

echo "Running pre-commit hook..."

# Get the list of staged files
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM)

BLOCKED=0

for file in $STAGED_FILES; do
    # Check for TODO or FIXME in staged content
    if grep -EH "(TODO|FIXME)" "$file" 2>/dev/null; then
        echo "ERROR: Found TODO or FIXME in $file"
        echo "Please resolve all TODO/FIXME comments before committing."
        BLOCKED=1
    fi
done

if [ $BLOCKED -eq 1 ]; then
    echo "COMMIT BLOCKED by pre-commit hook."
    exit 1
fi

echo "pre-commit checks passed."
exit 0
EOF
```

### Step 2: Make It Executable

```bash
chmod +x .git/hooks/pre-commit
```

### Step 3: Verify the Hook Exists

```bash
ls -la .git/hooks/pre-commit
```

```text
-rwxr-xr-x 1 codespace  4096 Jun 13 10:00  .git/hooks/pre-commit
```

### Step 4: Test — Block a Commit with TODO

```bash
# Create a file with a TODO comment and stage it
echo "# TODO: Implement user authentication" > feature.py
git add feature.py
git commit -m "Add feature"
```

```text
Running pre-commit hook...
ERROR: Found TODO or FIXME in feature.py
Please resolve all TODO/FIXME comments before committing.
COMMIT BLOCKED by pre-commit hook.
```

The commit was **blocked**. Notice that `git commit` returned an error — the commit does not exist.

```bash
git log --oneline -1
```

```text
# No output — commit was never created
```

### Step 5: Test — Allow a Clean Commit

Remove the TODO, stage again, and commit:

```bash
# Fix the file
echo "# Implement user authentication" > feature.py
git add feature.py
git commit -m "Add feature"
```

```text
Running pre-commit hook...
pre-commit checks passed.
[main a1b2c3d] Add feature
 1 file changed, 1 insertion(+)
```

The commit succeeded. The hook passed silently when no TODO/FIXME was found.

### Important: Hooks Are NOT Copied on Clone

A critical gotcha: hooks live in `.git/hooks/`, which is **not** version-controlled. When someone clones your repository, they get an empty hooks directory:

```bash
# On a fresh clone, hooks are NOT included
git clone https://github.com/your-org/your-repo.git
ls .git/hooks/
```

```text
applypatch-msg.sample  commit-msg.sample  post-update.sample
pre-applypatch.sample  pre-commit.sample  pre-merge-commit.sample
pre-push.sample  pre-rebase.sample  prepare-commit-msg.sample
```

Only the `.sample` files ship with Git. Your custom hooks must be distributed separately — either through a bootstrap script, a tool like `pre-commit` (Python) or `husky` (Node.js), or by committing hook scripts to the repo itself (in a directory like `scripts/hooks/` that is tracked, then symlinked or copied into `.git/hooks/`).

---

## Server-Side Hooks

Server-side hooks run on the Git server, not on individual developers' machines. They control what is **accepted** into the repository.

> **Note:** GitHub and GitLab run their own server-side hooks internally, but they do **not** expose custom server-side hook scripts to users in the way self-hosted Git servers do. The hooks described here apply to self-hosted Git deployments (see [Next: Self-Hosted Git →](./14-self-hosted-git.md)).

### pre-receive — Gate at the Server Entry Point

Runs on the server when a push is received, **before** any refs are updated. All pushed commits are available for inspection.

**Use cases:**
- Enforce repository policies (branch naming, commit authorship)
- Block force-pushes to protected branches
- Validate that pushed commits match certain criteria

### update — Per-Branch Gate

Runs once for each branch being updated. Receives the branch name, the old commit hash, and the new commit hash.

**Use cases:**
- Require signed commits on specific branches
- Prevent merges that do not pass CI on the server
- Block non-fast-forward updates to `main`

### post-receive — Trigger Downstream Actions

Runs after the push is fully processed and all refs are updated. It cannot block anything.

**Use cases:**
- Trigger CI/CD pipelines (via webhook)
- Deploy code after a push to `main`
- Send email or Slack notifications
- Mirror the repository to a backup server

### Server Hook Flow

```
Developer runs: git push origin main
           │
           ▼
    ┌──────────────────┐
    │  pre-receive     │  ← Block pushes, validate all refs
    └────────┬─────────┘
             │ (if pass)
    ┌────────▼─────────┐
    │  update (main)   │  ← Per-branch check: old SHA → new SHA
    └────────┬─────────┘
             │ (if pass)
    ┌────────▼─────────┐
    │ post-receive     │  ← Trigger deployments, notifications
    └──────────────────┘
```

---

## Managing Hooks at Scale

As projects grow, managing hooks manually becomes error-prone. Two popular tools solve this:

### pre-commit (Python)

The [`pre-commit`](https://pre-commit.com/) framework is a Python-based tool that installs and manages hooks from a `.pre-commit-config.yaml` file in your repository. Hooks are versioned and distributed with the repo.

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml

  - repo: https://github.com/psf/black
    rev: 24.1.1
    hooks:
      - id: black
```

```bash
# Install pre-commit
pip install pre-commit

# Install hooks from .pre-commit-config.yaml
pre-commit install

# Run manually
pre-commit run --all-files
```

Hooks defined in `.pre-commit-config.yaml` **are** tracked in the repository, solving the "hooks not copied on clone" problem.

### husky (Node.js)

[Husky](https://typicode.github.io/husky/) is a Node.js tool that makes Git hooks easier to manage, especially for JavaScript/TypeScript projects.

```bash
# Install husky
npm install husky --save-dev

# Initialize husky in your project
npx husky init

# Add a hook
npx husky add .husky/pre-commit "npm test"
```

This creates `.husky/pre-commit`:

```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

npm test
```

The `.husky/` directory can be committed to the repository, so hooks travel with the code.

---

## Exercise

**Task:** Create a `pre-commit` hook that blocks any commit message shorter than 10 characters. The hook should:

1. Read the commit message from the file passed as the first argument (this is how `commit-msg` hooks receive the message)
2. Check if the message length (excluding whitespace) is at least 10 characters
3. Exit with code `1` (block) if too short, exit with code `0` (allow) if valid
4. Display a helpful error message when blocking

Test your hook with:
- A blocked short message (e.g., `"fix bug"`)
- An allowed longer message (e.g., `"fix: resolve null pointer on login"`)

---

## Solution

### Step 1: Create the commit-msg Hook

```bash
cat > .git/hooks/commit-msg << 'EOF'
#!/bin/bash
# commit-msg hook: Block commits with messages shorter than 10 chars

COMMIT_MSG_FILE="$1"
COMMIT_MSG=$(cat "$COMMIT_MSG_FILE")

# Remove leading and trailing whitespace
COMMIT_MSG_TRIMMED=$(echo "$COMMIT_MSG" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')

# Check length (non-whitespace characters only)
MSG_LEN=${#COMMIT_MSG_TRIMMED}

if [ $MSG_LEN -lt 10 ]; then
    echo "ERROR: Commit message too short."
    echo "  Received: '$COMMIT_MSG_TRIMMED' (${MSG_LEN} chars)"
    echo "  Minimum:  10 characters"
    echo "COMMIT BLOCKED by commit-msg hook."
    exit 1
fi

echo "Commit message check passed (${MSG_LEN} chars)."
exit 0
EOF
chmod +x .git/hooks/commit-msg
```

### Step 2: Test — Block a Short Message

```bash
git add .git/hooks/commit-msg
git commit -m "Add commit-msg hook"
```

Now test with a short message:

```bash
# Create a test file to force a non-empty commit
touch exercise-test.txt
git add exercise-test.txt
git commit -m "fix bug"
```

```text
ERROR: Commit message too short.
  Received: 'fix bug' (8 chars)
  Minimum:  10 characters
COMMIT BLOCKED by commit-msg hook.
```

```bash
git log --oneline -1
```

```text
# No new commit — blocked successfully
```

### Step 3: Test — Allow a Valid Message

```bash
git commit -m "fix bug: resolve null pointer on login"
```

```text
Commit message check passed (38 chars).
[main a1b2c3d] fix bug: resolve null pointer on login
 1 file changed, 0 insertions(+), 0 deletions(+)
```

The commit succeeded. The hook correctly allows messages of 10 or more characters.

---

## Summary

| Hook | When It Runs | Can Block? | Common Use |
|------|-------------|------------|------------|
| `pre-commit` | Before each `git commit` | Yes | Linters, tests, secret scanning |
| `prepare-commit-msg` | Before message editor opens | No | Auto-insert issue numbers |
| `commit-msg` | After message is written | Yes | Enforce commit message format |
| `post-commit` | After commit is complete | No | Notifications |
| `pre-push` | Before `git push` sends data | Yes | Run full test suite |
| `post-merge` | After `git merge` finishes | No | Install dependencies |
| `pre-rebase` | Before `git rebase` starts | Yes | Block shared branch rebases |
| `pre-receive` | Server-side: push arrives | Yes | Enforce server policies |
| `update` | Server-side: per branch | Yes | Require signed commits |
| `post-receive` | Server-side: push complete | No | Trigger deployments |

Remember: **hooks are local and not copied on clone**. Use `pre-commit`, husky, or a bootstrap script to distribute hooks across a team.

[← Back to Index](./00-index.md) | [← Previous: GitHub Pages](./12-github-pages.md) | [Next: Self-Hosted Git →](./14-self-hosted-git.md)