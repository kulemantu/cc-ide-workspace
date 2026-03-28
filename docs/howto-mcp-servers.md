# How to: MCP Servers

MCP (Model Context Protocol) servers extend Claude beyond the filesystem. They connect Claude to external tools — browsers, APIs, project management, documentation — so you can work across your entire stack without leaving the IDE.

## Why MCPs matter in this workspace

Without MCPs, Claude can only read/write files and run terminal commands. With MCPs, Claude can:

- Look up live documentation before writing code (Context7)
- Create PRs, manage issues, and search code on GitHub
- Automate browser tasks — fill forms, take screenshots, run tests (Playwright)
- Check your calendar before scheduling a deploy
- Post updates to Slack or create Jira tickets

MCPs work in both the IDE extension and the terminal. Whatever you configure is available everywhere Claude runs.

## Recommended servers

| Server | What it enables | Why it's first |
|--------|----------------|----------------|
| **Context7** | Live documentation lookup for any library | Bootstrap — once you have this, ask Claude to set up the rest |
| **GitHub** | PRs, issues, code search, merges | Core development workflow |
| **Playwright** | Browser automation, screenshots, testing | Visual verification, form filling, web scraping |

## Worth adding for team workflows

| Server | What it enables |
|--------|----------------|
| **Jira** | Create/update tickets, link PRs to issues, manage sprints |
| **Slack** | Post deploy notifications, share PR links, alert on failures |
| **n8n** | Export/import workflows, trigger executions, read logs |
| **Notion** | Search pages, create databases, manage project docs |
| **Gmail** | Search messages, read threads, draft emails |
| **Google Calendar** | Find free time, create meetings, check availability |

## How to set up

**Start with Context7.** Once you have it, ask Claude:

> "How do I add the GitHub MCP server?"

Claude will look up the current setup instructions and walk you through it. This applies to every MCP — once you have Context7, Claude can set up everything else itself.

For manual setup, see the [Claude Code MCP documentation](https://docs.anthropic.com/en/docs/claude-code).

MCP servers are configured in Claude Code's settings. The configuration is shareable — your team can use the same MCP setup across all their workspaces.

## In this workspace

- API credentials for MCP servers go in `.local/` (gitignored, never committed)
- MCP-generated output (screenshots, exports, reports) goes to `workspace/outputs/`
- If an MCP interaction produces reusable logic, Claude moves it to `scripts/src/`
