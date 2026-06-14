# Undoing Changes

[← Previous: History and Diff](./03-history-and-diff.md)

Git's safety net is one of its best features. Almost everything you do can be undone. However, choosing the **wrong undo method** can create confusion or even lose work. This section teaches you the right tool for each situation.

The golden rule: **Git rarely destroys data permanently — but `git reset --hard` is the exception.** Understand each command before you run it.

---

## When to Undo

You will need to undo changes in several common situations:

- You edited a file but decided the changes were wrong
- You ran `git add` on a file you didn't want to stage
- You committed too early or forgot to include a file
- You merged or pulled something that broke your code
- You used `git reset` and need to find lost work

**The key question is:** Are your changes in the working tree, the staging area, or the commit history? Each location requires a different approach.

---

## Discarding Working Directory Changes

When you have edited a file but want to throw away those changes, you have two options. Both commands only affect the **working tree** — your commits stay safe.

### Using `git restore` (Git 2.23+)

The modern, recommended approach:

```bash
git restore README.md
```

```text
# No output means success — the file is back to its last committed state
```

`git restore` reads the file from the index (or the last commit if the file was never staged) and overwrites your working copy.

### Using `git checkout` (Legacy)

Older tutorials and scripts may show this syntax:

```bash
git checkout -- README.md
```

```text
# Same result — file reverted, no output
```

The `--` separates the branch name from the file path, preventing accidental branch switches.

### When to Use Each

| Command | What it does | Safety |
|---------|--------------|--------|
| `git restore <file>` | Reverts working tree | Safe — commits unchanged |
| `git checkout -- <file>` | Same, legacy syntax | Safe — commits unchanged |

Use `git restore`. It was introduced in Git 2.23 specifically to remove the ambiguity of `git checkout`, which does many different things.

---

## Unstaging Files

You ran `git add` on a file too soon. You want it back out of the staging area but keep your working changes.

### Using `git restore --staged`

```bash
git restore --staged README.md
```

```text
# File removed from staging, changes remain in working tree
```

Your edits to `README.md` are still there — it's just no longer staged for commit.

### Using `git reset` (Legacy)

```bash
git reset HEAD README.md
```

```text
# Same result — file unstaged, but not lost
```

`HEAD` here refers to the current commit. `git reset` moves the current branch's tip back, but without `--hard`, it only updates the staging area.

### Practical Example

```bash
echo "notes for tomorrow" >> TODO.txt
git add TODO.txt
git status
```

```text
On branch main
Changes to be committed:
  (use "git restore --staged <file>..." to update)
        modified:   TODO.txt

git reset HEAD TODO.txt
Unstaged changes after reset:
M   TODO.txt
```

After unstaging, your `TODO.txt` changes are still in the working tree, ready to edit further or stage again later.

---

## Resetting Commits

Sometimes you committed too early or on the wrong branch. `git reset` moves the branch tip backward. The key difference is what happens to your working tree and staging area.

### Three Modes

```bash
git reset --soft HEAD~1   # Keep changes staged
git reset --mixed HEAD~1  # Keep changes unstaged (default)
git reset --hard HEAD~1   # Destroy changes completely
```

### `--soft`: Keep Everything Staged

Your changes are preserved and staged. Useful for combining commits:

```bash
git commit -m "Fix typo"
git commit -m "Add feature"
# Oops — these should be one commit
git reset --soft HEAD~1
git commit -m "Fix typo and add feature"
```

After `--soft HEAD~1`, your second commit's changes are back in the staging area, ready to be recommitted.

### `--mixed`: Keep Changes Unstaged

This is the **default behavior**. Changes are preserved but unstaged:

```bash
git commit -m "WIP feature that needs more work"
git reset --mixed HEAD~1
```

```text
Unstaged changes after reset:
M   src/main.py
```

Your changes to `src/main.py` are still there, but not staged. You can continue editing, then commit correctly.

### `--hard`: Destroy Changes Completely

**Warning:** This deletes your uncommitted work permanently.

```bash
git reset --hard HEAD~1
```

```text
HEAD is now at a3f2b1c Added initial project structure
```

Everything you had in the working tree and staging area is gone. Only the commit remains.

### Safety Rule

> **Never use `git reset --hard` unless you are certain you don't need your changes.**
>
> If you might need the work later, run `git reflog` first to find your current position, or use `--soft` or `--mixed`.

A safer workflow before a hard reset:

```bash
# Create a backup branch just in case
git branch backup-before-reset
git reset --hard HEAD~1
```

If you realize you made a mistake:

```bash
git checkout backup-before-reset  # Go back to your backup
```

---

## Reverting Commits

Unlike `git reset`, `git revert` creates a **new commit** that undoes a previous one. This is safe for shared or published history because it doesn't rewrite history.

### When to Use Revert

- You pushed a commit to a shared branch (like `main` or `develop`)
- You need to undo a merge commit
- You want to keep history intact while removing a change

### Basic Revert

```bash
git revert a3f2b1c
```

Git opens your editor to write a commit message:

```text
Revert "Added initial project structure"

This reverts commit a3f2b1c7d8e9f.
```

Save and close the editor:

```text
[main (root-commit) 9b4d2e1] Revert "Added initial project structure"
 1 file changed, 0 insertions(+), 0 deletions(-)
```

The original commit is still in the history. A new commit that undoes it now sits on top.

### Revert with No Editor

Skip the editor prompt with `-m`:

```bash
git revert a3f2b1c --no-edit
```

```text
[main 9b4d2e1] Revert "Added initial project structure"
 1 file changed, 0 insertions(+), 0 deletions(-)
```

### Handling Revert Conflicts

If the same lines were modified since the commit you're reverting, you may get a conflict:

```bash
git revert a3f2b1c
```

```text
error: could not revert a3f2b1c "Added initial project structure"
hint: Resolve conflicts manually and mark them as resolved
hint: Run "git revert --abort" to abandon the revert
```

You have two choices:

**Abort the revert** (abandon the operation):

```bash
git revert --abort
```

```text
# Revert abandoned, back to previous state
```

**Resolve and continue:**

```bash
# Edit the conflicted files manually
git add conflicted-file.txt
git revert --continue
```

### Reverting a Merge Commit

Merge commits have two parents. You must tell Git which parent to revert:

```bash
git revert -m 1 abc1234
```

`-m 1` means "keep the first parent's changes" — undoing the merge as if the branch was never merged.

---

## The Reflog: Your Safety Net

The reflog records every movement of `HEAD`. Even if you use `git reset --hard`, the reflog remembers where you were a moment ago.

### Viewing the Reflog

```bash
git reflog
```

```text
a3f2b1c HEAD@{0}: commit: Added feature
9b4d2e1 HEAD@{1}: reset: moving to HEAD~1
7c3e8a2 HEAD@{2}: commit: Fix typo
1a9d6f4 HEAD@{3}: clone: from https://github.com/example/repo.git
```

Each entry shows:
- The commit hash
- The action that moved HEAD
- The commit message (if any)

### Recovering from a Bad Reset

You used `--hard` and lost work:

```bash
git reflog
```

```text
a3f2b1c HEAD@{0}: reset: moving to HEAD~1
7c3e8a2 HEAD@{1}: commit: Work in progress
```

Your lost work was at `7c3e8a2`. Restore it:

```bash
git reset --hard HEAD@{1}
```

```text
HEAD is now at 7c3e8a2 Work in progress
```

### Alternative: Using `git checkout` with Reflog

For a more cautious recovery, checkout the old state as a detached HEAD:

```bash
git checkout HEAD@{1}
```

```text
Note: switching to 'HEAD@{1}'.
You are in 'detached HEAD' state...
```

This lets you inspect the old state before deciding what to do with it.

### When Reflog Expires

The reflog is local to your repository. It expires by default after 90 days for reachable commits, or 30 days for unreachable (orphaned) commits. Do not rely on it as a long-term backup — commits you need long-term should be properly branched.

---

## Exercise

### Scenario

You're working on a project and made several mistakes:

1. You added a change to `config.txt` and staged it
2. You then accidentally committed it with the wrong message
3. You realize the committed change was actually correct, but the message was wrong

Your task: Fix the commit message but keep the actual changes.

### Steps

1. Initialize a new repository or use an existing one
2. Create a file called `config.txt` with some content
3. Stage and commit it (with a temporary message like "WIP")
4. Edit `config.txt` to add more content
5. Stage and commit again (with another temporary message)
6. Use `git log --oneline` to see your commits
7. Change the last commit message to something meaningful
8. Verify with `git log --oneline`

### Hint

Think about which reset mode keeps your changes staged and lets you recommit with a new message.

---

## Solution

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

## Summary

| Situation | Command |
|-----------|---------|
| Discard working tree changes | `git restore <file>` |
| Unstage a file | `git restore --staged <file>` |
| Undo last commit, keep staged | `git reset --soft HEAD~1` |
| Undo last commit, keep unstaged | `git reset --mixed HEAD~1` |
| Destroy last commit entirely | `git reset --hard HEAD~1` |
| Safe undo of a public commit | `git revert <commit>` |
| Find lost commits | `git reflog` |

Remember: **Safety first.** When in doubt, use `--soft` or `--mixed` instead of `--hard`, and check `git reflog` before panic.

[Next: Branching →](./05-branching.md)

[← Back to Index](./00-index.md)