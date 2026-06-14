# History and Diff

[← Previous: Staging and Commits](./02-staging-and-commits.md)

You have been making commits and building your project history. But how do you actually look back at that history? How do you see what changed between two commits, or between your current work and the last saved snapshot? That is what this section covers. By the end, you will know how to browse, filter, and inspect your project's commit timeline with confidence.

---

## Understanding Git History as a Timeline

Every time you run `git commit`, Git records a new snapshot of your staged files and attaches metadata: who made the change, when, and why (your commit message). These snapshots form a **linked chain** — each commit points backward to its parent. This chain is your repository's history.

Think of it like a timeline or a photo album. Each commit is a photograph of your project at a specific moment. `git log` lets you flip through that album backward in time, from the newest photo to the oldest.

---

## Browsing History with `git log`

The `git log` command shows you the commit history for your repository. By default, it shows the most recent commits first, with full details including the author name, email, date, and full commit message.

### A Standard Log

```bash
git log
```

```text
commit a3f7c2d
Author: Maria Chen <maria.chen@example.dev>
Date:   Thu Jun 11 14:32:07 2026 +0000

    Refactor user authentication to use JWT tokens

    - Replace session-based auth with stateless JWT
    - Add token refresh endpoint
    - Update client SDK to handle token storage
```

The log shows one commit at a time with a blank line separating each entry. This format is thorough but verbose — for everyday use, the compact formats below are more practical.

---

## Common `git log` Options

### `--oneline` — Compact View

The `--oneline` flag collapses each commit to a single line: the short hash and the subject. This is the most common format for daily use.

```bash
git log --oneline
```

```text
a3f7c2d Refactor user authentication to use JWT tokens
91da4e1 Add password validation utility
7c3a1fb Fix edge case in email parser
b3f1a2c Add user authentication module
2e9d4a3 Add progress.txt tracking daily learning
```

With hundreds of commits, `--oneline` keeps the view readable. You can always run `git show <hash>` to get full details on any specific commit.

### `--graph` — ASCII Branch Visualization

The `--graph` flag draws an ASCII art representation of branches and merges, making it easier to see the shape of your history.

```bash
git log --oneline --graph
```

```text
* a3f7c2d Refactor user authentication to use JWT tokens
* 91da4e1 Add password validation utility
* 7c3a1fb Fix edge case in email parser
* b3f1a2c Add user authentication module
* 2e9d4a3 Add progress.txt tracking daily learning
```

When you have multiple branches, the graph shows you where they diverge and merge:

```text
*   d4b8a91 Merge feature/search into main
|\
| * e1c3f72 Add search index caching
| * 7f2d4a8 Implement search result ranking
* | c9e1b33 Update dependencies
|/
* a3f7c2d Refactor user authentication to use JWT tokens
```

The `*` marks commits on the main branch. The `|` and `\` characters draw the branching lines. In the merge commit `d4b8a91`, you can see two parent commits — one from each branch that was merged.

### `--decorate` — Show Branch and Tag Names

The `--decorate` flag adds branch and tag names to the commits they point to. This is especially useful when navigating multi-branch histories.

```bash
git log --oneline --decorate
```

```text
a3f7c2d (main) Refactor user authentication to use JWT tokens
91da4e1 Add password validation utility
7c3a1fb Add search index caching
b3f1a2c Add user authentication module
```

In this output, `(main)` appears next to the most recent commit, telling you that `main` currently points there.

### `--all` — Show All Branches

By default, `git log` shows only the current branch's history. To see commits from all branches, add `--all`:

```bash
git log --oneline --all
```

```text
f9e2d71 (feature/oauth) Add OAuth2 provider integration
a3f7c2d (main) Refactor user authentication to use JWT tokens
91da4e1 Add password validation utility
7c3a1fb Add search index caching
e1c3f72 (develop) Add search result ranking
```

The `feature/oauth` commit `f9e2d71` exists only on that branch — it would not appear without `--all`.

### `-n <number>` — Limit the Number of Commits

Show only the most recent `N` commits:

```bash
git log --oneline -n 3
```

```text
a3f7c2d Refactor user authentication to use JWT tokens
91da4e1 Add password validation utility
7c3a1fb Fix edge case in email parser
```

This is equivalent to the common `git log -3` shorthand.

### `--since` and `--until` — Time Ranges

Filter commits by date using natural language or absolute dates:

```bash
git log --oneline --since="2026-06-01"
```

```text
a3f7c2d Refactor user authentication to use JWT tokens
91da4e1 Add password validation utility
```

```bash
git log --oneline --since="2 weeks ago"
```

```text
a3f7c2d Refactor user authentication to use JWT tokens
91da4e1 Add password validation utility
7c3a1fb Fix edge case in email parser
```

Use `--until` to get commits before a specific date:

```bash
git log --oneline --until="2026-06-05"
```

These filters are useful for generating changelogs, weekly reports, or finding which commits landed in a particular release window.

### `--author` — Filter by Author

Show only commits by a specific author:

```bash
git log --oneline --author="Maria Chen"
```

```text
a3f7c2d Refactor user authentication to use JWT tokens
b3f1a2c Add user authentication module
```

Author filtering works with partial names too — `git log --oneline --author="Maria"` matches `"Maria Chen"`.

### Combining Options

The real power comes from combining options. The most useful everyday combination for understanding your project structure is:

```bash
git log --oneline --graph --decorate --all
```

```text
* f9e2d71 (feature/oauth) Add OAuth2 provider integration
|\
| * 7f2d4a8 Implement search result ranking
* | c9e1b33 Update dependencies
|/
*   d4b8a91 (HEAD -> main) Merge feature/search into main
|\
| * e1c3f72 Add search index caching
| * 7f3a1db Add search index
* | a3f7c2d Refactor user authentication to use JWT tokens
|/
* 91da4e1 Add password validation utility
```

`HEAD -> main` marks which commit the current branch is pointing to. This view shows you exactly where you are in the tree, what branches exist, and how they relate to each other.

---

## `git log --stat` — Commit Stats

The `--stat` flag shows a summary of changed files per commit — how many lines were added and removed — without showing the actual diff:

```bash
git log --stat
```

```text
commit a3f7c2d
Author: Maria Chen <maria.chen@example.dev>
Date:   Thu Jun 11 14:32:07 2026 +0000

    Refactor user authentication to use JWT tokens

 auth.py      | 45 +++++++++++++++++------------------
 auth_test.py | 22 +++++++++++++++----
 utils.py     |  5 +++++
 3 files changed, 41 insertions(+), 31 deletions(-)
```

Each file is listed with a visual representation of the change magnitude: `45 +++++++++++++++++------------------` shows the additions and deletions. The summary line at the bottom (`3 files changed, 41 insertions(+), 31 deletions(-)`) gives you the totals.

`--stat` is useful when you want a high-level view of what changed across several commits without wading into the full diffs.

---

## `git log --patch` — Inline Diffs in Log

The `--patch` flag (or `-p`) shows the actual code changes (the diff) inline within the log. This combines the commit metadata with the full diff for each commit:

```bash
git log --patch
```

```text
commit a3f7c2d
Author: Maria Chen <maria.chen@example.dev>
Date:   Thu Jun 11 14:32:07 2026 +0000

    Refactor user authentication to use JWT tokens

diff --git a/auth.py b/auth.py
index 8a1b3c7..d4e5f92 100644
--- a/auth.py
+++ b/auth.py
@@ -15,10 +15,12 @@ class AuthHandler:
-    def authenticate(self, username, password):
-        return self.db.verify(username, password)
+    def authenticate(self, username, password):
+        token = self.jwt_service.generate_token(username)
+        return {"token": token, "expires_in": 3600}

     def refresh(self, token):
         return self.jwt_service.refresh(token)
```

The diff shows lines removed (prefixed with `-`) and lines added (prefixed with `+`). This format is equivalent to running `git show` on each commit individually — covered next.

---

## `git show` — Inspecting a Single Commit

The `git show` command displays the full details of a single commit: its hash, author, date, message, and the complete diff. It is equivalent to `git log --patch` but focused on one specific commit.

### Basic `git show`

```bash
git show a3f7c2d
```

```text
commit a3f7c2d (main)
Author: Maria Chen <maria.chen@example.dev>
Date:   Thu Jun 11 14:32:07 2026 +0000

    Refactor user authentication to use JWT tokens

diff --git a/auth.py b/auth.py
index 8a1b3c7..d4e5f92 100644
--- a/auth.py
+++ b/auth.py
@@ -15,10 +15,12 @@ class AuthHandler:
-    def authenticate(self, username, password):
-        return self.db.verify(username, password)
+    def authenticate(self, username, password):
+        token = self.jwt_service.generate_token(username)
+        return {"token": token, "expires_in": 3600}

     def refresh(self, token):
         return self.jwt_service.refresh(token)
diff --git a/auth_test.py b/auth_test.py
index 9b2c4d8..e1f3a72 100644
--- a/auth_test.py
+++ b/auth_test.py
@@ -22,6 +22,9 @@ def test_authenticate():
     assert response["expires_in"] == 3600

+def test_token_refresh():
+    assert auth.refresh("expired_token") is not None
+
```

`git show` is the go-to command when you need to review exactly what a specific commit changed — during code review, debugging, or when exploring unfamiliar code.

---

## Understanding `git diff` — What Changed?

While `git log` shows you the **history**, `git diff` shows you the **changes** between different states of your project. It is how you answer: "What have I actually changed?"

Git compares pairs of commits, branches, or work states and reports the differences line by line. Lines that were removed show with a `-` prefix; lines that were added show with a `+` prefix.

---

## `git diff` — Working Directory vs Staging Area

The plain `git diff` (with no arguments) compares your **working directory** (uncommitted changes) against the **staging area** (what you have staged with `git add`). This shows what you have changed but not yet staged.

### Example

You edit `README.md` and add a new line. Running `git diff` shows:

```bash
git diff
```

```text
diff --git a/README.md b/README.md
index 8b1b3c7..d4e5f92 100644
--- a/README.md
+++ b/README.md
@@ -5,6 +5,7 @@

  ## Project Overview
  This is a documentation project for learning Git.
+Added this new line to the README.
  ## Getting Started
  Follow the sections in order.
```

The `+` line (with no `-` counterpart) is an addition. If you had deleted a line, it would show with a `-` prefix.

### When to Use This

Run `git diff` before staging to review exactly what you are about to commit. It lets you catch unintended changes before they enter the staging area and eventually the history.

---

## `git diff --staged` — Staging Area vs Last Commit

The `--staged` flag (also `--cached`) compares the **staging area** against the **last commit**. This shows what you have staged but not yet committed — the changes that will enter the next snapshot.

### After Staging a Change

You edit `README.md` and run `git add README.md`. Then:

```bash
git diff --staged
```

```text
diff --git a/README.md b/README.md
index 8b1b3c7..d4e5f92 100644
--- a/README.md
+++ b/README.md
@@ -5,6 +5,7 @@
  ## Project Overview
  This is a documentation project for learning Git.
+Added this new line to the README.
  ## Getting Started
  Follow the sections in order.
```

The output looks identical to plain `git diff` — but it is comparing against the staged state, not the working directory.

### When to Use This

Run `git diff --staged` after staging to double-check exactly what will be committed. This is your final review pass before running `git commit`.

---

## `git diff <commit1> <commit2>` — Comparing Two Commits

Compare any two commits by giving their hashes. The order matters: the output shows what changed **from the first commit to the second**.

### Recent Commits Compared

```bash
git diff 91da4e1 a3f7c2d
```

```text
diff --git a/auth.py b/auth.py
index 8a1b3c7..d4e5f92 100644
--- a/auth.py
+++ b/auth.py
@@ -15,10 +15,12 @@ class AuthHandler:
-    def authenticate(self, username, password):
-        return self.db.verify(username, password)
+    def authenticate(self, username, password):
+        token = self.jwt_service.generate_token(username)
+        return {"token": token, "expires_in": 3600}
```

This shows exactly what changed between `91da4e1` (the earlier commit) and `a3f7c2d` (the later one).

You can also use relative references:

```bash
git diff HEAD~3 HEAD
```

This compares the commit 3 steps back from `HEAD` to the current `HEAD`.

---

## `git diff <branch1> <branch2>` — Comparing Two Branches

Compare the tips of two branches to see all changes that would result from merging one into the other:

```bash
git diff main feature/oauth
```

```text
diff --git a/oauth.py b/oauth.py
new file mode 100644
index 0000000..e1f3a72
--- /dev/null
+++ b/oauth.py
@@ -0,0 +1,34 @@
+import oauthlib
+
+class OAuthProvider:
+    def authenticate(self, provider):
+        return oauthlib.authenticate(provider)
```

In this output, `oauth.py` is a new file that exists on `feature/oauth` but not on `main`. To understand how a branch diverged from `main`, use:

```bash
git diff main...feature/oauth
```

The triple-dot syntax shows only the changes on `feature/oauth` since it diverged from `main` — not every difference between the two branch tips.

---

## `git diff <commit> -- <file>` — Diff a Specific File

Focus the diff on a single file by naming it after `--`:

```bash
git diff a3f7c2d -- auth.py
```

```text
diff --git a/auth.py b/auth.py
index 8a1b3c7..d4e5f92 100644
--- a/auth.py
+++ b/auth.py
@@ -15,10 +15,12 @@ class AuthHandler:
-    def authenticate(self, username, password):
-        return self.db.verify(username, password)
+    def authenticate(self, username, password):
+        token = self.jwt_service.generate_token(username)
+        return {"token": token, "expires_in": 3600}
```

This ignores changes to any other file. It is especially useful in large repositories where a full diff is overwhelming.

You can also diff the working directory version of a single file against a specific commit:

```bash
git diff HEAD -- README.md
```

---

## A Complete Diff Workflow Example

Here is how these commands fit together in a real development session:

1. **Start your day:** Check recent commits on your branch:
```bash
git log --oneline -n 5
```

```text
a3f7c2d Refactor user authentication to use JWT tokens
91da4e1 Add password validation utility
7c3a1fb Fix edge case in email parser
b3f1a2c Add user authentication module
```

2. **Make some changes:** Edit `auth.py` and `config.py`.

3. **Review unstaged changes:**
```bash
git diff
```
Shows working directory changes against the staging area.

4. **Stage the changes you want to commit:**
```bash
git add auth.py
```

5. **Review staged changes (final check before commit):**
```bash
git diff --staged
```
Shows exactly what will be committed.

6. **Commit:**
```bash
git commit -m "Add rate limiting to auth endpoints"
```

This workflow — **diff, stage, diff --staged, commit** — is a reliable routine for making intentional, well-reviewed commits.

---

## Exercise

### Scenario

You are working on a Python CLI tool and have made several commits. Your task is to explore the commit history, understand what changed between commits, and review your working directory changes before making a new commit.

### Tasks

1. Navigate to your practice repository (or the repository you created in the previous exercise).
2. Make at least 2 more commits if you have not already done so. Give each a meaningful commit message.
3. Run `git log --oneline -n 5` to see your recent history. Note the hash of the second-most-recent commit.
4. Run `git show <hash>` on your most recent commit to review its full diff.
5. Make a new change to any file, then run `git diff` to see the unstaged changes.
6. Stage that change with `git add`, then run `git diff --staged` to see it in staged form.
7. Use `git diff <older-hash>..<newer-hash>` to compare two commits directly.
8. Run `git log --oneline --graph --decorate --all` to see the full branch structure.

---

## Solution

Follow these steps to complete the exercise:

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

Since you are working on a single branch, the graph is linear. Once you create branches and merges (covered in a later section), the `--graph` output becomes more interesting.

---

## Key Takeaways

- **`git log`** shows the commit timeline; use `--oneline` for compact views and `--graph` to see branch structure.
- **`git log --stat`** summarizes changed files per commit; **`git log --patch`** shows full diffs inline.
- **`git show <commit>`** gives full details (metadata + diff) for a single commit.
- **`git diff`** compares states: working directory vs staging area, staging area vs last commit, or any two commits/branches.
- **Use `git diff --staged` before every commit** as your final review pass.
- **`git diff branch1 branch2`** compares branch tips; **`git diff branch1...branch2`** compares only the changes since they diverged.

---

## What's Next

You now know how to browse and inspect your project's history. But what happens when you make a mistake? The next section covers undoing changes — from un-staging a file you accidentally added, to rolling back a commit that introduced a bug.

[Next: Undoing Changes →](./04-undoing-changes.md)

[← Back to Index](./00-index.md)