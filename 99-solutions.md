# Consolidated Solutions

All exercise solutions from the Git and GitHub Documentation guide.

[← Back to Index](./00-index.md)

---

## Table of Contents

- [01: Getting Started](#01-getting-started)
- [02: Staging and Commits](#02-staging-and-commits)
- [03: History and Diff](#03-history-and-diff)
- [04: Undoing Changes](#04-undoing-changes)
- [05: Branching](#05-branching)
- [06: Merging](#06-merging)
- [07: Remotes](#07-remotes)
- [08: GitHub Repos and Forks](#08-github-repos-and-forks)
- [09: Pull Requests and Issues](#09-pull-requests-and-issues)
- [10: Code Review](#10-code-review)
- [11: Branching Strategies](#11-branching-strategies)
- [12: GitHub Pages](#12-github-pages)
- [13: Git Hooks](#13-git-hooks)
- [14: Self-Hosted Git](#14-self-hosted-git)

---

## 01: Getting Started

**Exercise:** Configure Git with your name and email, create a directory called `git-practice`, initialize it as a Git repository, create a file named `notes.txt` with the text `Learning Git is fun!`, and stage and commit the file with a descriptive message.

**Solution:**

### Step 1 — Configure Git

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
git config --global init.defaultBranch main
```

### Step 2 — Create and Initialize the Repository

```bash
mkdir git-practice
cd git-practice
git init
```

```text
Initialized empty Git repository in /home/username/git-practice/.git/
```

### Step 3 — Create a File

```bash
echo "Learning Git is fun!" > notes.txt
```

### Step 4 — Stage and Commit

```bash
git add notes.txt
git commit -m "Add notes.txt with opening message"
```

```text
[main (root-commit) b2c3d4e] Add notes.txt with opening message
 1 file changed, 1 insertion(+)
 create mode 100644 notes.txt
```

### Step 5 — Verify Your Work

```bash
git status
```

```text
On branch main
nothing to commit, working tree clean
```

```bash
git log
```

```text
commit b2c3d4e (HEAD -> main)
Author: Your Name <your.email@example.com>
Date:   Sat Jun 13 10:00:00 2026

    Add notes.txt with opening message
```

You have successfully initialized a repository, created a file, and committed it. The repository now tracks your work.

---

## 02: Staging and Commits

**Exercise:** Create two files (`notes.txt` and `progress.txt`), stage and commit only `notes.txt`, then stage and commit `progress.txt`. Verify both commits appear in the log.

**Solution:**

**Step 1 — Create the first file:**

```bash
echo "Learning Git staging and commits." > notes.txt
```

**Step 2 — Create the second file:**

```bash
echo "Day 1: Getting started with Git." > progress.txt
```

**Step 3 — Check status (untracked files):**

```bash
git status
```

```text
On branch main
Untracked files:
  (use "git add <file>..." to include in what will be committed)

        notes.txt
        progress.txt

nothing staged for commit
```

**Step 4 — Stage only `notes.txt`:**

```bash
git add notes.txt
```

**Step 5 — Confirm staging state:**

```bash
git status
```

```text
On branch main
Changes to be committed:
  (use "git restore --staged <file>..." to undo this)

        new file:   notes.txt

Untracked files:
  (use "git add <file>..." to include in what will be committed)

        progress.txt

nothing staged for commit
```

`notes.txt` is staged. `progress.txt` is still untracked and unstaged.

**Step 6 — Commit `notes.txt`:**

```bash
git commit -m "Add notes.txt with initial learning notes"
```

```text
[main 7c3a1fb] Add notes.txt with initial learning notes
 1 file changed, 1 insertion(+)
 create mode 100644 notes.txt
```

**Step 7 — Confirm commit in history:**

```bash
git log --oneline
```

```text
7c3a1fb Add notes.txt with initial learning notes
91da4e1 Initial project setup
```

**Step 8 — Stage and commit `progress.txt`:**

```bash
git add progress.txt
git commit -m "Add progress.txt tracking daily learning"
```

```text
[main 2e9d4a3] Add progress.txt tracking daily learning
 1 file changed, 1 insertion(+)
 create mode 100644 progress.txt
```

**Step 9 — Confirm both commits in log:**

```bash
git log --oneline
```

```text
2e9d4a3 Add progress.txt tracking daily learning
7c3a1fb Add notes.txt with initial learning notes
91da4e1 Initial project setup
```

Both commits appear in history, each with its own meaningful message.

---

## 03: History and Diff

**Exercise:** Make commits, run `git log --oneline`, use `git show` on the most recent commit, make a new change and use `git diff`, stage it and use `git diff --staged`, compare two commits with `git diff`, and view the full branch graph.

**Solution:**

**Step 1 — Navigate to your repository:**

```bash
cd ~/git-practice
```

If you do not have a practice repository, create one:

```bash
mkdir ~/git-practice && cd ~/git-practice
git init
echo "# My Project" > README.md
git add README.md
git commit -m "Initial project setup"
```

**Step 2 — Make additional commits:**

```bash
echo "Feature A" >> features.txt
git add features.txt
git commit -m "Add features list"

echo "Feature B" >> features.txt
git add features.txt
git commit -m "Add second feature to list"
```

**Step 3 — View recent history:**

```bash
git log --oneline -n 5
```

```text
c7f3b2a Add second feature to list
91da4e1 Add features list
a3f7c2d Add notes.txt with initial learning notes
b3f1a2c Add user authentication module
2e9d4a3 Initial project setup
```

Note the second-most-recent commit hash: `91da4e1`.

**Step 4 — Inspect the most recent commit:**

```bash
git show c7f3b2a
```

```text
commit c7f3b2a
Author: Alex Rivera <alex.rivera@example.dev>
Date:   Thu Jun 11 17:45:22 2026 +0000

    Add second feature to list

diff --git a/features.txt b/features.txt
index 9b2c1d4..e5f8a72 100644
--- a/features.txt
+++ b/features.txt
@@ -1 +1,2 @@
 Feature A
+Feature B
```

This shows the full metadata and diff for the commit — a single line addition of "Feature B".

**Step 5 — Make and diff unstaged changes:**

```bash
echo "Feature C" >> features.txt
git diff
```

```text
diff --git a/features.txt b/features.txt
index e5f8a72..a1b3c9d 100644
--- a/features.txt
+++ b/features.txt
@@ -1,2 +1,3 @@
 Feature A
 Feature B
+Feature C
```

The `+Feature C` line is unstaged — it exists only in your working directory.

**Step 6 — Stage and view staged changes:**

```bash
git add features.txt
git diff --staged
```

```text
diff --git a/features.txt b/features.txt
index e5f8a72..a1b3c9d 100644
--- a/features.txt
+++ b/features.txt
@@ -1,2 +1,3 @@
 Feature A
 Feature B
+Feature C
```

The same change now appears under "staged" — this is what will be committed.

**Step 7 — Compare two commits directly:**

```bash
git diff 91da4e1..c7f3b2a
```

```text
diff --git a/features.txt b/features.txt
index 8b1b3c7..a1b3c9d 100644
--- a/features.txt
+++ b/features.txt
@@ -1 +1,3 @@
 Feature A
+Feature B
+Feature C
```

This shows everything that changed between `91da4e1` (only "Feature A") and `c7f3b2a` (now has "Feature A", "Feature B", and "Feature C").

**Step 8 — Full branch graph:**

```bash
git log --oneline --graph --decorate --all
```

```text
* c7f3b2a (HEAD -> main) Add second feature to list
* 91da4e1 Add features list
* a3f7c2d Add notes.txt with initial learning notes
* b3f1a2c Add user authentication module
* 2e9d4a3 Initial project setup
```

---

## 04: Undoing Changes

**Exercise:** Using `git reset --soft HEAD~1`, fix the last commit message while keeping the changes staged, then recommit with a proper message.

**Solution:**

```bash
mkdir undo-practice
cd undo-practice
git init
```

```text
Initialized empty Git repository in /home/user/undo-practice/.git/
```

```bash
echo "database=localhost" > config.txt
git add config.txt
git commit -m "WIP"
```

```text
[main (root-commit) 1a2b3c4] WIP
 1 file changed, 1 insertion(+)
 create mode 100644 config.txt
```

```bash
echo "port=8080" >> config.txt
git add config.txt
git commit -m "WIP 2"
```

```text
[main 5d6e7f8] WIP 2
 1 file changed, 1 insertion(+)
```

```bash
git log --oneline
```

```text
5d6e7f8 WIP 2
1a2b3c4 WIP
```

Now fix the last commit. Use `--soft` to keep changes staged, then recommit with the correct message:

```bash
git reset --soft HEAD~1
```

```text
# No output — changes are staged
```

```bash
git commit -m "Add port configuration to config.txt"
```

```text
[main 9g0h1i2] Add port configuration to config.txt
 1 file changed, 1 insertion(+)
```

```bash
git log --oneline
```

```text
9g0h1i2 Add port configuration to config.txt
1a2b3c4 WIP
```

The "WIP 2" commit is gone, but its changes are now in a properly named commit. Your file `config.txt` contains both lines:

```bash
cat config.txt
```

```text
database=localhost
port=8080
```

---

## 05: Branching

**Exercise:** Create a branch `fix-typo`, switch to it, fix a typo in README.md, commit, switch back to `main`, create a new file on `main`, and verify the branches have independent histories.

**Solution:**

**1. Initialize the repository:**

```bash
mkdir branch-practice && cd branch-practice && git init
```

```text
Initialized empty Git repository in /home/user/branch-practice/.git/
```

**2. Create the initial commit:**

```bash
echo "Project Alpha v1.0" > README.md
git add README.md
git commit -m "Initial commit"
```

```text
[main (root-commit) 1a2b3c4] Initial commit
 1 file changed, 1 insertion(+)
 create mode 100644 README.md
```

**3. Create and switch to the `fix-typo` branch:**

```bash
git switch -c fix-typo
```

```text
Switched to a new branch 'fix-typo'
```

**4. Fix the typo:**

```bash
echo "Project Alpha v1.1" > README.md
```

**5. Commit the fix on `fix-typo`:**

```bash
git add README.md
git commit -m "Fix version typo in README"
```

```text
[fix-typo d5e6f7g] Fix version typo in README
 1 file changed, 1 insertion(+), 1 deletion(-)
```

**6. Switch back to `main`:**

```bash
git switch main
```

```text
Switched to branch 'main'
```

**7. On `main`, add a user guide file and commit:**

```bash
mkdir -p docs
echo "# User Guide\n\nComing soon." > docs/user-guide.md
git add docs/user-guide.md
git commit -m "Add user guide draft"
```

```text
[main h8i9j0k] Add user guide draft
 1 file changed, 3 insertions(+)
 create mode 100644 docs/user-guide.md
```

**8. Verify the typo fix is NOT on `main`:**

```bash
cat README.md
```

```text
Project Alpha v1.0
```

The file still reads `v1.0` — the typo fix lives only on `fix-typo`.

**9. Verify `docs/user-guide.md` does NOT exist on `fix-typo`:**

Switch to `fix-typo` and check:

```bash
git switch fix-typo
```

```text
Switched to branch 'fix-typo'
```

```bash
ls docs/
```

```text
ls: cannot access 'docs/': No such file or directory
```

The `docs/` directory and its contents exist only on `main`. Each branch holds its own independent line of commits.

---

## 06: Merging

**Exercise:** Perform a fast-forward merge of `branch-a` into `main`, then create a conflict by merging `branch-b` (which modified the same lines differently), and resolve the conflict by keeping both changes.

**Solution:**

### Setup

```bash
mkdir merge-practice
cd merge-practice
git init
echo "Line 1" > notes.txt
git add notes.txt
git commit -m "Initial commit"
```

```text
[main (root-commit) a1b2c3d] Initial commit
 1 file changed, 1 insertion(+)
 create mode 100644 notes.txt
```

### Create branch-a and make a change

```bash
git checkout -b branch-a
echo "Line 2 from branch-a" >> notes.txt
git add notes.txt
git commit -m "Add line from branch-a"
```

```text
[branch-a 4d5e6f7] Add line from branch-a
 1 file changed, 1 insertion(+)
```

### Create branch-b from main (not from branch-a)

```bash
git checkout main
git checkout -b branch-b
echo "Line 2 from branch-b" >> notes.txt
git add notes.txt
git commit -m "Add line from branch-b"
```

```text
[branch-b 8h9i0j1] Add line from branch-b
 1 file changed, 1 insertion(+)
```

### Merge branch-a (fast-forward)

```bash
git checkout main
git merge branch-a
```

```text
Updating a1b2c3d..4d5e6f7
Fast-forward
 notes.txt | 2 ++
 1 file changed, 2 insertions(+)
```

Because `main` hasn't moved since `branch-a` was created, Git fast-forwards `main` to `branch-a`'s commit. No merge commit is created.

### Merge branch-b (conflict!)

```bash
git merge branch-b
```

```text
Auto-merging notes.txt
CONFLICT (content): Merge conflict in notes.txt
Automatic merge failed; fix conflicts and then commit the result.
```

### Check the conflict status

```bash
git status
```

```text
On branch main
You have unmerged paths.
  (use "git add <file>...")

        both modified:   notes.txt

no changes added to commit (use "git add <file>..." to commit)
```

### View the conflicted file

```bash
cat notes.txt
```

```text
Line 1
<<<<<<< HEAD
Line 2 from branch-a
=======
Line 2 from branch-b
>>>>>>> branch-b
```

Git has marked the conflicting region. The current branch (`main`, which now includes `branch-a`'s change) wants "Line 2 from branch-a". The incoming `branch-b` wants "Line 2 from branch-b".

### Resolve the conflict by keeping both lines

Open `notes.txt` in your editor and replace the conflict markers with both lines:

```text
Line 1
Line 2 from branch-a
Line 2 from branch-b
```

Now the file contains both additions, which is the correct combined result.

### Complete the merge

```bash
git add notes.txt
git commit
```

```text
[main 2k3l4m5] Merge branch 'branch-b' into main
```

Git has created a merge commit that combines both histories.

### Verify the final result

```bash
cat notes.txt
git log --oneline --graph --all
```

```text
Line 1
Line 2 from branch-a
Line 2 from branch-b
```

```text
*   Merge branch 'branch-b' into main
|\
| * 8h9i0j1 Add line from branch-b
* | 4d5e6f7 Add line from branch-a
|/
* a1b2c3d Initial commit
```

The `notes.txt` file now contains all three lines. The graph clearly shows the two branches diverging from the initial commit and being brought back together by the merge commit.

---

## 07: Remotes

**Exercise:** Simulate a two-developer workflow using local "bare" repositories as remotes — create a shared bare repository, clone it to two separate repos, have colleague push changes, fetch and pull them, make your own changes, push, and verify both repos have identical histories.

**Solution:**

```bash
# Step 1: Create the directory structure
mkdir -p ~/git-remotes-exercise
cd ~/git-remotes-exercise

# Step 2: Create and initialize the shared remote as a bare repository
mkdir shared-remote.git
cd shared-remote.git
git init --bare
cd ..
```

```text
Initialized empty Git repository in /home/user/git-remotes-exercise/shared-remote.git/
```

```bash
# Step 3: Clone the shared remote into both repos
git clone shared-remote.git your-repo
git clone shared-remote.git colleague-repo

# Check remotes in each
cd your-repo
git remote -v
```

```text
origin  /home/user/git-remotes-exercise/shared-remote.git (fetch)
origin  /home/user/git-remotes-exercise/shared-remote.git (push)
```

```bash
# Step 4: In colleague-repo, add file, commit, and push
cd ../colleague-repo

# Configure git user (for this exercise)
git config user.name "Colleague"
git config user.email "colleague@example.com"

# Create about.html
cat > about.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>About Us</title>
</head>
<body>
    <h1>About Our Project</h1>
    <p>This is the about page.</p>
</body>
</html>
EOF

# Commit and push
git add about.html
git commit -m "Add about page"
git push origin main
```

```text
[main (root-commit) 1a2b3c4] Add about page
 1 file changed, 9 insertions(+)
Enumerating objects: 3, done.
Counting objects: 100% (3/3), done.
Writing objects: 100% (3/3), 150 bytes | 100.00 KiB/s, done.
To /home/user/git-remotes-exercise/shared-remote.git
 * [new branch]      main -> main
```

```bash
# Step 5: In your-repo, fetch and view what your colleague did
cd ../your-repo
git config user.name "You"
git config user.email "you@example.com"

# Fetch the changes
git fetch origin
```

```text
remote: Enumerating objects: 3, done.
remote: Counting objects: 100% (3/3), done.
Compressing objects: 100% (3/3), done.
Receiving objects: 100% (3/3), 70 bytes | 70.00 KiB/s, done.
Resolving deltas: 100% (3/3), done.
From /home/user/git-remotes-exercise/shared-remote
 * [new branch]      main -> origin/main
```

```bash
# See what your colleague pushed
git log origin/main --oneline
```

```text
1a2b3c4 Add about page
```

```bash
# Pull the changes (fast-forward since no divergent history)
git pull origin main
```

```text
From /home/user/git-remotes-exercise/shared-remote
 * [new branch]      main -> origin/main
Already up to date.
```

Wait, that says "Already up to date" — that's because `git pull` fetched AND merged, but our local main was at the same commit as origin/main. Let's verify:

```bash
git log --oneline
```

```text
1a2b3c4 Add about page
```

The about.html file should now be here:

```bash
ls -la
```

```text
total -rw-r--r-- about.html
total drwxr-xr-x about.html
total -rw-r--r-- about.html
```

Now make your changes:

```bash
# Create index.html
cat > index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Home</title>
</head>
<body>
    <h1>Welcome</h1>
    <p>This is the home page.</p>
</body>
</html>
EOF

# Commit and push with upstream tracking (-u)
git add index.html
git commit -m "Add index page"
git push -u origin main
```

```text
[main 2b3c4d5] Add index page
 1 file changed, 9 insertions(+)
Counting objects: 100% (2/2), done.
Writing objects: 100% (3/3), 150 bytes | 150.00 KiB/s, done.
To /home/user/git-remotes-exercise/shared-remote.git
   1a2b3c4..2b3c4d5  main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

```bash
# Step 6: In colleague-repo, pull your changes
cd ../colleague-repo
git pull origin main
```

```text
remote: Enumerating objects: 3, done.
remote: Counting objects: 100% (3/3), done.
Compressing objects: 100% (3/3), done.
From /home/user/git-remotes-exercise/shared-remote
   1a2b3c4..2b3c4d5  main     -> origin/main
Updating 1a2b3c4..2b3c4d5
Fast-forward
 index.html | 9 +++++++++++++++++
 1 file changed, 1 insertion(+)
```

```bash
# Step 7: Verify both repos have the same history
cd ../your-repo
echo "=== Your repo ==="
git log --oneline --all

cd ../colleague-repo
echo "=== Colleague repo ==="
git log --oneline --all
```

```text
=== Your repo ===
2b3c4d5 Add index page
1a2b3c4 Add about page

=== Colleague repo ===
2b3c4d5 Add index page
1a2b3c4 Add about page
```

Both repos now have identical commit histories!

---

## 08: GitHub Repos and Forks

**Exercise:** Create a repository `my-devops-scripts` on GitHub with README, Python .gitignore, and MIT license. Customize the README, add DevOps-specific .gitignore patterns, commit and push. Then fork `github/gitignore`, clone it, add upstream remote, fetch and merge from upstream/main, and push to origin.

**Solution:**

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

## 09: Pull Requests and Issues

**Exercise:** Create an issue for a login page crash bug, create a branch `fix-blank-username-crash`, make a commit with `Fixes #42`, push the branch, open a PR that references the issue, merge with squash merge, and verify the issue was closed.

**Solution:**

```bash
# 1. Create the issue
gh issue create \
  --title "Login page crashes when username is blank" \
  --body "When the username field is left blank and the user clicks Submit,
the application crashes with an error.

Steps to reproduce:
1. Navigate to /login
2. Leave the username field empty
3. Click Submit
Expected: validation message appears
Actual: application crashes

Labels: bug
Assignees: yourusername"
```

```text
https://github.com/yourusername/myrepo/issues/42
```

```bash
# 2. Create a feature branch
git checkout -b fix-blank-username-crash
```

```text
Switched to a new branch 'fix-blank-username-crash'
```

```bash
# 3. Make a commit with Fixes #42 in the message
# (Assume the file has been edited — here we simulate the commit)
git add src/auth/login.py
git commit -m "Fixes #42 — validate username field before submission"
```

```text
[fix-blank-username-crash 5f6g7h8] Fixes #42 — validate username field before submission
 1 file changed, 5 insertions(+), 1 deletion(-)
```

```bash
# 4. Push the branch to remote with upstream tracking
git push -u origin fix-blank-username-crash
```

```text
Enumerating objects: 5, done.
Counting objects: 100%
Writing objects: 100%
To https://github.com/yourusername/myrepo.git
 * [new branch]      fix-blank-username-crash -> fix-blank-username-crash
Branch 'fix-blank-username-crash' set up to track remote branch 'fix-blank-username-crash' from 'origin'.
```

```bash
# 5. Open a PR that references the issue
gh pr create \
  --title "Fix login crash on blank username" \
  --body "## What does this PR do?
Adds client-side validation to reject empty username before submission.

## Why is this needed?
Fixes #42 — the login page crashes when the username field is blank.

## Testing
1. Navigate to /login
2. Leave the username field empty
3. Click Submit
4. Verify a validation message appears instead of a crash"
```

```text
https://github.com/yourusername/myrepo/pull/43
```

```bash
# 6. Merge the PR with squash merge and delete the branch
gh pr merge 43 --squash --delete-branch
```

```text
Merged pull request #43 (Fix login crash on blank username)
✓ Squashed 1 commit into main
✓ Deleted branch fix-blank-username-crash, as you requested
```

```bash
# 7. Verify the issue was closed
gh issue view 42
```

```text
Login page crashes when username is blank
Labels: bug
Assignees: yourusername
State: closed    <-- Issue is now CLOSED
Opened by: yourusername
Closed by: yourusername  (via #43)
```

Issue #42 is automatically closed when PR #43 is merged. The issue even records which PR closed it.

---

## 10: Code Review

**Exercise:** As both reviewer and author, find a PR needing review, examine its diff, leave a blocking comment, request changes formally, simulate the author fixing the issue, approve the PR, and verify the review history.

**Solution:**

### Finding PRs Awaiting Review

```bash
gh pr list --search "review-requested:@me" --state open --json number,title,url
```

```text
[
  {
    "number": 38,
    "title": "Add health check endpoint",
    "url": "https://github.com/alexdev/your-repo/pull/38"
  }
]
```

### Examining the Diff

```bash
gh pr diff 38
```

```text
diff --git a/api/health.py b/api/health.py
new file mode 100644
index 0000000..123abc
--- /dev/null
+++ b/api/health.py
@@ -0,0 +1,14 @@
+"""Health check endpoint for load balancer probes."""
+from flask import Blueprint, jsonify
+
+health_bp = Blueprint("health", __name__)
+
+@health_bp.route("/health")
+def health_check():
+    """Return service health status."""
+    from api.db import check_connection  # expensive import at request time
+
+    db_ok = check_connection()
+    return jsonify({"status": "ok", "db": db_ok})
```

### Leaving a Comment

```bash
gh pr comment 38 --body "The health check looks like a good start, but there
is no error handling around \`check_connection()\`. If the database is
unreachable, this will raise an unhandled exception and return a 500 error.
Instead, it should catch that exception and return a 200 with \`db: false\`
so the load balancer knows the service is \`ok\` but the database is
unhealthy."
```

```text
https://github.com/alexdev/your-repo/pull/38#issuecomment-XXXXXXX
```

### Requesting Changes

```bash
gh pr review 38 --request-changes -b "Thanks for adding this! The structure
looks good. Blocking issue: \`check_connection()\` is not wrapped in a
try/except. If the DB is down, the endpoint crashes instead of returning a
health status. Please catch exceptions and return \`db: false\` rather than
raising. Non-blocking: consider moving the import to the top of the file —
importing at request time adds latency to every health check call."
```

```text
Pull request #38 (Add health check endpoint) reviewed with requested changes.
```

### Simulating the Fix

```bash
cat > api/health.py << 'EOF'
"""Health check endpoint for load balancer probes."""
from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)

@health_bp.route("/health")
def health_check():
    """Return service health status."""
    try:
        db_ok = check_connection()
    except Exception:
        db_ok = False

    return jsonify({"status": "ok", "db": db_ok})
EOF
```

```bash
git add api/health.py
git commit -m "fix: handle database errors gracefully in health check"
```

```text
[simulate-fix abc123d] fix: handle database errors gracefully in health check
 1 file changed, 4 insertions(+), 5 deletions(-)
```

### Approving

```bash
gh pr review 38 --approve -b "The try/except handles database errors correctly
now. The health check returns \`db: false\` instead of crashing. Non-blocking
note about the import placement is a future refactor — not a merge blocker.
LGTM, ship it!"
```

```text
Approved pull request #38 (Add health check endpoint)
```

### Verifying

```bash
gh pr view 38 --json reviews --jq '.reviews[] | {state, body}'
```

```text
{"state":"COMMENTED","body":"The health check looks like a good start..."}
{"state":"CHANGES_REQUESTED","body":"Thanks for adding this..."}
{"state":"APPROVED","body":"The try/except handles database errors..."}
```

The review history shows the complete lifecycle: a comment, a request for changes, and an approval.

---

## 11: Branching Strategies

**Exercise:** Simulate a complete GitFlow lifecycle: create initial commit on main, develop branch, feature/dashboard branch (merge with --no-ff), release/1.0.0 branch, finish release (merge to main with tag, merge to develop), create hotfix/security-patch (merge to both main and develop with tag), show final history.

**Solution:**

```bash
# 1. Setup and initial commit on main
mkdir -p ~/gitflow-practice && cd ~/gitflow-practice
git init
git config user.email "student@example.com"
git config user.name "Student"

echo "Initial project" > README.md
git add README.md
git commit -m "Initial commit"

# 2. Create develop branch
git checkout -b develop

# 3. Create feature branch and make a commit
git checkout -b feature/dashboard develop
echo "Dashboard page" > dashboard.html
git add dashboard.html
git commit -m "Add dashboard feature"

# 4. Merge feature into develop with --no-ff
git checkout develop
git merge --no-ff feature/dashboard -m "Merge feature/dashboard into develop"

# 5. Create release branch
git checkout -b release/1.0.0 develop
echo "1.0.0" > version.txt
git add version.txt
git commit -m "Bump version to 1.0.0"

# 6. Finish the release: merge into main, tag, merge back to develop
git checkout main
git merge --no-ff release/1.0.0 -m "Merge release/1.0.0 into main"
git tag -a v1.0.0 -m "Release version 1.0.0"

git checkout develop
git merge --no-ff release/1.0.0 -m "Merge release/1.0.0 into develop"

# Clean up release branch
git branch -d release/1.0.0

# 7. Create and finish a hotfix
git checkout -b hotfix/security-patch main
echo "Security fix applied" > security.txt
git add security.txt
git commit -m "Apply security hotfix"

git checkout main
git merge --no-ff hotfix/security-patch -m "Merge hotfix/security-patch into main"
git tag -a v1.0.1 -m "Hotfix version 1.0.1"

git checkout develop
git merge --no-ff hotfix/security-patch -m "Merge hotfix/security-patch into develop"

git branch -d hotfix/security-patch
git branch -d feature/dashboard
```

### Final History

```text
*   3f2a1b4 Merge hotfix/security-patch into develop
|\  
| * 2a1b3c5 Apply security hotfix
* |   1b2c3d4 Merge hotfix/security-patch into main
|\ \  
| |/  
| * 4d5e6f7 Security fix applied
|/|  
* |   a1b2c3d Merge release/1.0.0 into develop
|\ \  
| |/  
| *   e1f2g3h Merge release/1.0.0 into main
| |\  
| | * 9i8j7k6 Bump version to 1.0.0
* | |   b2c3d4e Merge feature/dashboard into develop
|\ \ \  
| | |/  
| | * 5f6g7h8 Add dashboard feature
| |/  
| * c3d4e5f Initial develop setup
|/  
* 7h8i9j0 Initial commit
```

Notice how `--no-ff` creates a **merge commit** (the commit with two parents shown as `*   ...`) for each feature and release, making it easy to see where each piece of work began and ended. The `develop` branch commits (b2c3d4e, 3f2a1b4) show the integration history. The `main` branch shows only production-ready commits (initial, v1.0.0, v1.0.1).

---

## 12: GitHub Pages

**Exercise:** Create a repository `git-fruit`, add an `index.md` with Jekyll front matter, enable GitHub Pages from the main branch root, push, and verify the site is live.

**Solution:**

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

---

## 13: Git Hooks

**Exercise:** Create a `commit-msg` hook that blocks any commit message shorter than 10 characters. Test it with a blocked short message ("fix bug") and an allowed longer message ("fix: resolve null pointer on login").

**Solution:**

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

## 14: Self-Hosted Git

**Exercise:** Install Gitea using Docker, complete the first-run setup wizard, create an admin account, create a repository `hello-devops`, clone it, add a file, commit and push, and verify in the web UI.

**Solution:**

```bash
# 1. Start the Gitea container
docker run -d \
  --name=gitea \
  --hostname=localhost \
  -p 3000:3000 \
  -p 2222:22 \
  -v /tmp/gitea:/data \
  --restart unless-stopped \
  gitea/gitea:latest
```

```bash
# 2. Wait for Gitea to start (30–60 seconds)
docker logs gitea 2>&1 | tail -5
```

Expected output:

```text
2024/11/01 14:23:01 [I] Gitea version 1.21.11 built with GNU Make
2024/11/01 14:23:01 [I] Log mode: File (Info)
2024/11/01 14:23:02 [I] XORM Log Mode: File (Info)
2024/11/01 14:23:03 [I] Migration completed successfully
2024/11/01 14:23:03 [I] listen: http://0.0.0.0:3000
```

The line `listen: http://0.0.0.0:3000` confirms Gitea is ready.

```bash
# 3. Open the setup wizard
# Open http://localhost:3000 in your browser.
# If first time, redirected to http://localhost:3000/install
```

**4. Fill in the setup form:**
- **Database Type:** SQLite3 (default)
- **Site Title:** `Gitea Local`
- **Repository Root Path:** `/data/git/repositories` (default)
- **Domain:** `localhost`
- **SSH Port:** `2222`
- **HTTP Port:** `3000`
- **Base URL:** `http://localhost:3000/`

Under **Administrator Account**:
- **Email:** `admin@gitea.local`
- **Password:** `SecureAdmin123!`
- **Username:** `gitea_admin`

Click **Install Gitea**.

```bash
# 5. Sign in as admin and create repository
# Click the + icon → Create Repository
# Name: hello-devops
# ☑️ Add a README
```

```bash
# 6. Clone the repository
git clone http://localhost:3000/gitea_admin/hello-devops.git
```

```text
Cloning into 'hello-devops'...
warning: redirecting to http://localhost:3000/gitea_admin/hello-devops.git/
remote: Enumerating objects: 3, done.
remote: Counting objects: 100% (3/3), done.
remote: Total 3 (delta 0), reused 0 (delta 0), pack-reused 0
Receiving objects: 100% (3/3), done.
```

```bash
# 7. Add a file, commit, and push
cd hello-devops
echo "# Hello DevOps" > devops.txt
git add devops.txt
git commit -m "Add devops.txt marker file"
git push -u origin main
```

```text
[main (root-commit) abc1234] Add devops.txt marker file
 1 file changed, 1 insertion(+), 1 deletion(-)
 create mode 100644 devops.txt
Username for 'http://localhost:3000': gitea_admin
Password for 'http://localhost:3000': SecureAdmin123!
Enumerating objects: 2, done.
Counting objects: 100% (2/2), done.
Writing objects: 100% (2/2), 81 bytes, done.
Total 2 (delta 0), reused 0 (delta 0), pack-reused 0
To http://localhost:3000/gitea_admin/hello-devops.git
 * [new branch]      main -> main
branch 'main' set up to track 'main'.
```

```bash
# 8. Verify in the web UI
# Refresh the Gitea repository page.
# You should see devops.txt in the file tree and the commit in history.
```

**To verify your setup was successful:**

```bash
# Verify the container is running
docker ps --filter name=gitea --format "{{.Names}} {{.Status}}"

# Verify the clone worked
ls hello-devops/devops.txt && echo "File exists"

# Verify the commit history
git -C hello-devops log --oneline
```

Expected output:

```text
gitea Up (healthy)
File exists
abc1234 Add devops.txt marker file
```

If you see the commit in the log and the file exists, your self-hosted Git server is working correctly.

---

[← Back to Index](./00-index.md)