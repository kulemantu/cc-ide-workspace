# Git Conventions

- Do NOT auto-commit or auto-push. Always show proposed commit message and wait for explicit approval.
- Batch commits by concern — separate commits for config, features, docs, tests. Never lump unrelated changes into a single commit.
- Conventional commit format: `type(scope): description`
- Show proposed message with files to stage. Wait for user to approve before running git commands.
- Use `--force-with-lease` instead of `--force` for pushes.

## Commit Trailers

Each team member should configure their own sign-off. Co-author trailer for AI-assisted commits:

```
Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
```
