# Capstone Mini-Project

[← Previous: Self-Hosted Git](./14-self-hosted-git.md) · [← Back to Index](./00-index.md)

---

This is the final project in the Git and GitHub Documentation guide. Everything you have learned in the preceding 14 sections comes together here. You will simulate a real DevOps team workflow from scratch — creating a repository, branching strategy, code review, issue tracking, GitHub Pages, a pre-commit hook, and a merge conflict resolution.

No new concepts are introduced. Every task in this project uses skills you have already practiced:

| Section | Skill Used |
|---------|-----------|
| 01 — Getting Started | `git init`, `git config`, first commit |
| 02 — Staging and Commits | `git add`, `git commit`, meaningful messages |
| 03 — History and Diff | `git log`, `git diff` |
| 04 — Undoing Changes | `git restore`, `git reset` |
| 05 — Branching | `git branch`, `git switch`, branch per feature |
| 06 — Merging | `git merge`, fast-forward vs true merge |
| 07 — Remotes | `git remote`, `git push`, `git pull` |
| 08 — GitHub Repos and Forks | GitHub web UI, SSH/HTTP clone URLs |
| 09 — Pull Requests and Issues | `gh pr create`, PR-to-issue linking |
| 10 — Code Review | PR approval, reviewing and merging |
| 11 — Branching Strategies | Feature branches, clean `main` history |
| 12 — GitHub Pages | Static site hosting from `main` branch |
| 13 — Git Hooks | Pre-commit hook with `shellcheck` |
| 14 — Self-Hosted Git | Docker-based Gitea setup |

---

## Scenario

You are a DevOps engineer joining a fictional team called **InfraCore**. The team needs a shared repository for infrastructure automation scripts. Your mission is to set up the repository and go through the full development lifecycle — from a blank GitHub repo to a live GitHub Pages site and a functioning pre-commit hook.

You will wear three hats:

- **Alice** — sets up the repository and creates the initial structure
- **Bob** — contributes a feature branch (you, playing Bob)
- **Carol** — contributes a bug-fix branch with a merge conflict (you, playing Carol)

By the end, the repository will contain:

- A meaningful commit history across multiple branches
- A merged feature branch with a linked Pull Request
- A resolved merge conflict on a bug-fix branch
- A live GitHub Pages site
- A pre-commit hook that lints shell scripts
- An issue tracker entry linked to the PR

---

## Prerequisites

Before starting, make sure you have:

- **Git 2.38 or later** installed (`git --version`)
- **A GitHub account** (free tier is fine) at [github.com](https://github.com)
- **`gh` CLI** installed and authenticated (`gh auth status`)
- **`shellcheck`** installed (`shellcheck --version`) — used by the pre-commit hook
- A web browser to interact with GitHub's web UI

All work is done from the terminal. No special infrastructure is required.

---

## Project Requirements

Complete all of the following tasks in order. Each task builds on the previous one.

### Task 1 — Create the GitHub Repository

Create a new **public** GitHub repository named `infracore-scripts`.

- Add a `README.md` with a brief project description
- Add a `.gitignore` for **Bash** (GitHub's template)
- Clone it to your local machine
- Configure Git identity (use a name and email — they can be fictional)

**Deliverable:** A clean, cloned repository on your local machine with the GitHub remote set as `origin`.

---

### Task 2 — Configure Git Identity

Set your name and email in Git's global config. Then set the same identity specifically for this repository (local config) using the name "Alice <alice@infracore.dev>".

**Deliverable:** `git config --local user.email` in the repo returns `alice@infracore.dev`.

---

### Task 3 — Create the Initial Commit

Create a `deploy.sh` shell script with the following content. Make it executable. Commit it with a meaningful message. Push to `origin main`.

```bash
#!/usr/bin/env bash
# deploy.sh — Infrastructure deployment script for InfraCore
# Usage: ./deploy.sh <environment>

set -euo pipefail

ENVIRONMENT="${1:-staging}"
echo "Deploying to ${ENVIRONMENT} environment..."

case "$ENVIRONMENT" in
  staging|production)
    echo "Deployment target validated: ${ENVIRONMENT}"
    ;;
  *)
    echo "Error: Unknown environment '${ENVIRONMENT}'" >&2
    exit 1
    ;;
esac

echo "Deployment to ${ENVIRONMENT} complete."
```

**Deliverable:** `deploy.sh` is committed, pushed, and visible in the `main` branch on GitHub.

---

### Task 4 — Open an Issue

On GitHub, create an issue titled: **"Add health-check script for all environments"**

In the body, describe the request: a new shell script `health-check.sh` that pings localhost and reports service status.

Give the issue a label of your choice (e.g., `enhancement` or `feature`).

Note the **issue number** — you will reference it in Task 5.

**Deliverable:** Issue exists on GitHub with a known number (e.g., #1).

---

### Task 5 — Create a Feature Branch

As **Bob**, create a branch called `feature/health-check` from `main`. This branch will implement the health-check script.

Switch to the branch.

**Deliverable:** `git branch` shows `feature/health-check` as the current branch.

---

### Task 6 — Make Multiple Commits on the Feature Branch

Create the `health-check.sh` script with the following content:

```bash
#!/usr/bin/env bash
# health-check.sh — Service health check for InfraCore environments
# Usage: ./health-check.sh <service-name>

set -euo pipefail

SERVICE="${1:-web}"

echo "Running health check for service: ${SERVICE}"
echo "Status: OK (simulated)"
echo "Uptime: 99.98%"
echo "Health check complete."
```

Make it executable.

Commit this file with a message that references the issue: `"Add health-check script refs #1"`.

Then make a **second commit**: edit `deploy.sh` to call `health-check.sh` at the start of the deployment. Update the deploy script commit message to reflect the change.

**Deliverable:** The `feature/health-check` branch has exactly 3 commits (the initial `deploy.sh` commit + 2 new ones on this branch).

---

### Task 7 — Push the Feature Branch and Open a Pull Request

Push `feature/health-check` to `origin`.

Open a Pull Request on GitHub with the title: **"feat: add health-check script"**

In the PR body, write:

```
## Description
Adds a `health-check.sh` script that verifies service availability before deployment.

## Related Issue
Closes #<your-issue-number>
```

Set the PR to request a review (you can self-review as Alice).

**Deliverable:** PR exists on GitHub, linked to the issue via the `Closes #<number>` keyword.

---

### Task 8 — Simulate Code Review

As **Alice**, go to the PR on GitHub and add a review comment on the `health-check.sh` file — leave a comment such as: *"Consider adding a `--verbose` flag for more detailed output."* Then **Approve** the PR.

**Deliverable:** The PR has at least one review comment and is in "Approved" state.

---

### Task 9 — Merge the Pull Request

Merge the PR using the **Squash and merge** strategy on GitHub.

Delete the `feature/health-check` branch after merging.

**Deliverable:** The PR is merged. The `feature/health-check` branch no longer exists locally or on `origin`. The `main` branch contains the squashed commit.

---

### Task 10 — Set Up GitHub Pages

Enable GitHub Pages in the repository settings:

- Source branch: `main`
- Folder: `/ (root)`

Save the settings and wait 1–2 minutes for the site to build.

Find the published URL (it will be `https://<yourusername>.github.io/infracore-scripts/`).

**Deliverable:** GitHub Pages site is live at the expected URL.

---

### Task 11 — Set Up a Pre-Commit Hook

In the local repository (on `main`), create a pre-commit hook at `.git/hooks/pre-commit` that runs `shellcheck` on any `.sh` file being committed. The hook should **fail** (exit non-zero) if `shellcheck` finds any errors or warnings.

Use this content:

```bash
#!/usr/bin/env bash
# Pre-commit hook: run shellcheck on all .sh files being committed

set -euo pipefail

echo "Running shellcheck on staged shell scripts..."

STAGED_SH_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep '\.sh$')

if [ -z "$STAGED_SH_FILES" ]; then
  echo "No shell scripts staged — skipping shellcheck."
  exit 0
fi

for FILE in $STAGED_SH_FILES; do
  echo "Checking: $FILE"
  shellcheck --severity=error "$FILE" || {
    echo "shellcheck failed for $FILE — commit aborted." >&2
    exit 1
  }
done

echo "shellcheck passed for all staged scripts."
exit 0
```

Make the hook executable.

Register it with Git:

```bash
git config --local core.hooksPath .git/hooks
```

Test the hook by staging `deploy.sh` and running `git commit`. The commit should succeed (deploy.sh passes shellcheck).

Then add a deliberate error to `health-check.sh` (e.g., remove the `set -euo pipefail` line), stage it, and verify the hook **blocks** the commit.

After testing, restore `health-check.sh` to its correct state.

**Deliverable:** The pre-commit hook runs automatically, blocks bad shell scripts, and passes for clean scripts.

---

### Task 12 — Create a Bug-Fix Branch with a Merge Conflict

As **Carol**, create a branch called `fix/deploy-output` from `main`.

On this branch, edit `deploy.sh` to change the success message:

```bash
echo "Deployment to ${ENVIRONMENT} complete — SUCCESS."
```

Commit this change.

Switch back to `main` and make a **different** change to the same line in `deploy.sh`:

```bash
echo "Deployment to ${ENVIRONMENT} finished."
```

Commit this change directly on `main`.

Now merge `fix/deploy-output` into `main`. Git will report a **merge conflict** on the `echo` line in `deploy.sh`.

Resolve the conflict by keeping **both** useful pieces of information:

```bash
echo "Deployment to ${ENVIRONMENT} complete — SUCCESS."
```

Stage the resolved file and commit the merge.

**Deliverable:** `main` has a merge commit that resolves the conflict without losing either change.

---

### Task 13 — Final Verification

Run the following commands and capture output:

```bash
# Show full commit history
git log --oneline --graph --all

# Verify GitHub Pages URL
git remote -v

# Verify the pre-commit hook is registered
git config --local core.hooksPath

# Show all branches (local and remote)
git branch -a

# Verify deploy.sh has the merged content
cat deploy.sh | grep "complete"
```

**Deliverable:** The output confirms a clean, multi-branch history with a merged conflict resolution, a live GitHub Pages URL, and a functioning pre-commit hook.

---

## Evaluation Criteria

A mentor reviewing this capstone would check:

| # | Criterion | How to Verify |
|---|-----------|--------------|
| 1 | Repository is public on GitHub with a Bash `.gitignore` | GitHub repo settings |
| 2 | Git identity is set locally to Alice's email | `git config --local user.email` |
| 3 | `deploy.sh` exists, is executable, and is on `main` | `ls -la deploy.sh && git log --oneline main` |
| 4 | Issue #1 exists with a meaningful description | GitHub Issues tab |
| 5 | `feature/health-check` branch has exactly 3 commits | `git log --oneline feature/health-check` |
| 6 | PR is open, approved, linked to issue via `Closes #1` | GitHub PR page |
| 7 | PR is merged via squash-merge; branch deleted | GitHub PR merged state |
| 8 | GitHub Pages is live at the expected URL | Visit the Pages URL |
| 9 | Pre-commit hook blocks bad shell scripts | Intentionally break a script and try to commit |
| 10 | `fix/deploy-output` branch has a conflict resolved with a merge commit | `git log --oneline main` shows merge commit |
| 11 | No broken internal links in the repo (exercise only) | `grep -r -- '](\./' 00-index.md 09-*.md` |

If all 11 criteria pass, the capstone is complete.

---

## Full Solution

This section walks through every task step-by-step with the exact commands and expected terminal output. If you get stuck at any point, come here first. Only check this solution when you have genuinely spent time trying — struggle is part of the learning process.

---

### Task 1 — Create the GitHub Repository

**On GitHub (web UI):**

1. Sign in to GitHub and click **+ → New repository**.
2. Owner: your username. Repository name: `infracore-scripts`.
3. Description: `Shared infrastructure automation scripts for InfraCore team`.
4. Select **Public**.
5. ☑️ Add a README file
6. ☑️ Add .gitignore → filter for "Bash" and select it
7. Click **Create repository**.

**Clone it locally:**

```bash
git clone https://github.com/YOURUSERNAME/infracore-scripts.git
cd infracore-scripts
```

```text
Cloning into 'infracore-scripts'...
warning: redirecting to https://github.com/YOURUSERNAME/infracore-scripts.git/
remote: Enumerating objects: 3, done.
remote: Counting objects: 100% (3/3), done.
remote: Total 3 (delta 0), reused 0 (delta 0), pack-reused 0
Receiving objects: 100% (3/3), done.
```

---

### Task 2 — Configure Git Identity

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
git config --global init.defaultBranch main

git config --local user.name "Alice <alice@infracore.dev>"
git config --local user.email "alice@infracore.dev"
```

Verify:

```bash
git config --local user.email
```

```text
alice@infracore.dev
```

---

### Task 3 — Create the Initial Commit

**Create the deploy.sh file:**

```bash
cat > deploy.sh << 'EOF'
#!/usr/bin/env bash
# deploy.sh — Infrastructure deployment script for InfraCore
# Usage: ./deploy.sh <environment>

set -euo pipefail

ENVIRONMENT="${1:-staging}"
echo "Deploying to ${ENVIRONMENT} environment..."

case "$ENVIRONMENT" in
  staging|production)
    echo "Deployment target validated: ${ENVIRONMENT}"
    ;;
  *)
    echo "Error: Unknown environment '${ENVIRONMENT}'" >&2
    exit 1
    ;;
esac

echo "Deployment to ${ENVIRONMENT} complete."
EOF
```

**Make it executable and commit:**

```bash
chmod +x deploy.sh
git add deploy.sh
git commit -m "Add deploy.sh with staging and production support"
```

```text
[main (root-commit) a1b2c3d] Add deploy.sh with staging and production support
 1 file changed, 1 insertion(+)
 create mode 100755 deploy.sh
```

**Push to GitHub:**

```bash
git push -u origin main
```

```text
Enumerating objects: 3, done.
Counting objects: 100% (3/3), done.
Writing objects: 100% (3/3), 191 bytes, done.
To https://github.com/YOURUSERNAME/infracore-scripts.git
 * [new branch]      main -> main
branch 'main' set up to track 'main'.
```

---

### Task 4 — Open an Issue

On GitHub, navigate to the repository → **Issues → New issue**.

- Title: `Add health-check script for all environments`
- Body:
  ```
  ## Problem
  We need a health-check script that verifies services are running before deployment proceeds.

  ## Proposed Solution
  Create a `health-check.sh` script that can be called by `deploy.sh` to confirm service availability.

  ## Additional Context
  Should support passing a service name as an argument.
  ```
- Labels: `enhancement`
- Click **Submit new issue**

Note the issue number in the URL. The issue URL will look like:
`https://github.com/YOURUSERNAME/infracore-scripts/issues/1`

Assume the issue number is **1** for the rest of this solution.

---

### Task 5 — Create a Feature Branch

```bash
git switch -c feature/health-check
```

```text
Switched to a new branch 'feature/health-check'
```

---

### Task 6 — Make Multiple Commits on the Feature Branch

**Commit 1 — Add health-check.sh:**

```bash
cat > health-check.sh << 'EOF'
#!/usr/bin/env bash
# health-check.sh — Service health check for InfraCore environments
# Usage: ./health-check.sh <service-name>

set -euo pipefail

SERVICE="${1:-web}"

echo "Running health check for service: ${SERVICE}"
echo "Status: OK (simulated)"
echo "Uptime: 99.98%"
echo "Health check complete."
EOF

chmod +x health-check.sh
git add health-check.sh
git commit -m "Add health-check script refs #1"
```

```text
[feature/health-check 2b3c4d5] Add health-check script refs #1
 1 file changed, 1 insertion(+)
 create mode 100755 health-check.sh
```

**Commit 2 — Update deploy.sh to call health-check.sh:**

```bash
cat > deploy.sh << 'EOF'
#!/usr/bin/env bash
# deploy.sh — Infrastructure deployment script for InfraCore
# Usage: ./deploy.sh <environment>

set -euo pipefail

ENVIRONMENT="${1:-staging}"
echo "Deploying to ${ENVIRONMENT} environment..."

# Run health check before deployment
./health-check.sh web

case "$ENVIRONMENT" in
  staging|production)
    echo "Deployment target validated: ${ENVIRONMENT}"
    ;;
  *)
    echo "Error: Unknown environment '${ENVIRONMENT}'" >&2
    exit 1
    ;;
esac

echo "Deployment to ${ENVIRONMENT} complete."
EOF

git add deploy.sh
git commit -m "Invoke health-check.sh before deployment"
```

```text
[feature/health-check 3c4d5e6] Invoke health-check.sh before deployment
 1 file changed, 4 insertions(+), 2 deletions(-)
```

**Verify the branch history:**

```bash
git log --oneline feature/health-check
```

```text
3c4d5e6 Invoke health-check.sh before deployment
2b3c4d5 Add health-check script refs #1
a1b2c3d Add deploy.sh with staging and production support
```

---

### Task 7 — Push the Feature Branch and Open a Pull Request

```bash
git push -u origin feature/health-check
```

```text
Enumerating objects: 5, done.
Counting objects: 100% (5/5), done.
Writing objects: 100% (5/5), 300 bytes, done.
To https://github.com/YOURUSERNAME/infracore-scripts.git
 * [new branch]      feature/health-check -> feature/health-check
Branch 'feature/health-check' set up to track remote branch 'feature/health-check' from 'origin'.
```

**Open the Pull Request using `gh`:**

```bash
gh pr create \
  --title "feat: add health-check script" \
  --body "## Description
Adds a \`health-check.sh\` script that verifies service availability before deployment.

## Related Issue
Closes #1" \
  --reviewer YOURUSERNAME
```

```text
https://github.com/YOURUSERNAME/infracore-scripts/pull/2
Creating pull request for 'feature/health-check' against 'main' in YOURUSERNAME/infracore-scripts
```

---

### Task 8 — Simulate Code Review

On GitHub, navigate to **Pull Requests → PR #2 → Files changed**.

Click on `health-check.sh`. Hover over a line number and click the blue `+` icon to add a comment:

> *"Consider adding a `--verbose` flag for more detailed output."*

Click **Add review comment**.

Then click **Review → Approve**.

---

### Task 9 — Merge the Pull Request

On GitHub, in the PR page:

1. Click **Squash and merge**
2. Check the commit message (the PR title is pre-filled)
3. Click **Confirm squash and merge**

After merging, GitHub will prompt to delete the branch. Click **Delete branch**.

**Verify locally:**

```bash
git switch main
git pull origin main
git branch -a
```

```text
Switched to branch 'main'
Your branch is up to date.
  main
* main
  remotes/origin/main
```

The `feature/health-check` branch is gone from both local and remote.

```bash
git log --oneline origin/main
```

```text
4d5e6f7 feat: add health-check script    # squashed commit
a1b2c3d Add deploy.sh with staging and production support
```

---

### Task 10 — Set Up GitHub Pages

On GitHub, navigate to **Settings → Pages**:

- Source: **Deploy from a branch** → Branch: `main` / `/ (root)`
- Click **Save**

Wait 1–2 minutes, then visit:
`https://YOURUSERNAME.github.io/infracore-scripts/`

The README.md will be published as a static site.

To find the URL from the terminal:

```bash
gh api repos/YOURUSERNAME/infracore-scripts/pages --jq '.html_url'
```

```text
https://YOURUSERNAME.github.io/infracore-scripts
```

---

### Task 11 — Set Up a Pre-Commit Hook

**Create the hooks directory:**

```bash
mkdir -p .git/hooks
```

**Write the pre-commit hook:**

```bash
cat > .git/hooks/pre-commit << 'EOF'
#!/usr/bin/env bash
# Pre-commit hook: run shellcheck on all .sh files being committed

set -euo pipefail

echo "Running shellcheck on staged shell scripts..."

STAGED_SH_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep '\.sh$')

if [ -z "$STAGED_SH_FILES" ]; then
  echo "No shell scripts staged — skipping shellcheck."
  exit 0
fi

for FILE in $STAGED_SH_FILES; do
  echo "Checking: $FILE"
  shellcheck --severity=error "$FILE" || {
    echo "shellcheck failed for $FILE — commit aborted." >&2
    exit 1
  }
done

echo "shellcheck passed for all staged scripts."
exit 0
EOF
```

**Make it executable and register it:**

```bash
chmod +x .git/hooks/pre-commit
git config --local core.hooksPath .git/hooks
```

**Verify:**

```bash
git config --local core.hooksPath
```

```text
.git/hooks
```

**Test — commit a good file:**

```bash
git add deploy.sh
git commit -m "Update deploy script"
```

```text
Running shellcheck on staged shell scripts...
Checking: deploy.sh
shellcheck passed for all staged scripts.
[main abc7890] Update deploy script
 1 file changed, 4 insertions(+), 2 deletions(-)
```

**Test — verify the hook blocks bad scripts:**

```bash
# Introduce a deliberate error
echo 'bad_script.sh << EOF
#!/usr/bin/env bash
echo $UNQUOTED_VAR
' > test-bad.sh
git add test-bad.sh
git commit -m "Add bad script"
```

Expected output (the commit should be **blocked**):

```text
Running shellcheck on staged shell scripts...
Checking: test-bad.sh

In test-bad.sh line 3:
echo $UNQUOTED_VAR
     ^----------^ SC2086: Double quote to prevent globbing and word splitting.
shellcheck failed for test-bad.sh — commit aborted.
```

If you see the blocked commit message, the hook is working correctly.

**Clean up the test file:**

```bash
rm test-bad.sh
git reset HEAD test-bad.sh
```

**Restore health-check.sh to correct state (if modified during testing):**

```bash
git checkout -- health-check.sh deploy.sh
```

---

### Task 12 — Create a Bug-Fix Branch with a Merge Conflict

**Create and switch to the fix branch:**

```bash
git switch -c fix/deploy-output
```

```text
Switched to a new branch 'fix/deploy-output'
```

**Modify deploy.sh on the fix branch:**

```bash
cat > deploy.sh << 'EOF'
#!/usr/bin/env bash
# deploy.sh — Infrastructure deployment script for InfraCore
# Usage: ./deploy.sh <environment>

set -euo pipefail

ENVIRONMENT="${1:-staging}"
echo "Deploying to ${ENVIRONMENT} environment..."

# Run health check before deployment
./health-check.sh web

case "$ENVIRONMENT" in
  staging|production)
    echo "Deployment target validated: ${ENVIRONMENT}"
    ;;
  *)
    echo "Error: Unknown environment '${ENVIRONMENT}'" >&2
    exit 1
    ;;
esac

echo "Deployment to ${ENVIRONMENT} complete — SUCCESS."
EOF

git add deploy.sh
git commit -m "Improve deploy success message"
```

```text
[fix/deploy-output 9f0a1b2] Improve deploy success message
 1 file changed, 1 insertion(+), 1 deletion(-)
```

**Switch back to main and make a different change to the same line:**

```bash
git switch main
```

```text
Switched to branch 'main'
```

```bash
cat > deploy.sh << 'EOF'
#!/usr/bin/env bash
# deploy.sh — Infrastructure deployment script for InfraCore
# Usage: ./deploy.sh <environment>

set -euo pipefail

ENVIRONMENT="${1:-staging}"
echo "Deploying to ${ENVIRONMENT} environment..."

# Run health check before deployment
./health-check.sh web

case "$ENVIRONMENT" in
  staging|production)
    echo "Deployment target validated: ${ENVIRONMENT}"
    ;;
  *)
    echo "Error: Unknown environment '${ENVIRONMENT}'" >&2
    exit 1
    ;;
esac

echo "Deployment to ${ENVIRONMENT} finished."
EOF

git add deploy.sh
git commit -m "Simplify deploy completion message"
```

```text
[main d3e4f5a] Simplify deploy completion message
 1 file changed, 1 insertion(+), 1 deletion(-)
```

**Merge the fix branch and encounter the conflict:**

```bash
git merge fix/deploy-output
```

```text
Auto-merging deploy.sh
CONFLICT (content): Merge conflict in deploy.sh
Automatic merge failed; fix conflicts and then commit the result.
```

**View the conflict:**

```bash
git diff
```

```text
<<<<<<< HEAD
echo "Deployment to ${ENVIRONMENT} finished."
=======
echo "Deployment to ${ENVIRONMENT} complete — SUCCESS."
>>>>>>> fix/deploy-output
```

**Resolve the conflict — keep both improvements:**

```bash
cat > deploy.sh << 'EOF'
#!/usr/bin/env bash
# deploy.sh — Infrastructure deployment script for InfraCore
# Usage: ./deploy.sh <environment>

set -euo pipefail

ENVIRONMENT="${1:-staging}"
echo "Deploying to ${ENVIRONMENT} environment..."

# Run health check before deployment
./health-check.sh web

case "$ENVIRONMENT" in
  staging|production)
    echo "Deployment target validated: ${ENVIRONMENT}"
    ;;
  *)
    echo "Error: Unknown environment '${ENVIRONMENT}'" >&2
    exit 1
    ;;
esac

echo "Deployment to ${ENVIRONMENT} complete — SUCCESS."
EOF
```

**Stage the resolved file and complete the merge:**

```bash
git add deploy.sh
git commit -m "Merge fix/deploy-output: resolved conflict, kept SUCCESS message"
```

```text
[main e5f6a7b] Merge fix/deploy-output: resolved conflict, kept SUCCESS message
```

---

### Task 13 — Final Verification

```bash
git log --oneline --graph --all
```

```text
*   e5f6a7b Merge fix/deploy-output: resolved conflict, kept SUCCESS message
|\
| * 9f0a1b2 Improve deploy success message
* | d3e4f5a Simplify deploy completion message
|/
* 4d5e6f7 feat: add health-check script (squash-merged from PR #2)
* a1b2c3d Add deploy.sh with staging and production support
```

```bash
git remote -v
```

```text
origin  https://github.com/YOURUSERNAME/infracore-scripts.git (fetch)
origin  https://github.com/YOURUSERNAME/infracore-scripts.git (push)
```

```bash
git config --local core.hooksPath
```

```text
.git/hooks
```

```bash
git branch -a
```

```text
  fix/deploy-output
* main
  remotes/origin/main
```

```bash
cat deploy.sh | grep "complete"
```

```text
echo "Deployment to ${ENVIRONMENT} complete — SUCCESS."
```

All verification commands confirm a correct, complete capstone project.

---

## Congratulations

You have completed the full Git and GitHub Development guide from first principles to a production-like workflow. You have:

- Created and configured a repository from scratch
- Used Git's branching model to isolate and review work
- Linked issues, branches, and pull requests into a cohesive development cycle
- Published a live GitHub Pages site
- Automated code quality checks with a pre-commit hook
- Resolved a merge conflict without losing any change

These are the exact skills DevOps engineers use every day. The tools and workflows you practiced here scale to teams of any size.

---

[← Previous: Self-Hosted Git](./14-self-hosted-git.md) · [Next: Consolidated Solutions →](./99-solutions.md) · [← Back to Index](./00-index.md)