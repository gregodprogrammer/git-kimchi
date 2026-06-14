# Merging

[← Previous: Branching](./05-branching.md) | [← Back to Index](./00-index.md)

So far you've learned how to create branches and switch between them. But branches only become useful when you **combine** them. Merging is the process of integrating changes from one branch into another, bringing your divergent histories back together.

---

## What Is a Merge?

A **merge** in Git combines the histories of two or more branches. When you merge a feature branch into `main`, Git takes all the commits from the feature branch and integrates them into the target branch's history. The result is a single, unified branch that contains changes from both places.

Think of it this way: if you've been working on a `login-feature` branch while someone else has been adding tests to `main`, a merge is how you bring those login changes into `main` without losing anyone's work.

---

## The `git merge` Command

The basic syntax is:

```bash
git merge <branch-name>
```

**Critical rule:** You must be on the branch that will **receive** the changes (the target), and you merge the source branch *into* it.

For example, to merge `login-feature` into `main`:

```bash
git switch main
git merge login-feature
```

The current branch (`main` in this case) is where the result ends up. The source branch (`login-feature`) is not modified — its history remains as-is.

---

## Fast-Forward Merge

A **fast-forward** merge happens when the target branch has not moved forward since the source branch was created. Git can simply "fast-forward" the target pointer to the same commit as the source branch, because there is a clear linear path.

### When It Happens

You branched off `main` at commit `A`. Since then, `main` has not changed — no new commits were added to `main`. Your branch has two new commits (`B` and `C`). Git can just move `main`'s pointer forward to `C`.

### Example

```bash
git switch main
git merge feature
```

```text
Updating a1b2c3d..e4f5g6h
Fast-forward
 README.md | 2 ++
 1 file changed, 2 insertions(+)
```

Git reports "Fast-forward" and does not create a merge commit. The history remains a single straight line. This is clean and simple — but it only works when the branches have not diverged.

---

## Three-Way Merge

A **three-way merge** is necessary when both the target branch and the source branch have moved forward since they diverged. Git must combine the changes from both branches, which may involve different modifications to the same lines of code.

Because neither branch is simply ahead of the other, Git creates a new **merge commit** that has two parent commits — one from each branch. This merge commit ties the two histories together.

### When It Happens

You branched off `main` at commit `A`. Meanwhile, someone else committed to `main` (commit `B`). Your branch also has commits (commit `C`). Now `main` and your branch have "diverged" — they both contain unique commits that the other doesn't have. Git must perform a three-way merge.

### Example

```bash
git switch main
git merge feature
```

```text
Merge made by the 'ort' strategy.
 README.md | 2 ++
 1 file changed, 2 insertions(+)
```

Git combines the changes and creates a merge commit. Your history now looks like:

```text
*---.
 \  \
  A--B--C--M
         /
   (main)
```

Commit `M` is the merge commit, with two parents: `B` (from `main`) and `C` (from `feature`).

---

## Forcing a Merge Commit with `--no-ff`

Even when a fast-forward merge is possible, you might want to explicitly record that a branch was merged. The `--no-ff` flag forces Git to create a merge commit regardless of whether a fast-forward would work.

```bash
git merge --no-ff feature
```

### Why Use It?

- **Preserves branch history** — In tools like GitHub's network graph or `git log --graph`, you can clearly see when a feature branch was integrated.
- **Auditing** — A merge commit stands out as a landmark in the history, making it easier to trace when features landed.
- **Reversibility** — Reverting a merge commit is cleaner than trying to "un-fast-forward" a branch.

For long-lived feature branches that you want to see clearly in the history, `--no-ff` is the conventional choice.

---

## Merge Conflicts

A merge conflict happens when Git cannot automatically resolve differences between two branches. This occurs when **both branches modified the same lines** of the same file, or when one branch deleted a file that another branch modified.

### Why Conflicts Happen

Git is very good at combining changes automatically when they touch different parts of a file. But when two people both edit line 15 of `config.py`, Git doesn't know which change to keep. It pauses the merge and asks you to decide.

### How Git Marks Conflicts

When a conflict occurs, Git inserts special markers into the conflicted file:

```text
<<<<<<< HEAD
Changes from the current branch (main)
=======
Changes from the branch you're merging in (feature)
>>>>>>> feature
```

- `<<<<<<< HEAD` marks the start of the conflict and the beginning of the current branch's content.
- `=======` separates the two versions.
- `>>>>>>> feature` marks the end of the conflict and the incoming branch's content.

### Viewing Conflict Status

```bash
git status
```

```text
On branch main
You have unmerged paths.
  (fix conflicts and run "git commit")

Unmerged paths:
  (use "git add <file>...")

        both modified:   config.py

no changes added to commit (use "git add" and/or "git commit")
```

The phrase **"both modified"** tells you this is a conflict between two branches that both changed the file.

### Resolving a Conflict Manually

1. **Open the conflicted file** and find the `<<<<<<<`, `=======`, and `>>>>>>>` markers.
2. **Decide what the final content should be.** Delete the markers and keep the version you want (or combine both changes manually).
3. **Add the resolved file:**

   ```bash
   git add config.py
   ```

4. **Complete the merge with a commit** (Git pre-fills a merge commit message for you):

   ```bash
   git commit
   ```

   ```text
   Merge branch 'feature' into main
   ```

Git automatically opens your editor for the commit message. The default message is fine — just save and close it.

### Aborting a Merge

If you've made a mess of conflict resolution and want to start over, you can abort the merge entirely:

```bash
git merge --abort
```

This returns your repository to the state it was in before you started the merge. No changes are lost — you can try again once you've prepared better.

---

## Visualizing Merge History with `git log --graph`

After merging, `git log` shows you a linear list of commits. But it doesn't show you the branch structure. Adding `--graph` draws an ASCII art diagram that reveals the topology of your history.

```bash
git log --oneline --graph --all
```

```text
*   Merge branch 'feature' into main
|\
| * e4f5g6h Add login page
* | a1b2c3d Update README
|/
* a9b1c2d Initial commit
```

Each asterisk `*` is a commit. The backslash `\`, vertical bar `|`, and forward slash `/` characters show where branches split and merged.

The `--all` flag ensures Git shows branches other than the current one. Combined with `--oneline`, it gives you a compact but informative view of your project's history.

---

## Exercise

In this exercise, you will practice both a fast-forward merge and a conflict-causing merge, then resolve the conflict manually.

### Scenario

You are working on a project with a `main` branch. You create two branches from `main`, make different changes to the same file on each branch, and merge them one at a time. The second merge will produce a conflict that you will resolve.

### Tasks

1. Initialize a new Git repository with one commit on `main`.
2. Create a branch called `branch-a` and add a line to a file called `notes.txt`.
3. Create a branch called `branch-b` from `main` (not from `branch-a`) and add a *different* line to `notes.txt` on the same line number.
4. Merge `branch-a` into `main` (expect fast-forward).
5. Merge `branch-b` into `main` (expect a conflict).
6. Resolve the conflict by keeping both changes in `notes.txt`.
7. Complete the merge commit and verify the final file contains both lines.

### Estimated Time

15–20 minutes.

---

## Solution

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

no changes added to commit (use "git add" and/or "git commit")
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

### Cleanup

```bash
cd ..
rm -rf merge-practice
```

---

## Key Takeaways

- A **fast-forward** merge is only possible when the target branch has not advanced since the source branch was created. It creates no merge commit and results in a linear history.
- A **three-way merge** is needed when both branches have advanced. Git creates a merge commit with two parents to join the histories.
- Use `git merge --no-ff` when you want to preserve the fact that a branch was merged, even if a fast-forward would have been possible.
- Merge conflicts happen when both branches modified the same lines. Git marks the conflict with `<<<<<<<`, `=======`, and `>>>>>>>` markers. You decide which version to keep, add the file, and commit.
- `git merge --abort` lets you back out of a conflicted merge if you need to start fresh.
- `git log --oneline --graph --all` reveals the true shape of your history, including branches and merges.

---

[← Previous: Branching](./05-branching.md) | [Next: Remotes →](./07-remotes.md)