# How to: Worktrees

Git worktrees let you work on multiple tasks in parallel — each in its own directory with its own branch, its own Claude session, and its own session file. Instead of building features one at a time, you decompose work into tasks and run them simultaneously.

## The pattern

1. Break work into discrete tasks
2. Create a worktree for each task (its own branch + directory)
3. Each worktree gets its own Claude Code session
4. Each session maintains its own session file: `SESSION-YYYY-MM-DD-task-description.md`
5. When done, merge branches back to main

## Why this works with cc-ide-workspace

Session files are named per-task, not per-day: `SESSION-YYYY-MM-DD-task-description.md`. This means parallel worktrees don't collide — each task has its own session log, its own context, its own decisions.

The `.sessions/` and `.local/` directories are per-worktree (they live in the working directory), so each worktree has isolated operational context.

## Branch naming convention

```
feature/NNN-task-name
```

Examples:
- `feature/001-authentication`
- `feature/002-dashboard`
- `feature/003-data-export`

Numbered prefixes make ordering and dependencies visible.

## How to create a worktree

Ask Claude:

> "Create a worktree for the authentication feature"

Claude will:
1. Create the branch: `feature/001-authentication`
2. Set up the worktree: `git worktree add ../my-project-001-authentication feature/001-authentication`
3. Create a session file in the worktree's `.sessions/`

Or manually:

```bash
git worktree add ../my-project-001-authentication feature/001-authentication
cd ../my-project-001-authentication
```

Then open the worktree directory in your IDE as a separate workspace.

## The developer's role shifts

With worktrees, your role changes from writing code to:

- **Decomposing** — breaking the roadmap into task specs
- **Reviewing** — checking Claude's work in each worktree
- **Merging** — coordinating branches back to main
- **Coordinating** — resolving dependencies between tasks

## Cleanup

When a worktree's branch is merged:

```bash
git worktree remove ../my-project-001-authentication
git branch -d feature/001-authentication
```

Or ask Claude: *"Clean up merged worktrees"*

## Further reading

- [Git worktree documentation](https://git-scm.com/docs/git-worktree)
- See `pattern-scripts-from-prompting.md` for automating worktree management
