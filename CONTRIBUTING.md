# Contributing

Thanks for your interest in improving this skill. Contributions are welcome — the bar is simply that changes must make guided reading sessions *better*, not just longer.

## Ground rules

- **Instructions only.** This skill is pure SKILL.md instructions — no scripts, no binaries, no network calls beyond fetching the document the user provides. Please keep it that way; it's what makes the skill portable and safe to install.
- **Preserve the core principle.** The user does the thinking, not the agent. Changes that shift work from the reader to the agent (e.g., front-loading summaries, batching questions into quizzes) will be declined.
- **One question at a time.** Any change to the engagement flow must keep questions sequential, never batched.

## Proposing a change

1. Open an issue describing the failure mode you observed in a real session — what the agent did, what it should have done. Session excerpts (with anything sensitive removed) are the most useful evidence.
2. For fixes, edit `skills/guided-reading/SKILL.md` and open a pull request. Keep the frontmatter `name` and `description` intact unless the change is specifically about triggering.
3. Test before submitting: run the modified skill on at least one real document in your agent of choice (Claude Code, OpenCode, etc.) and include a short note on how the session went.

## Validation

Before submitting, check the skill still passes spec validation:

```sh
gh skill publish --dry-run
```

This validates against the [Agent Skills specification](https://agentskills.io) (name format, required fields, etc.).

## Style

- Write instructions in direct, imperative prose. Explain *why* a rule exists when it isn't obvious — agents follow reasoned instructions more faithfully.
- Prefer removing words to adding them. The SKILL.md loads into the agent's context; every line costs tokens in every session.

## License

By contributing, you agree your contributions are licensed under the repository's [MIT License](./LICENSE).
