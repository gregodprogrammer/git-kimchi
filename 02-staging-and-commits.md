# Staging and Commits

[← Previous: Getting Started](./01-getting-started.md)

In the previous section you created your first Git repository with `git init`. Now comes the real power of Git: capturing meaningful snapshots of your work. This section teaches you how to stage files intentionally and commit them with clear, professional messages.

---

## The Staging Area — Your Draft Space

Before Git saves a snapshot, you choose exactly what goes into it. The **staging area** (also called the **index**) is a holding zone between your working directory and the repository history. Think of it as a rehearsal space where you arrange what the next "photo" will capture.

### Why Staging Exists

Without staging, every save would be all-or-nothing. Staging lets you:

- **Select specific files** for a commit, ignoring temporary or unrelated changes
- **Split unrelated changes** into separate commits (a bug fix in one file, a new feature in another)
- **Review what you are about to commit** before locking it in history

Git's three states help you understand where your files live at any moment:

| State | Description |
|-------|-------------|
| **Modified** | You have changed a file but not staged it yet |
| **Staged** | You have marked the changed file to be included in the next commit |
| **Committed** | The staged snapshot is safely stored in the repository |

This is Git's fundamental workflow: modify files, stage the ones you want, commit the staged snapshot, repeat.

---

## Checking Status with `git status`

The `git status` command shows exactly what state your files are in. Run it often — it is your map of the working directory.

### A Clean Repository

When nothing has changed, Git tells you the branch is up to date:

```bash
git status
```

```text
On branch main
nothing to commit, working tree clean
```

### Untracked Files

An untracked file is a new file that Git has never seen before. Git does not track it automatically — you must add it:

```bash
git status
```

```text
On branch main
Untracked files:
  (use "git add <file>..." to include in what will be committed)

        README.md

nothing staged for commit
```

### Modified Files

When you edit a tracked file but have not staged the changes:

```bash
git status
```

```text
On branch main
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)

        modified:   README.md

no changes added to commit
```

### Staged Files

After you stage a file, it appears under "Changes to be committed":

```bash
git status
```

```text
On branch main
Changes to be committed:
  (use "git restore --staged <file>..." to undo this)

        new file:   README.md

nothing staged for commit
```

---

## Staging Files with `git add`

The `git add` command moves files from modified or untracked into the staging area. You stage **by name** — this gives you precise control over what enters the next snapshot.

### Staging a New (Untracked) File

```bash
git add README.md
```

After running this command, `README.md` moves from untracked to staged:

```bash
git status
```

```text
On branch main
Changes to be committed:
  (use "git restore --staged <file>..." to undo this)

        new file:   README.md

nothing staged for commit
```

### Staging a Modified File

Imagine you edited `app.py`. First, check its status:

```bash
git status
```

```text
On branch main
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)

        modified:   app.py

no changes added to commit
```

Stage it explicitly:

```bash
git add app.py
```

```bash
git status
```

```text
On branch main
Changes to be committed:
  (use "git restore --staged <file>..." to undo this)

        modified:   app.py

nothing staged for commit
```

### Staging Multiple Specific Files

If you have changes in several files, stage them one by one:

```bash
git add config.py
git add utils.py
git add tests/test_app.py
```

This lets you group related changes into a single thoughtful commit while leaving unrelated changes unstaged.

> **Note:** This guide uses explicit `git add ` throughout. Avoid `git add -A` or `git add .` — they stage everything at once and make it easy to accidentally commit files you did not intend to include (like temporary files, build artifacts, or secrets).

---

## Removing Files from Staging

Sometimes you stage a file by mistake. Git gives you two ways to unstage — one modern, one legacy.

### Modern: `git restore --staged`

The modern approach uses `git restore` with the `--staged` flag:

```bash
git restore --staged app.py
```

This removes `app.py` from the staging area. The file returns to the "modified but not staged" state — your changes are not lost:

```bash
git status
```

```text
On branch main
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)

        modified:   app.py

nothing staged for commit
```

### Legacy: `git reset HEAD`

The `git reset` command with `HEAD` as the target achieves the same result:

```bash
git reset HEAD app.py
```

```text
Unstaged changes after reset:
M       app.py
```

Both commands unstage the file without destroying your changes. The modern `git restore --staged` is clearer in intent and is recommended for new users. The `git reset` approach appears in older tutorials and some automated scripts, so it is worth recognizing.

---

## Writing Commits with `git commit`

A commit is a permanent snapshot of your staged changes, timestamped and stored in the repository history. Each commit has a unique identifier (a SHA-1 hash) and records who made it and when.

### A Basic Commit

After staging your changes, commit them with a message:

```bash
git commit -m "Add user authentication module"
```

Git confirms the commit with its hash, the branch, and what changed:

```text
[main b3f1a2c] Add user authentication module
 2 files changed, 87 insertions(+)
 create mode 100644 auth.py
 create mode 100644 auth_test.py
```

### What Makes a Good Commit Message

A commit message explains **why** a change was made, not just what changed. Follow these rules:

| Rule | Example |
|------|---------|
| **Imperative mood** — describe what the commit does, not what you did | `"Fix null pointer in login handler"` not `"Fixed null pointer"` |
| **First line under 72 characters** | Keep the subject line concise |
| **Separate subject from body with a blank line** | Enables good rendering in tools |
| **Explain the why, not the what** | Code shows what; message explains why |
| **Reference the issue if one exists** | `"Close #42: Add password reset flow"` |

A well-formed multi-line commit message:

```bash
git commit -m "Add rate limiting to API endpoints

Implements a token bucket algorithm with 100 req/min per user.
Prevents abuse in the staging environment where no rate limiting existed.
Fixes #38."
```

The first line is the **subject**. The blank line separates it from the **body**, which can be as long as needed to provide context.

### Why Imperative Mood?

You may wonder why Git itself uses imperative messages. When you write `"Add feature"` rather than `"Added feature"` or `"Adds feature"`, it completes the sentence: *"If applied, this commit will [subject]."* This keeps every message grammatically consistent and matches the style used in merge commits and release notes.

---

## Amending Commits

Made a mistake in your last commit — wrong message, forgot to include a file? You can fix it with `git commit --amend`.

### Correcting a Commit Message

If you just committed and realized the message has a typo:

```bash
git commit --amend -m "Add user authentication with JWT tokens"
```

This replaces the previous commit message entirely. The commit hash changes because the content (including metadata) is different.

### Adding a Forgotten File

If you forgot to stage a file:

```bash
git add forgotten_file.py
git commit --amend --no-edit
```

The `--no-edit` flag keeps the original message while including the newly staged file in the same commit.

### When NOT to Amend

**Never amend commits that have been pushed to a shared repository.** Other people may have built work on top of your commit. Amending rewrites history and breaks their clones. If you need to fix a pushed commit, the correct approach is a new commit that reverts or corrects the error.

For local commits that have not been shared, amending is safe and common during active development.

---

## Viewing Commit History

After you have made a few commits, view them with `git log`. The `--oneline` flag gives a compact view that is perfect for everyday use:

```bash
git log --oneline
```

```text
b3f1a2c Add user authentication module
91da4e1 Initial project setup
```

Each line shows the first 7 characters of the commit hash followed by the subject line. This format scales well — a project with hundreds of commits remains readable.

For more detail on `git log` and `git diff` (which shows exactly what changed in each commit), see the next section: [History and Diff](./03-history-and-diff.md).

---

## Exercise

### Scenario

You are working on a small documentation project. You have created a new repository and made changes to several files, but you have not staged or committed anything yet. Your task is to stage and commit your changes using proper Git workflow.

### Tasks

1. Create a new file called `notes.txt` and add the text `Learning Git staging and commits.`
2. Modify an existing file (or create and modify `progress.txt`) with the text `Day 1: Getting started with Git.`
3. Run `git status` to observe the untracked and modified states.
4. Stage **only** `notes.txt` using `git add`.
5. Check `git status` to confirm `notes.txt` is staged and `progress.txt` remains unstaged.
6. Commit `notes.txt` with a meaningful commit message in imperative mood.
7. Run `git log --oneline` to confirm the commit appears in history.
8. Now stage and commit `progress.txt` with its own message.
9. Confirm both commits appear in the log.

---

## Solution

Follow these steps to complete the exercise:

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

Both commits appear in history, each with its own meaningful message. You staged and committed files one at a time, giving you full control over the snapshot each commit captures.

---

## Key Takeaways

- **Staging is intentional** — use `git add ` to choose exactly which files enter the next commit.
- **Check status often** — `git status` shows you what is modified, staged, or untracked at a glance.
- **Unstage with `git restore --staged`** — your changes are safe; they just move back to modified.
- **Write clear commit messages** in imperative mood — `"Add feature"` not `"Added feature"`.
- **Amend only local commits** — never rewrite history of pushed commits.
- **`git log --oneline`** gives a compact history view — useful for orienting yourself in any project.

---

## What's Next

Now that you understand staging and commits, learn how to browse and understand your project history in depth.

[Next: History and Diff →](./03-history-and-diff.md)

[← Back to Index](./00-index.md)