# guided-reading — usage notes

Human notes for running this skill. What the skill actually does lives in [`SKILL.md`](SKILL.md).

No setup: no config file, no API key, nothing to run. Point it at a document and it works.

## Usage

Share a document, a file, or a link, and ask to read it:

```
guided reading: https://arxiv.org/abs/2402.xxxxx
Here's a report I've never managed to finish. Walk me through it.
Read this with me — I keep skimming it and retaining nothing.
```

It also picks up on "help me understand this doc", "walk me through this", and mentions of trouble focusing. Right after an agent hands you a long document, "guided reading" on its own is enough.

A session looks roughly like this:

```
You:    guided reading: <link to a 30-page report>

Agent:  Before we start — what do you want out of this? A decision, the
        gist, or deep understanding you can act on?

You:    Deciding whether to adopt their approach on my team.

Agent:  Then we'll spend time on the methodology and the failure cases and
        move fast through the background. It's five sections; I'd guess six
        chunks. Section 1 sets up the problem: teams reviewing generated
        code spend more time than they save. Before I go on — what do you
        expect their proposed fix to be?

You:    Probably better tooling for review.

Agent:  Close, but they go the other way: they change what gets submitted,
        not how it's reviewed. [...continues chunk by chunk...]
```

Mid-session steering that works well: "smaller chunks", "fewer questions", "just finish walking through it and stop only where it matters", "stay on this section" — and at the end, "let's do a second pass" for full coverage, or a third pass where you read the source yourself and the agent checks your summary against it.

## Known limitations

- **It's a conversation, not a job.** The skill needs your replies to work. Running it in a non-interactive or autonomous context produces a summary with rhetorical questions in it, which is exactly what it exists to avoid.
- **Link fetching depends on the host.** The agent needs a web-fetch tool or shell access with `curl`. Paywalled pages, login-gated docs, and some PDFs will fail; paste the text instead.
- **PDFs are second-class.** Prefer an HTML version when one exists (arXiv's HTML rendering, for instance). Extracted PDF text loses table and figure structure, so chunking around data-heavy sections gets rough.
- **Long documents cost context.** A book-length document won't fit; the skill triages against your stated purpose and fast-forwards the rest, so coverage is deliberately incomplete on a first pass. Ask for a second pass, or split the document, if you need all of it.
- **The deliverable is the session.** You won't get notes, flashcards, or a study guide unless you ask for them separately afterward.
