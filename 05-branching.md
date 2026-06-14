# Branching

[← Previous: Undoing Changes](./04-undoing-changes.md) · [← Back to Index](./00-index.md)

In the projects you've worked on so far, every commit lives on a single line of history. That works fine for solo experiments, but real software involves multiple people simultaneously: someone is adding a login feature while another person fixes a bug in the payments code, and neither wants to interfere with the other until the work is proven solid. Branching is the mechanism that makes this possible.

A **branch** is an independent line of development. Think of it as a parallel universe for your codebase — changes you make on one branch don't affect any other branch until you explicitly bring them together (merged). Git's branching is cheap, local, and safe. Unlike older version control systems that copied entire directories, Git stores branches as lightweight pointers to commits, making it trivial to create, switch, and delete branches without consuming significant resources.

---

## Why Branch?

Branches solve three fundamental problems in collaborative software development:

**Isolation for features and experiments.** When you start working on a new feature, you don't want its half-finished code sitting in the main project and breaking things for everyone else. Creating a branch gives you a private sandbox. You can commit freely, experiment with different approaches, and only share the result when it's ready.

**Safe bug fixes.** A critical bug report comes in while your team is in the middle of a large refactor. Branching lets you hot-fix the production issue on a separate branch without destabilizing the in-progress work — you fix the bug in isolation, then merge the fix back into main alongside the refactor.

**Parallel development streams.** Multiple team members can work on separate features simultaneously, each on their own branch. When feature A is done, it gets reviewed and merged. When feature B is done, it follows the same path. Nothing blocks anything else.

The `main` (or `master`, depending on your git version) branch is the default and typically represents the canonical, deployable state of your project. Other branches feed into it through code review and merging — topics covered in the next two sections.

---

## Listing and Managing Branches

### Viewing Branches

The `git branch` command lists all local branches in your repository. The current branch is marked with an asterisk (`*`):

```bash
git branch
```

```text
* main
  feature-login
  hotfix-payment-bug
```

In this output, `main` is the active branch (you are "on" main). The other branches exist in the repository but you haven't switched to them yet.

### Creating a Branch

To create a new branch without switching to it, pass the branch name to `git branch`:

```bash
git branch feature-dark-mode
```

Running `git branch` again shows the new branch exists, but you are still on `main`:

```bash
git branch
```

```text
  feature-dark-mode
* main
```

Creating a branch does not switch you to it. The new branch starts at the same commit you are currently on — it shares the same history up to that point.

### Deleting a Branch

When a branch's work is done and merged (or abandoned), you can delete it:

```bash
git branch -d feature-dark-mode
```

```text
Deleted branch feature-dark-mode (was a3f7d21).
```

Git protects you from accidentally deleting a branch that hasn't been merged. If you try to delete an unmerged branch, you'll see a warning:

```bash
git branch -d feature-abandoned-work
```

```text
error: The branch 'feature-abandoned-work' is not fully merged.
If you are sure you want to delete it, run 'git branch -D feature-abandoned-work'.
```

The lowercase `-d` flag is *safe* — it refuses to delete unless the branch's commits are already integrated somewhere else. The uppercase `-D` flag forces deletion regardless:

```bash
git branch -D feature-abandoned-work
```

```text
Deleted branch feature-abandoned-work (was 8c2e101).
```

Use `-D` with caution. Unmerged commits on a deleted branch are unrecoverable (unless you referenced them elsewhere).

### Renaming a Branch

If you named a branch incorrectly, you can rename it while on the branch:

```bash
git branch -m feature-old-name feature-correct-name
```

Or rename a different branch while on any branch:

```bash
git branch -m feature-old-name feature-correct-name
```

There is no output on success — the rename is silent.

---

## Switching Branches with `git switch`

Git 2.23 introduced `git switch` as a cleaner replacement for the legacy `git checkout` command (covered below). Use `git switch` in all new work unless you are on an older Git version.

### Switching to an Existing Branch

To switch from your current branch to another branch:

```bash
git switch feature-login
```

```text
Switched to branch 'feature-login'
```

Git moves your working directory to match the latest commit on that branch. Any uncommitted changes in your working directory must either be committed or stashed (covered in a later section) before switching — otherwise Git refuses the switch to prevent losing work.

### Switching Back to Main

```bash
git switch main
```

```text
Switched to branch 'main'
```

---

## Switching Branches with `git checkout` (Legacy)

The `git checkout` command has been the traditional way to switch branches in older Git versions. It still works, but `git switch` is preferred in modern Git because its name is more intuitive — `checkout` historically did too many different things (switch branches, restore files, create new branches).

To switch branches with `git checkout`:

```bash
git checkout feature-login
```

```text
Switched to branch 'feature-login'
```

To switch back:

```bash
git checkout main
```

```text
Switched to branch 'main'
```

Throughout this guide, `git switch` is the primary command shown. If your system has an older Git version that predates 2.23, substitute `git checkout` for any `git switch` command — they are functionally equivalent for branch switching.

---

## Creating and Switching in One Step

Typing two commands — create the branch, then switch to it — is common enough that Git provides a shortcut. The `-c` flag (create and switch) does both at once:

```bash
git switch -c feature-user-profile
```

```text
Switched to a new branch 'feature-user-profile'
```

The equivalent with `git checkout` (the legacy approach):

```bash
git checkout -b feature-user-profile
```

```text
Switched to a new branch 'feature-user-profile'
```

Both commands create the branch at your current location and immediately check it out. After running either, you are on the new branch and ready to start committing.

---

## A Basic Branching Workflow

The typical day-to-day workflow with branches follows a consistent pattern:

**1. Create a branch for your work.**

```bash
git switch -c feature-newsletter
```

```text
Switched to a new branch 'feature-newsletter'
```

**2. Make commits on that branch.** Every commit you make on `feature-newsletter` is isolated from `main`.

```bash
echo "# Newsletter Signup" > newsletter.md
git add newsletter.md
git commit -m "Add newsletter signup page"
```

```text
[feature-newsletter abc1234] Add newsletter signup page
 1 file changed, 1 insertion(+)
 create mode 100644 newsletter.md
```

**3. Switch back to `main` when you need to context-shift.** For example, a colleague asks you to review their work, or a production issue comes in.

```bash
git switch main
```

```text
Switched to branch 'main'
```

Notice that after switching to `main`, the `newsletter.md` file you just created and committed on `feature-newsletter` is gone from your working directory — it exists only on that branch. This is the core of branching isolation.

**4. When your feature is ready, merge the branch into `main`.** Merging is covered in detail in the next section. For now, know that the command is:

```bash
git merge feature-newsletter
```

This brings the isolated work back into the main line.

This cycle — create, commit, switch, merge — is the foundation of all Git branching workflows. Small teams may share branches directly; larger teams push branches to a remote and open pull requests for review before merging. Both patterns build on the same core mechanism.

---

## Tracking Branches

When you clone a repository that has branches on the remote, your local branches start with no upstream tracking by default. The `git branch -vv` command shows which local branches are tracking remote branches:

```bash
git branch -vv
```

```text
* main              a3f7d21 [origin/main] Add homepage hero section
  feature-login     8c2e101 Add login form stub
  feature-dashboard 5d9a3c7 [origin/dashboard] Add dashboard layout
```

Each branch with `[origin/branch-name]` is tracking a remote branch. `feature-login` has no tracking configured — it exists only locally. `main` and `feature-dashboard` are tracking their remote counterparts.

Tracking is set automatically when you clone or when you create a branch with `git switch -t origin/branch-name`. When a branch tracks a remote, Git can show you how many commits your local branch is ahead or behind the remote with `git fetch` followed by `git status`.

---

## Exercise

In this exercise you will practice creating branches, switching between them, committing changes, and observing how commits are isolated per branch.

### Scenario

You are working on a documentation site. While preparing a draft of the user guide, you remember you need to fix an urgent typo in the README. You will use branching to handle both tasks without mixing them together.

### Tasks

1. Initialize a new Git repository in a directory called `branch-practice`.
2. Create an initial commit with a `README.md` file containing the text `Project Alpha v1.0`.
3. Create a branch called `fix-typo` and switch to it.
4. On `fix-typo`, fix the typo by changing the README content to `Project Alpha v1.1`.
5. Commit the fix on `fix-typo`.
6. Switch back to `main`.
7. On `main`, create a commit that adds a `docs/user-guide.md` file (any placeholder content is fine).
8. Verify that the typo fix from step 5 does NOT appear in the README on `main`.
9. Verify that the `docs/user-guide.md` file you created on `main` does NOT exist on `fix-typo`.

---

## Solution

### Step-by-step

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

## Key Takeaways

- `git branch` lists local branches; the asterisk marks the current branch.
- `git switch -c <branch>` creates and switches to a new branch in one step.
- `git switch <branch>` switches to an existing branch.
- Commits made on one branch are invisible on all other branches — this isolation is the point.
- Always switch back to `main` (or your integration branch) before starting new, unrelated work.
- Delete branches with `-d` once their work is merged, and with `-D` only for truly unwanted branches.

[Next: Merging →](./06-merging.md)