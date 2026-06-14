# Pull Requests and Issues

[← Previous: GitHub Repos and Forks](./08-github-repos-and-forks.md) · [← Back to Index](./00-index.md)

---

## What Is a Pull Request?

A **Pull Request (PR)** is a proposal to merge one branch into another. It is the central hub for code collaboration on GitHub. Before merging, a PR opens a space for discussion, review, and approval of the proposed changes.

Think of it this way: you have been working on a feature branch. Now you want to merge those changes into `main`. Instead of just pushing and merging, you *request* that the maintainers of the repository *pull* your changes in. This gives them a chance to review before anything lands in the main codebase.

A PR is not just a technical action — it is a **conversation**. Comments, questions, and suggestions happen right in the PR thread. This is why opening a PR early (even when work is incomplete, as a Draft PR) is often better than keeping it private until it is "done."

**Key point:** A PR is the bridge between your feature branch and the main branch. It ensures changes do not land in `main` unannounced.

---

## The PR Lifecycle

The PR lifecycle has several stages, from creating a branch to cleaning up after a merge. Here is each step in detail.

### Step 1 — Create a Feature Branch

Always develop new work on a dedicated branch, never directly on `main`.

```bash
git checkout -b fix-login-bug
```

```text
Switched to a new branch 'fix-login-bug'
```

### Step 2 — Make Commits

Edit files and commit your changes. Each commit should represent a logical unit of work.

```bash
git add src/auth/login.py
git commit -m "Fix: prevent null pointer on empty password field"
```

```text
[fix-login-bug a1b2c3d] Fix: prevent null pointer on empty password field
 1 file changed, 3 insertions(+), 1 deletion(-)
```

### Step 3 — Push the Branch to Remote

Your branch does not exist on the remote yet. Use `-u` (short for `--set-upstream`) to set the tracking relationship:

```bash
git push -u origin fix-login-bug
```

```text
Enumerating objects: 5, done.
Counting objects: 100%
Writing objects: 100%
To https://github.com/yourusername/myrepo.git
 * [new branch]      fix-login-bug -> fix-login-bug
Branch 'fix-login-bug' set up to track remote branch 'fix-login-bug' from 'origin'.
```

After the first push with `-u`, a plain `git push` is sufficient on subsequent commits.

### Step 4 — Open a Pull Request

You can open a PR through the GitHub web UI, or directly from the terminal using the **`gh` CLI**.

```bash
gh pr create --title "Fix login null pointer bug" --body "Fixes #42 — prevents a crash when the password field is empty."
```

```text
https://github.com/yourusername/myrepo/pull/1
```

That single line opens the PR and prints the URL. From this point on, teammates can review, comment, and approve.

#### Anatomy of a Great PR Description

A good PR description has three parts:

1. **What does this change?** — Describe the feature, fix, or refactor.
2. **Why is this needed?** — Provide context. Link to the related issue.
3. **How was it tested?** — Steps to verify the fix works.

### Step 5 — Code Review

Reviewers examine the code, leave comments, and either:

- **Approve** — ready to merge
- **Request changes** — something needs to be fixed first
- **Comment** — general feedback, no formal approval or blocking

As the author, you reply to comments, push additional commits, or dismiss review comments. The PR is a living thread until it is merged or closed.

### Step 6 — Merge the PR

Once approved, there are three merge strategies to choose from:

| Strategy | What happens | When to use |
|---|---|---|
| **Merge commit** | Creates a merge commit that ties the two histories together | Teams wanting a full history |
| **Squash and merge** | Compresses all commits into one | Feature branches with many small commits |
| **Rebase and merge** | Replays your commits on top of main | Clean, linear history |

To merge via `gh`:

```bash
gh pr merge 1 --squash --delete-branch
```

```text
// If using squash merge:
Merged pull request #1 (Fix login null pointer bug)
✓ Squashed 1 commit into main
✓ Deleted branch fix-login-bug, as you requested

// If using a regular merge commit:
Merged pull request #1 (Fix login null pointer bug)
✓ Merged branch fix-login-bug into main
✓ Deleted branch fix-login-bug, as you requested
```

GitHub also provides merge buttons in the web UI with all three options.

### Step 7 — Delete the Branch

After merging, delete the feature branch both locally and on the remote. `gh pr merge` with `--delete-branch` (shown above) handles the remote side. Clean up locally with:

```bash
git checkout main
git pull origin main
git branch -d fix-login-bug
```

```text
Deleted branch fix-login-bug (was a1b2c3d).
```

---

## GitHub Issues

### What Is an Issue?

An **Issue** is a record of a task, bug, or feature request associated with a repository. Issues are the primary tool for tracking work independently of code changes. They let anyone — the team, users, contributors — report problems or suggest improvements in a structured way.

You can create an issue to:
- Report a bug
- Request a new feature
- Track a known problem
- Plan a refactor
- Ask a question

### Creating Issues via the Web UI

On GitHub, navigate to your repository and click the **Issues** tab, then click **New issue**. Fill in:
- A clear, descriptive **title**
- A **body** describing the problem or suggestion in detail
- **Labels** to categorise (e.g. `bug`, `enhancement`, `good first issue`)
- **Assignees** to delegate responsibility
- **Milestones** to group related issues by target release

### Creating Issues via `gh`

You can create issues directly from the terminal:

```bash
gh issue create --title "Login form crashes on empty password" --body "Steps to reproduce:
1. Navigate to /login
2. Leave the password field empty
3. Click Submit
Expected: validation message appears
Actual: application throws NullPointerException"
```

```text
https://github.com/yourusername/myrepo/issues/42
```

### Listing and Viewing Issues

```bash
gh issue list
```

```text
Showing 3 open issues in yourusername/myrepo

#42  bug       Login form crashes on empty password       about 1 hour ago
#41  enhancem  Add dark mode support                      about 1 day ago
#40  question  How do I reset my password?                about 3 days ago
```

```bash
gh issue view 42
```

```text
Login form crashes on empty password
Labels: bug
Assignees: yourusername
Milestone: v2.1.0
Opened by: yourusername
---
Steps to reproduce:
1. Navigate to /login
2. Leave the password field empty
3. Click Submit
Expected: validation message appears
Actual: application throws NullPointerException
```

### Closing Issues

You can close an issue manually:

```bash
gh issue close 42
```

Or you can close it automatically — this is one of the most powerful GitHub automations.

---

## Linking PRs to Issues

### The `Closes` / `Fixes` / `Resolves` Keywords

When you write a commit message or PR description, you can include one of these keywords followed by an issue number:

| Keyword | Effect |
|---|---|
| `Closes #42` | Closes issue #42 when the PR is merged |
| `Fixes #42` | Closes issue #42 and marks it as fixed |
| `Resolves #42` | Closes issue #42 and marks it as resolved |

**Example PR body:**

```text
## What does this PR do?
Adds client-side validation to the login form so an empty password is
rejected before it reaches the server.

## Why is this needed?
Fixes #42 — the empty password field causes a NullPointerException.

## Testing
1. Navigate to /login
2. Leave password blank and click Submit
3. Verify a validation message appears instead of a crash
```

When this PR is merged, GitHub automatically closes issue #42 and adds a link from the issue to the PR.

### Multiple Issues

You can close multiple issues at once:

```text
Closes #42
Closes #43
Closes #44
```

Or use a list in the PR description. Each referenced issue gets updated automatically.

---

## Draft Pull Requests

### What Is a Draft PR?

A **Draft Pull Request** is a PR that is explicitly marked as a work in progress. It cannot be merged, and reviewers are not automatically assigned. Draft PRs are useful when:

- You want early feedback before the work is complete
- You want CI to run on your branch before investing time in review
- The feature is large and you want to track progress incrementally

### Creating a Draft PR

```bash
gh pr create --draft --title "Implement dark mode" --body "Work in progress — not ready for review"
```

```text
https://github.com/yourusername/myrepo/pull/3
```

The PR will appear with a `Draft` badge on GitHub. When you are ready for review, click the **"Ready for review"** button in the GitHub UI, or convert it with:

```bash
gh pr ready 3
```

```text
https://github.com/yourusername/myrepo/pull/3
Pull request #3 is now ready for review
```

### Quick Reference: `gh pr` Commands

```bash
gh pr create --title "..." --body "..."          # Open a new PR
gh pr create --draft --title "..."                # Open a draft PR
gh pr list                                         # Show open PRs
gh pr view 1                                       # View a specific PR
gh pr status                                       # Show PRs for current branch
gh pr ready 1                                      # Convert draft to ready
gh pr merge 1 --squash --delete-branch            # Merge and clean up
gh pr close 1                                      # Close a PR without merging
```

---

## Exercise

### Scenario

You are a developer on a team. Someone has reported that the login page crashes when the username field is left blank. Your task is to fix this bug and open a PR that closes the issue.

### Tasks

1. Create an issue for the bug using `gh issue create` (simulate the issue creation)
2. Create a new branch named `fix-blank-username-crash`
3. Make a commit on that branch with the message `"Fixes #42 — validate username before submission"`
4. Push the branch with upstream tracking
5. Open a PR that references the issue using `gh pr create`
6. Merge the PR using squash merge and delete the branch
7. Verify the issue was closed

### Hints

- Use `git checkout -b` to create and switch to a new branch in one step.
- Use `--set-upstream` (`-u`) only on the first push.
- Use `gh pr create --title "..." --body "..."` to open the PR.
- Use `Closes #N` or `Fixes #N` in the PR body to link it to an issue.
- Use `gh pr merge --squash --delete-branch` to merge and delete in one command.

---

## Solution

Below is a complete, step-by-step walkthrough with all commands and their expected outputs.

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

### What You Just Did

1. Created an issue to track the bug — giving the team a single source of truth.
2. Created a feature branch to isolate the fix from `main`.
3. Committed the fix with `Fixes #42` — this links the commit to the issue.
4. Pushed the branch and opened a PR — inviting review.
5. Merged the PR with squash merge — keeping the `main` history clean.
6. Verified the issue auto-closed — the whole workflow is connected.

This workflow is the backbone of how modern software teams collaborate on GitHub. From issue to PR to merge, every step is traceable and reversible.

---

## Quick Reference

| Action | Command |
|---|---|
| Open PR from current branch | `gh pr create --title "..." --body "..."` |
| Open draft PR | `gh pr create --draft --title "..."` |
| List open PRs | `gh pr list` |
| View a PR | `gh pr view 1` |
| Check PR status for current branch | `gh pr status` |
| Mark draft PR as ready | `gh pr ready 1` |
| Merge a PR | `gh pr merge 1 --squash --delete-branch` |
| Close a PR without merging | `gh pr close 1` |
| Create an issue | `gh issue create --title "..." --body "..."` |
| List open issues | `gh issue list` |
| View an issue | `gh issue view 42` |
| Close an issue | `gh issue close 42` |
| Auto-close via commit message | `Fixes #42` in commit or PR body |

---

[← Previous: GitHub Repos and Forks](./08-github-repos-and-forks.md) · [Next: Code Review →](./10-code-review.md)