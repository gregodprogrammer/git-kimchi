# Branching Strategies

[← Previous: Code Review](./10-code-review.md) | [← Back to Index](./00-index.md)

In DevOps, how you manage branches is not a cosmetic decision — it directly determines how fast your team can ship, how safely you can hotfix production issues, and how cleanly your CI/CD pipeline integrates with your workflow. A poor branching strategy creates merge hell, missed releases, and CI pipelines that break unexpectedly. This section teaches you to reason about branching as an architectural choice, not just a convention.

---

## Why Branching Strategies Matter in DevOps

A branching strategy defines **when** you create branches, **what** you name them, **where** they get merged, and **who** is responsible for the merge. The right strategy aligns with your team's release cadence and tooling.

### Key DevOps Concerns

| Concern | What a Branching Strategy Must Support |
|---|---|
| **Release cadence** | Can you ship weekly? Daily? Multiple times per day? |
| **Hotfix handling** | How fast can you fix production without destabilizing in-progress work? |
| **Parallel development** | Can multiple teams work on the same codebase without blocking each other? |
| **CI/CD pipeline triggers** | Does your strategy map cleanly to automated build/test/deploy pipelines? |
| **Auditability** | Can you trace every production change back to a branch and a review? |

Teams that deploy multiple times per day typically use **trunk-based development**. Teams that maintain multiple long-running release trains (e.g., enterprise software with quarterly releases) typically use **GitFlow** or a variant.

---

## Feature Branching

Feature branching is the simplest model: every piece of work gets its own branch, cut from `main`, merged back when done.

### How It Works

```
main:    ──────●───────────────────────────────●
             │                                   │
             └─── feature/login ─────────────────┘
                               (merge back when done)
```

1. Cut a branch from `main`
2. Write code, commit freely
3. Open a pull request
4. After review, merge into `main`

### Commands

```bash
# Create and switch to a new feature branch
git checkout -b feature/user-dashboard main

# Work on the feature, commit as needed
git add README.md  # replace with your actual file names
git commit -m "Add user dashboard skeleton"

# Push and create a pull request
git push -u origin feature/user-dashboard
```

### When to Use

| Pros | Cons |
|---|---|
| Simple to understand | Breaks down with many parallel features |
| Each feature is self-contained | Long-lived feature branches drift from `main` |
| Clear audit trail per feature | Hard to coordinate releases |
| Good for small teams (< 5 people) | No formal place for in-progress work between feature completion and release |

---

## GitFlow

GitFlow is a **branching model** (not a technical requirement) created by Vincent Driessen. It defines five branch types and a strict lifecycle for each. It is well-suited for projects with scheduled releases and separate release-engineering responsibilities.

### The Five Branch Types

| Branch | Purpose | Lifetime | Cuts From | Merges To |
|---|---|---|---|---|
| `main` | Production-ready code only | Forever | — | — |
| `develop` | Integration branch for next release | Forever | `main` | `main` (via release) |
| `feature/*` | Individual feature work | Temporary | `develop` | `develop` |
| `release/*` | Release preparation (bug fixes, version bumps) | Temporary | `develop` | `main` and `develop` |
| `hotfix/*` | Urgent production fixes | Temporary | `main` | `main` and `develop` |

### The GitFlow Flow (Visual)

```
main:    ●────────────────────────────────────────●──────────────────●
              ↑                                    ↑                  ↑
         (initial)                           merge release        merge hotfix
                                                  ↓                      ↓
                                              [main + tag]          [main + tag]
                                                  ↑                      ↑
develop:    ●────────●────────●────────●────────●───●───●─────────────●
               ↑       ↑       ↑       ↑       ↑   ↑   ↑               ↑
          feature/a feature/b feature/c  release/1.0  hotfix/  develop keeps
                                                         1.0.1   advancing
```

### Detailed Flow by Branch Type

#### Feature Branches

Features branch off `develop` and merge back into `develop`. They never touch `main`.

```bash
# Start a feature branch
git checkout -b feature/login develop

# ... work, commit, push ...
git push -u origin feature/login

# After PR review, merge back into develop with no fast-forward
git checkout develop
git merge --no-ff feature/login

# Delete the feature branch
git branch -d feature/login
git push origin --delete feature/login
```

**What `--no-ff` does here:** It creates a merge commit even when a fast-forward merge is possible, preserving the fact that all commits on this branch belong to one feature. Your history becomes a tree with visible feature groupings:

```
*   Merge branch 'feature/login'
|\
| * Add login form component
| * Add login validation
| * Add login tests
```

Without `--no-ff`, all those commits would be scattered linearly across `develop` with no indication they belong together.

#### Release Branches

When `develop` has enough features for a release, cut a `release/*` branch from `develop`. Only bug fixes and release-related metadata changes (version numbers, CHANGELOG) go on this branch. No new features.

```bash
# Create the release branch
git checkout -b release/1.0.0 develop

# Bump version — edit files, commit
git add version.txt
git commit -m "Bump version to 1.0.0"

# Finish the release: merge into main, tag, merge back into develop, delete branch
git checkout main
git merge --no-ff release/1.0.0
git tag -a v1.0.0 -m "Release version 1.0.0"

git checkout develop
git merge --no-ff release/1.0.0

git branch -d release/1.0.0
```

#### Hotfix Branches

Hotfixes branch from `main` (production is broken, `develop` may be unstable), get fixed, and merge back into both `main` and `develop` so the fix is not lost when the next release cut happens.

```bash
# Create hotfix branch from main
git checkout -b hotfix/critical main

# ... fix the bug, commit ...
git commit -m "Fix critical auth bypass"

# Merge into main and tag
git checkout main
git merge --no-ff hotfix/critical
git tag -a v1.0.1 -m "Hotfix: critical auth bypass"

# Merge into develop so the fix is included in the next release
git checkout develop
git merge --no-ff hotfix/critical

git branch -d hotfix/critical
```

### GitFlow: Pros and Cons

| Pros | Cons |
|---|---|
| Clear separation between development and production | High ceremony: many branches, many merges |
| Formal hotfix path protects production | CI/CD pipelines must track multiple integration points |
| Excellent audit trail with `--no-ff` | Too heavyweight for teams deploying multiple times per day |
| Scales to many parallel features and teams | Release branches can drift from `develop` if not managed |

---

## Trunk-Based Development

Trunk-based development (TBD) is the practice where developers commit directly to `main` (the "trunk") or to very short-lived feature branches (typically < 1 day, often < 2 hours). The goal is to keep the codebase in a continuously integrateable state.

### The Core Principles

1. **Everyone commits to `main` frequently** — at least once per day.
2. **Short-lived branches** — if you use branches at all, they live for minutes or hours, not days or weeks.
3. **Feature flags** — unfinished or experimental features are merged behind a toggle, not behind a branch.
4. **Continuous integration** — every commit to `main` triggers the full pipeline. If the pipeline is red, you fix it immediately.

### Visual Flow

```
main (trunk): ──●───●───●───●───●───●───●───●───●───●───●───●───●───●───●───●───●
               ↑   ↑   ↑                           ↑   ↑
            [short-lived feature branches, merged within hours]

# Feature flags gate incomplete work:
# if (features.isEnabled("new-checkout")) { ... }
```

### Commands

```bash
# Keep main up to date before starting work
git checkout main
git pull origin main

# For larger work, create a very short-lived branch
git checkout -b feature/checkout main

# ... small, focused commit ...
git commit -m "Add checkout form"

# Immediately merge — do not let the branch live more than a few hours
git checkout main
git pull origin main
git merge --no-ff feature/checkout

git branch -d feature/checkout
git push origin main
```

### Feature Flags in Practice

With feature flags, you merge incomplete code into `main` behind a toggle:

```bash
git checkout main
git pull origin main

# Add new feature behind a flag
cat >> config/features.py << 'EOF'
NEW_CHECKOUT = os.getenv("NEW_CHECKOUT", "false") == "true"
EOF

git add config/features.py
git commit -m "Add feature flag for new checkout flow"

git push origin main
```

In your application code:

```python
if features.NEW_CHECKOUT:
    return render_new_checkout()
else:
    return render_legacy_checkout()
```

This means **every commit is production-ready** even if the feature behind the flag is not finished.

### Trunk-Based Development: Pros and Cons

| Pros | Cons |
|---|---|
| Minimal merge complexity — branches are tiny | Requires a strong CI/CD culture and fast pipelines |
| Maximum velocity for high-release-frequency teams | Engineers must be comfortable committing incomplete-but-flagged work |
| Early integration catches conflicts and regressions | Feature flags add code complexity and testing overhead |
| Simple mental model — `main` is always the truth | Not suitable when you cannot merge unfinished work safely (e.g., compiled libraries with semantic versioning) |

---

## Strategy Comparison

| Criteria | Feature Branching | GitFlow | Trunk-Based Development |
|---|---|---|---|
| **Complexity** | Low | High | Medium (low branch complexity, high CI complexity) |
| **Best release frequency** | Weekly or less | Scheduled (monthly, quarterly) | Multiple times per day |
| **Team size fit** | 1–8 | 5–50+ | 5–500+ |
| **Hotfix speed** | Medium | Fast (dedicated hotfix branch) | Fast (direct to main) |
| **Merge conflict risk** | High on long-lived branches | Medium | Very low (short branches) |
| **CI/CD fit** | Basic | Requires multi-branch pipeline logic | Continuous pipeline triggers |
| **Auditability** | Good per-feature | Excellent with `--no-ff` | Good (linear history, but no branch context) |

---

## When to Use Which

Use this as a decision guide, not a rigid rule:

| Situation | Recommended Strategy |
|---|---|
| **Startup, daily deploys, small team** | Trunk-based development |
| **Open-source project with many contributors** | Feature branching with protected `main` |
| **Enterprise software, quarterly releases** | GitFlow |
| **Product with multiple release trains** | GitFlow with multiple `develop` tracks |
| **Team new to version control** | Feature branching → migrate to GitFlow → trunk-based as maturity grows |
| **Monolithic release with scheduled freeze** | GitFlow release branches |

Many teams **combine** strategies: they use trunk-based `main` for daily work but create formal `release/*` branches when preparing a version for certification or distribution.

---

## Exercise

In this exercise you will simulate a complete GitFlow lifecycle from scratch.

### Setup

Create a new working directory for this exercise:

```bash
mkdir ~/gitflow-practice && cd ~/gitflow-practice
git init
git config user.email "student@example.com"
git config user.name "Student"
```

### Tasks

Perform the following steps in order:

1. Create the initial commit on `main`
2. Create a `develop` branch off `main`
3. Create a `feature/dashboard` branch off `develop` and make a commit
4. Merge the feature into `develop` using `--no-ff`
5. Create a `release/1.0.0` branch off `develop`
6. Finish the release: merge into `main` with a tag `v1.0.0`, merge back into `develop`
7. Create a `hotfix/security-patch` branch off `main`, make a commit, and merge back into both `main` and `develop` with a tag `v1.0.1`
8. Run `git log --oneline --graph --all` to display the final history

Show all commands and the final `git log` output.

---

## Solution

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

## Key Takeaways

- **GitFlow** gives you rigid structure at the cost of ceremony. Use it when you have scheduled releases, formal QA gates, or multiple simultaneous release trains.
- **Trunk-based development** keeps you moving fast but demands strong CI/CD, fast pipelines, and discipline around feature flags.
- **Feature branching** is the right starting point for new teams — it is simple and teaches the fundamentals of branch isolation.
- **Always use `--no-ff`** when merging into `main` or `develop` from a feature or release branch. It preserves the semantic grouping of commits that belong together.
- **Hotfixes** need to touch both `main` and `develop` — never forget to merge back into `develop` or your hotfix will be lost at the next release.

---

[Next: GitHub Pages →](./12-github-pages.md)