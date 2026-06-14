# Remotes

[← Previous: Merging](./06-merging.md) | [← Back to Index](./00-index.md)

So far, everything we've done has been local — commits, branches, and merges all exist only on your machine. But Git's real power is collaboration, which requires sharing code between computers. That's what remote repositories are for.

A **remote** is a copy of your Git repository hosted on another server. When you push code to a remote, you're uploading your commits so others can pull them down. Popular remote hosting services include GitHub, GitLab, Bitbucket, and Gitea.

## What Is a Remote?

Think of a remote as a shared Dropbox for your Git history. Each collaborator has their own local copy, and they sync changes through a central remote. The remote doesn't just store your latest code — it stores your entire commit history, all branches, and all tags.

By convention, the default remote is named `origin`. You can have multiple remotes, but `origin` is the standard name for your primary source of truth.

```text
┌─────────────────────────────────────────────────────────────────┐
│                         REMOTE SERVER                           │
│                     (GitHub, GitLab, etc.)                      │
│                                                                 │
│   origin:  main  ·  feature-login  ·  develop  ·  commit abc123 │
└─────────────────────────────────────────────────────────────────┘
            │ push/pull              │ push/pull
            ▼                       ▼
┌─────────────────────┐     ┌─────────────────────┐
│   YOUR COMPUTER     │     │   COLLABORATOR      │
│                     │     │                     │
│   main              │     │   main              │
│   feature-login     │     │   feature-dashboard │
│   develop           │     │                     │
└─────────────────────┘     └─────────────────────┘
```

## Listing Remotes with `git remote -v`

Before adding or modifying remotes, it's good to see what you already have. The `-v` flag (verbose) shows both the fetch and push URLs for each remote.

```bash
# Check existing remotes in your repository
git remote -v
```

```text
origin  https://github.com/username/repo.git (fetch)
origin  https://github.com/username/repo.git (push)
```

If you haven't added any remotes yet, you'll see nothing:

```text
# No output means no remotes configured
```

A fresh `git init` creates a local repository with no remotes. You need to add one explicitly.

## Adding a Remote with `git remote add`

To connect your local repository to a remote server, use `git remote add`. The command takes a name (usually `origin`) and a URL.

```bash
# Add a remote named 'origin' pointing to your GitHub repository
git remote add origin https://github.com/username/my-project.git
```

After adding, verify it worked:

```bash
git remote -v
```

```text
origin  https://github.com/username/my-project.git (fetch)
origin  https://github.com/username/my-project.git (push)
```

You can add multiple remotes if you collaborate with different providers:

```bash
# Add GitHub as origin
git remote add origin https://github.com/username/my-project.git

# Add a colleague's fork as a separate remote
git remote add colleague https://github.com/colleague/my-project.git

# Verify both remotes are configured
git remote -v
```

```text
origin     https://github.com/username/my-project.git (fetch)
origin     https://github.com/username/my-project.git (push)
colleague  https://github.com/colleague/my-project.git (fetch)
colleague  https://github.com/colleague/my-project.git (push)
```

### HTTPS vs. SSH URLs

When adding remotes, you'll encounter two URL formats:

**HTTPS URLs** (recommended for beginners):
```text
https://github.com/username/repo.git
```
- Works out of the box with no configuration
- Requires username/password or personal access token
- Can use GitHub CLI (`gh auth login`) for seamless authentication

**SSH URLs**:
```text
git@github.com:username/repo.git
```
- Requires SSH key setup (`ssh-keygen`)
- No username/password prompts after initial configuration
- Slightly shorter commands for some operations

For this tutorial, we'll use HTTPS URLs. If you want to switch to SSH later, see the Advanced Git section.

## Managing Remotes

### Renaming a Remote

If you accidentally added a remote with the wrong name, or you want a more descriptive name, you can rename it:

```bash
# Rename 'origin' to 'github'
git remote rename origin github

# Verify the change
git remote -v
```

```text
github  https://github.com/username/my-project.git (fetch)
github  https://github.com/username/my-project.git (push)
```

### Removing a Remote

To disconnect from a remote entirely, use `git remote remove`:

```bash
# Remove the 'github' remote
git remote remove github

# Verify it's gone
git remote -v
```

```text
# No output — no remotes configured
```

**Caution**: Removing a remote doesn't delete any local branches or commits. It only removes the connection to that server. Your local history is safe.

## Pushing to a Remote with `git push`

Pushing uploads your local commits to the remote repository. Let's cover the common scenarios.

### Your First Push: Setting Upstream with `-u`

When you push a branch for the first time, Git doesn't know which remote branch to track. The `-u` (or `--set-upstream`) flag establishes that connection:

```bash
git push -u origin main
```

```text
Enumerating objects: 5, done.
Counting objects: 100% (5/5), done.
Writing objects: 100% (3/3), 243 bytes | 243.00 KiB/s, done.
To https://github.com/username/my-project.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

After using `-u`, Git remembers the upstream relationship. Future pushes from this branch are simpler.

### Subsequent Pushes

Once the upstream is set, just run `git push` without arguments:

```bash
git push
```

```text
Enumerating objects: 3, done.
Counting objects: 100% (3/3), 210 bytes | 210.00 KiB/s, done.
Writing objects: 100% (3/3), 200 bytes | 200.00 KiB/s, done.
To https://github.com/username/my-project.git
   5a2c1d3..e7f8g9h  main -> main
```

Git automatically pushes to the tracked remote branch.

### Pushing a Feature Branch

To share a feature branch with others, specify both the remote and branch name:

```bash
git push origin feature-login
```

```text
Enumerating objects: 7, done.
Counting objects: 100% (7/7), done.
Writing objects: 100% (4/4), 350 bytes | 350.00 KiB/s, done.
To https://github.com/username/my-project.git
 * [new branch]      feature-login -> feature-login
```

### Deleting a Remote Branch

To remove a branch from the remote (after it's been merged, for example), use `--delete`:

```bash
git push origin --delete feature-login
```

```text
To https://github.com/username/my-project.git
 - [deleted]         feature-login
```

**Important**: This only deletes the remote branch. Your local branch still exists. If you want to clean up locally too:

```bash
# Delete the local branch (only if merged)
git branch -d feature-login
```

## Fetching with `git fetch`

Fetching downloads commits from the remote but **does not merge them** into your local branches. Your code stays exactly as it is — fetch is a safe, non-destructive operation.

```bash
git fetch origin
```

```text
remote: Enumerating objects: 6, done.
remote: Counting objects: 100% (6/6), done.
remote: Compressing objects: 100% (3/3), done.
Receiving objects: 100% (4/4), 320 bytes | 320.00 KiB/s, done.
Resolving deltas: 100% (2/2), done.
From https://github.com/username/my-project
   5a2c1d3..e7f8g9h  main       -> origin/main
   8b9c0d1..a1b2c3d  develop    -> origin/develop
```

### What Just Happened?

After fetching:
- `origin/main` now points to the same commit as the remote's `main`
- Your local `main` is unchanged — it still points to your local commit
- The remote's commits are now in your local repository, but not yet integrated

### Viewing What's Different After a Fetch

To see what commits you're missing, compare your branch to the remote:

```bash
git log origin/main..main
```

```text
commit e7f8g9h (HEAD -> main)
Author: Jane Developer <jane@example.com>
Date:   Thu Jun 13 10:30:00 2024

    Add user authentication

commit a1b2c3d
Author: Jane Developer <jane@example.com>
Date:   Thu Jun 13 09:15:00 2024

    Set up project structure
```

This shows commits on `main` that aren't on `origin/main` — in other words, commits you've made locally but haven't pushed yet.

To see what the remote has that you don't:

```bash
git log main..origin/main
```

```text
commit 9x0y1z2
Author: Bob Contributor <bob@example.com>
Date:   Thu Jun 13 11:00:00 2024

    Fix navigation bug
```

### Why Fetch Instead of Pull?

Fetch is "peek without touching." Use it when you want to:
- See what others have done before merging
- Review remote changes without affecting your working directory
- Prepare for a rebase (which you'll learn about later)

Think of fetch as updating your "map" of the remote without changing your "position."

## Pulling with `git pull`

Pulling is fetch + merge in one command. It downloads remote commits and immediately integrates them into your current branch:

```bash
git pull
```

```text
remote: Enumerating objects: 4, done.
remote: Counting objects: 100% (4/4), done.
remote: Compressing objects: 100% (3/3), done.
Receiving objects: 100% (4/4), 280 bytes | 280.00 KiB/s, done.
Resolving deltas: 100% (2/2), done.
From https://github.com/username/my-project
   5a2c1d3..e7f8g9h  main     -> origin/main
Updating 5a2c1d3..e7f8g9h
Fast-forward
 index.html | 2 ++
 1 file changed, 2 insertions(+)
```

### Fast-Forward vs. Merge Commits

If the remote has commits that are directly "ahead" of your local branch (no divergent history), Git does a **fast-forward** — it just moves your branch pointer forward. No merge commit is created.

If you've made local commits that conflict with the remote, Git creates a **merge commit** to tie the histories together:

```text
Merge branch 'main' of https://github.com/username/my-project

# Please enter a commit message to explain why this merge is necessary.
# Lines starting with '#' will be ignored, and an empty message
# aborts the commit.
```

You'll learn more about merge conflicts in the [Merging](./06-merging.md) section.

## Pull with Rebase: `git pull --rebase`

There's a second way to integrate remote changes: rebasing instead of merging.

```bash
git pull --rebase
```

This fetches the remote commits and **replays your local commits on top of them**. Instead of a merge commit, your commit history stays linear:

```text
Before pull --rebase:
            
main:     A -- B -- C
              \
feature:        D -- E

After git pull --rebase:
            
main:     A -- B -- C
                      \
feature:               D' -- E'
```

The `--rebase` flag is often preferred for keeping history clean, but it rewrites commit hashes (which is fine for local branches, dangerous for shared branches without coordination).

Rebasing is covered in depth in the **Advanced Git** section, where you'll learn when to rebase and when to merge.

## Tracking Branches

A **tracking branch** (or upstream branch) is a local branch connected to a remote branch. When you push with `-u`, you create this link.

### Why Tracking Matters

Tracking enables convenient shortcuts:
- `git push` knows where to push
- `git pull` knows where to pull from
- `git status` shows how many commits ahead/behind you are
- `git branch -vv` shows the relationship

### Viewing Tracking Info with `git branch -vv`

The double-verbose flag shows upstream relationships:

```bash
git branch -vv
```

```text
* main             a1b2c3d [origin/main] Add user authentication
  feature-login    d4e5f6g [origin/feature-login] Add login form
  feature-settings 7h8i9j0 (no upstream) Configure user preferences
```

- `main` and `feature-login` have upstream branches — they're ready to push/pull
- `feature-settings` has no upstream — it's a local-only branch

### Setting Upstream After the Fact

If you forgot `-u` on your first push, set it later:

```bash
# Set feature-dashboard to track origin/feature-dashboard
git branch -u origin/feature-dashboard feature-dashboard

# Or if you're already on that branch:
git branch -u origin/feature-dashboard
```

```text
Branch 'feature-dashboard' set up to track remote branch 'feature-dashboard' from 'origin'.
```

### Breaking the Tracking Link

To disconnect a local branch from its upstream:

```bash
git branch --unset-upstream feature-dashboard
```

```text
Branch 'feature-dashboard' had its upstream branch removed.
```

## The Fetch/Pull Workflow in Practice

Here's the typical collaboration loop:

```bash
# 1. Start your workday by fetching the latest changes
git fetch origin

# 2. See what's new on main
git log origin/main --oneline

# 3. If everything looks good, pull to merge
git pull origin main

# 4. Or if you prefer to review first, stay on your branch and pull later
# (do your work...)
git push origin feature-login
```

The key insight: **fetch is safe, pull is convenient**. Use fetch when you want to inspect before integrating. Use pull when you're ready to merge.

## Exercise

In this exercise, you'll simulate a two-developer workflow using local "bare" repositories as remotes. This pattern is how you'd actually collaborate without internet access.

### Scenario

You and a colleague are building a website. You've set up a shared "remote" as a bare repository. Your colleague has already pushed some changes. You need to fetch their work, make your own changes, and push everything to the shared remote.

### Tasks

1. Create a directory structure with three folders:
   - `shared-remote/` — a bare repository acting as your remote server
   - `your-repo/` — your local work
   - `colleague-repo/` — your colleague's work (simulated)

2. Initialize `shared-remote` as a bare repository.

3. Clone `shared-remote` into `your-repo` and `colleague-repo`.

4. In `colleague-repo`:
   - Create a file `about.html` with content
   - Commit and push to the shared remote

5. In `your-repo`:
   - Fetch the changes from the shared remote
   - Verify what your colleague pushed using `git log`
   - Pull the changes
   - Create `index.html` with content
   - Commit and push

6. In `colleague-repo`:
   - Pull your changes

7. Verify both repos have identical commit histories.

### Success Criteria

- `your-repo` has commits from both you and your colleague
- `colleague-repo` can pull your new `index.html`
- `git remote -v` shows correct URLs in both repos
- `git branch -vv` shows tracking relationships

---

## Solution

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
Writing objects: 100% (3/3), 100 bytes | 100.00 KiB/s, done.
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
remote: Compressing objects: 100% (2/2), done.
Receiving objects: 100% (2/2), 70 bytes | 70.00 KiB/s, done.
Resolving deltas: 100% (2/2), done.
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
remote: Compressing objects: 100% (2/2), done.
From /home/user/git-remotes-exercise/shared-remote
   1a2b3c4..2b3c4d5  main     -> origin/main
Updating 1a2b3c4..2b3c4d5
Fast-forward
 index.html | 9 +++++++++++++++++
 1 file changed, 9 insertions(+)
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

Both repos now have identical commit histories! The exercise demonstrated:

- **Clone** sets up the remote connection automatically
- **Fetch** downloads without merging (you saw `origin/main` update)
- **Pull** fetches and merges in one step
- **Push -u** uploads and sets tracking for future convenience

---

## Key Takeaways

| Command | What It Does |
|---------|--------------|
| `git remote -v` | List configured remotes |
| `git remote add <name> <url>` | Add a new remote |
| `git remote rename <old> <new>` | Rename a remote |
| `git remote remove <name>` | Remove a remote |
| `git push -u origin <branch>` | Push and set upstream tracking |
| `git push` | Push to tracked remote branch |
| `git push origin --delete <branch>` | Delete remote branch |
| `git fetch <remote>` | Download commits without merging |
| `git pull` | Fetch and merge in one step |
| `git pull --rebase` | Fetch and rebase instead of merge |
| `git branch -vv` | Show tracking relationships |

**Remember**: fetch is safe (read-only), pull is convenient (read + write). When in doubt, fetch first to see what you're about to integrate.

---

[← Previous: Merging](./06-merging.md) | [Next: GitHub Repos and Forks →](./08-github-repos-and-forks.md) | [← Back to Index](./00-index.md)