# Step 2 Audit: 06-merging.md

## Created
- File: `/workspaces/git-kimchi/06-merging.md`
- Size: 12,149 bytes

## Verification
```
test -f /workspaces/git-kimchi/06-merging.md && grep -q 'git merge' /workspaces/git-kimchi/06-merging.md && grep -q 'Exercise' /workspaces/git-kimchi/06-merging.md
```
Result: PASS

## Contents
- What is a merge (combining divergent histories)
- git merge command syntax (target vs source branch direction)
- Fast-forward merge (linear history, no merge commit, expected output shown)
- Three-way merge (diverged branches, merge commit with two parents, expected output shown)
- git merge --no-ff (forcing merge commits for historical traceability)
- Merge conflicts: why they happen, conflict markers (<<<<<<<, =======, >>>>>>>), git status "both modified", manual resolution (edit, add, commit), git merge --abort
- git log --graph (ASCII topology diagram showing branch/merge structure)
- Exercise + Solution: create two branches from main, conflicting edits to same file, fast-forward one merge, conflict on second merge, resolve manually keeping both changes, verify with cat and --graph

## Formatting
- Top heading: # Merging
- ## for major sections, ### for subsections
- ```bash for commands, ```text for expected terminal output
- Navigation links: prev (05-branching.md), next (07-remotes.md), index (00-index.md)
- Exercise section with corresponding Solution section