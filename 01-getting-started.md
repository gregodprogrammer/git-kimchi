# Getting Started with Git

[← Back to Index](./00-index.md)

Welcome! This section walks you through installing Git, setting up your identity, and creating your very first repository. By the end, you will understand how Git tracks changes and why version control makes you a more effective developer.

---

## What is Git?

Git is a **distributed version control system** — a tool that records changes to your files over time. Unlike saving a file with names like `report-v2-FINAL-actual-FINAL.docx`, Git stores a complete history of every version, letting you compare changes, revert mistakes, and collaborate with others without overwriting work.

**Why bother?** Imagine you accidentally delete a critical function at 2 AM. With Git, you can restore it in seconds. Without Git, you spend hours reconstructing it from memory. Every professional developer uses version control — this guide teaches you how.

---

## Installing Git

### Checking If Git Is Already Installed

Open your terminal and run:

```bash
git --version
```

If Git is installed, you will see output similar to:

```text
git version 2.43.0
```

If you see an error like `command not found: git`, you need to install it.

### Installing on Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install git
```

After installation, verify:

```bash
git --version
```

```text
git version 2.43.0
```

### Installing on macOS

**Option 1 — Using Homebrew (recommended):**

```bash
brew install git
```

**Option 2 — Using the Xcode Command Line Tools:**

```bash
git --version
```

If Git is not found, macOS will prompt you to install the command line tools. Follow the on-screen instructions.

### Installing on Windows

Download Git from the official website: [https://git-scm.com/download/win](https://git-scm.com/download/win)

The installer includes Git Bash, which gives you a Unix-like terminal on Windows. Use Git Bash for all examples in this guide.

### Verifying Your Installation

After installing, confirm Git responds correctly:

```bash
git --version
```

```text
git version 2.43.0
```

If you see a version number, you are ready to proceed.

---

## First-Time Configuration

Git stores configuration in three levels:

| Level | Location | When to Use |
|-------|----------|-------------|
| `--system` | System-wide (all users) | System administrators only |
| `--global` | Your user account (`~/.gitconfig`) | Your personal settings — **use this** |
| `--local` | Inside a repository (`.git/config`) | Repository-specific overrides |

For personal settings, always use `--global`.

### Setting Your Identity

Before making any commits, tell Git who you are. This identity appears on every commit you create.

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

These commands create or update `~/.gitconfig`. Use your real name (or a handle you are comfortable appearing on commits) and an email you check regularly.

**Why does this matter?** Every commit is a record of who made a change and when. Later, when you collaborate on a team, this information helps teammates understand the history of the codebase.

### Setting a Default Branch Name

When you create a new repository with `git init`, Git names the initial branch. Newer Git versions use `main` by default, but older versions may use `master`. To ensure consistency:

```bash
git config --global init.defaultBranch main
```

### Setting Your Preferred Text Editor

Git opens an editor when you write commit messages, resolve conflicts, or perform interactive rebase. Set your editor:

```bash
# VS Code (most common for beginners)
git config --global core.editor "code --wait"

# Vim (classic, pre-installed on most Linux/macOS systems)
git config --global core.editor vim

# Nano (simpler alternative)
git config --global core.editor nano
```

### Verifying Your Configuration

List all settings Git is currently using:

```bash
git config --list
```

You will see output like:

```text
user.name=Your Name
user.email=your.email@example.com
init.defaultbranch=main
core.editor=code --wait
```

To view a single setting:

```bash
git config user.name
```

```text
Your Name
```

---

## Creating a Repository with `git init`

A **repository** (or "repo") is a directory that Git watches. Inside it, Git stores all its data and history in a hidden folder called `.git`.

### Initializing a New Repository

Navigate to a folder where you want to start tracking changes and run:

```bash
mkdir my-first-repo
cd my-first-repo
git init
```

Git responds with:

```text
Initialized empty Git repository in /home/username/my-first-repo/.git/
```

**What just happened?** Git created a `.git` subdirectory. Inside it are configuration files and a database that store your project's history. Until you run `git init`, the directory is just a normal folder.

### Understanding the `.git` Directory

Your repository now looks like this:

```bash
ls -la
```

```text
total .  ..  .git
```

The `.git` folder is hidden (it starts with a dot). Do not delete or edit files inside `.git` manually — Git manages this folder automatically.

**Key insight:** Running `git init` does not make a snapshot of your files. It only tells Git to start watching this directory. You still need to stage and commit changes (covered in the next section).

### Reinitializing an Existing Repository

Running `git init` in a folder that is already a Git repository is safe — it will not overwrite or destroy your history:

```bash
git init
```

```text
Reinitialized existing Git repository in /home/username/my-first-repo/.git/
```

---

## Cloning an Existing Repository with `git clone`

So far, you created a repository from scratch. More often, you will work on a project that already exists. Cloning downloads a complete copy of a repository, including its full history.

### Cloning a Public Repository

Find a public repository on GitHub, GitLab, or any Git host. Copy its URL. Then run:

```bash
git clone https://github.com/octocat/Hello-World.git
```

Git downloads the repository:

```text
Cloning into 'Hello-World'...
remote: Enumerating objects: 10, done.
remote: Counting objects: 100% (10/10), done.
remote: Compressing objects: 100% (6/6), done.
Receiving objects: 100% (10/10), 3.66 KiB | 1.83 MiB/s, done.
Resolving deltas: 100% (4/4), done.
```

Git creates a folder named after the repository (`Hello-World`) and places the complete project inside.

### Cloning to a Custom Folder Name

Specify a folder name as the second argument:

```bash
git clone https://github.com/octocat/Hello-World.git my-project
```

### What Does Cloning Give You?

After cloning, you have:

- **The full history** — every commit ever made
- **All branches** — even if they are not visible by default
- **A working copy** — files you can edit immediately

Cloning also automatically configures a **remote** called `origin`, which points back to the original URL. You will learn about remotes in detail later.

---

## Understanding the Git Workflow

Before making your first commit, understand how Git tracks changes. Git has three main areas:

### The Three States

```text
Working Directory  →  Staging Area  →  Repository
     (your files)       (.git/index)      (.git/objects)
```

| Area | Description | Command to Move Files |
|------|-------------|----------------------|
| **Working Directory** | Your actual files on disk — where you edit, create, and delete files | — |
| **Staging Area** (Index) | A holding area listing what will go into your next snapshot | `git add` |
| **Repository** | The permanent record of your project — the committed snapshots | `git commit` |

### How It Works in Practice

1. **Edit files** in your working directory.
2. **Stage changes** with `git add filename` to prepare a snapshot.
3. **Commit** with `git commit` to permanently save the snapshot in the repository.

This two-step process (edit → stage → commit) gives you precise control over what goes into each commit. You can stage some files while leaving others out, write a clear commit message, and review before saving permanently.

### Why This Matters

Imagine you fix a bug, add a new feature, and refactor some old code all in one session. If you commit everything at once, the commit message has to say "fixes bug, adds feature, refactors code" — which is vague and hard to understand later.

With staging, you can split this into three commits:

- `"Fix null pointer in login handler"`
- `"Add password strength meter"`
- `"Extract database utilities into separate module"`

Each commit tells a clear story. Months later, when you are trying to understand a change, these atomic commits are invaluable.

---

## Your First Commit

Now that you understand the workflow, make your first commit in the repository you created earlier.

### Step 1 — Create a File

```bash
cd my-first-repo
echo "Hello, Git!" > hello.txt
```

### Step 2 — Check the Status

Git tells you which files have changed:

```bash
git status
```

```text
On branch main

No commits yet yet

Untracked files:
  (use "git add" to stage their contents)
        hello.txt

nothing added to commit yet
```

Notice `hello.txt` appears under "Untracked files" — Git sees the file but is not yet watching its contents.

### Step 3 — Stage the File

```bash
git add hello.txt
```

Running `git status` again:

```text
On branch main

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
        new file:   hello.txt
```

The file moved from "Untracked" to "Changes to be committed" — it is now in the staging area.

### Step 4 — Commit the Change

```bash
git commit -m "Add hello.txt with greeting"
```

```text
[main (root-commit) a1b2c3d] Add hello.txt with greeting
 1 file changed, 1 insertion(+)
 create mode 100644 hello.txt
```

**Congratulations — you made your first commit!**

The `-m` flag supplies the commit message inline. Good commit messages are short and descriptive: they complete the sentence "This commit will..."

---

## Exercise

### Scenario

You have been working on a project without version control. You want to start using Git to track your work.

### Tasks

1. Configure Git with your name and email address.
2. Create a new directory called `git-practice`.
3. Initialize it as a Git repository.
4. Create a file named `notes.txt` with the text `Learning Git is fun!`.
5. Stage and commit the file with a descriptive message.

---

## Solution

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

## Summary

In this section you:

- **Installed Git** and verified the installation with `git --version`
- **Configured your identity** with `git config --global user.name` and `user.email`
- **Created a new repository** with `git init`
- **Cloned an existing repository** with `git clone`
- **Understood the Git workflow**: Working Directory → Staging Area → Repository
- **Made your first commit** using `git add` and `git commit`
- **Completed a hands-on exercise** to reinforce the concepts

---

## Next Steps

Now that you understand how to initialize a repository and make commits, move on to the next section to learn about the **staging area in depth** and how to write meaningful, well-structured commits.

[Next: Staging and Commits →](./02-staging-and-commits.md)