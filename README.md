# Guided Reading — an agent skill for actually finishing documents

A skill for AI agents (Claude Code, claude.ai, OpenCode, Cursor, Codex, Copilot, and any other host that supports the [Agent Skills spec](https://agentskills.io)) that turns any document into an interactive, guided reading session.

Long documents — especially AI-generated ones — are easy to skim and hard to absorb. Instead of handing you a summary, this skill has the agent read the document *with* you: in purpose-driven chunks, with one Socratic question at a time, so you do the thinking and leave actually knowing what the document said.

## What it does

1. **Orients first** — asks what you want *out of* the document, then triages: sections that serve your purpose get covered carefully, the rest gets fast-forwarded.
2. **Reads in chunks** — one idea-cluster at a time, each followed by a single engagement move: predict what comes next, explain an idea back in your own words, connect it to your own work, or challenge the argument.
3. **Flags when your case diverges** — if your situation matches an exception or edge case in the document rather than its headline finding, the skill says so explicitly.
4. **Closes the loop** — *you* summarize the document at the end; the agent fills the real gaps.

### Three passes

- **Pass 1 (default):** compressed, purpose-triaged first read — the gist plus what matters to you.
- **Pass 2 (on request):** full walkthrough with smaller chunks, deeper questioning, and a structured recap of findings, metrics, and caveats.
- **Pass 3 (optional):** you read the source yourself and write a summary; the agent validates it against the document.

## Install

With the GitHub CLI (v2.90.0+):

```sh
# For Claude Code, available in all projects
gh skill install jikkujoyce/agent-skills guided-reading --agent claude-code --scope user

# For OpenCode
gh skill install jikkujoyce/agent-skills guided-reading --agent opencode --scope user

# Pin to a release for reproducibility
gh skill install jikkujoyce/agent-skills guided-reading@v1.0.0 --agent claude-code --scope user
```

Or with the skills CLI:

```sh
npx skills add jikkujoyce/agent-skills/guided-reading
```

For claude.ai, download this repo, zip the `skills/guided-reading` folder, and upload it under Settings → Capabilities → Skills.

## Use

Share a document, file, or link and ask to read it:

```
guided reading: <URL/File>
```

```
Here's a report I've never managed to finish. Walk me through it.
```

The skill also triggers on phrases like "help me understand this doc", "read this with me", or mentions of trouble focusing on a document. To go deeper after a first pass, say "let's do a second pass."

## Why

Built on reading-comprehension techniques with strong evidence behind them — purpose-setting, chunking, prediction, self-explanation, elaborative interrogation, and retrieval practice — and shaped by live testing on real papers. The core principle: comprehension comes from the reader's effort, not the summary's eloquence.

## License

[MIT](./LICENSE)
