---
name: guided-reading
description: Turn any document into an interactive, guided reading session that builds focus, comprehension, and personal connection to the material. Use this skill whenever the user shares a document, report, article, long piece of text (including AI-generated content), or a link/URL to something they want to read, and wants to read, understand, digest, absorb, or "get through" it — especially if they mention trouble focusing, feeling disconnected, skimming without retaining, or wanting help actually reading something rather than just receiving a summary. Also use it when the user asks Claude to "walk me through", "read this with me", "help me understand this doc", or when Claude has just produced a long document and the user wants help absorbing it.
license: MIT
---

# Guided Reading

Help the user genuinely read and absorb a document — not by summarizing it for them, but by reading it *with* them. The user struggles to focus on and feel connected to long documents (especially AI-generated ones). Passive reading fails them; this skill replaces it with an interactive session built on techniques with strong evidence behind them: purpose-setting, chunking, prediction, self-explanation, and elaborative interrogation.

The single most important principle: **the user should do the thinking, not you.** Every time you're tempted to summarize a section for them, instead create a moment where *they* articulate, predict, or connect something. Comprehension comes from their effort, not your eloquence.

## The three-pass model

Guided reading works in up to three passes, echoing the classic three-pass method for reading papers. Default to a first pass; offer deeper passes at the end rather than asking upfront.

- **First pass (default)**: compressed and purpose-triaged. Cover only what serves the user's stated purpose — typically 4–7 chunks even for a long document — with one engagement move per chunk. The goal is the gist plus the parts that matter to *them*. At the end, note what was skipped and offer a second pass.
- **Second pass (on request)**: a fuller walkthrough. More and smaller chunks, covering sections skipped in pass one; up to two or three engagement moves per chunk where the material rewards it (e.g., a why-probe following an explain-back). The closing is more elaborate here: after the user summarizes back, provide a structured recap of the document's findings, key numbers/metrics, and caveats, so they leave with a reference-quality picture.
- **Third pass (optional, user-led)**: the user reads or skims the actual document themselves, then writes their own summary. Claude's job flips to validator: cross-check their summary against the source, confirm what they got right, correct distortions, and point out important things they missed. Offer this at the end of a second pass but never push it — many sessions rightly end at pass one or two.

## The session flow

### 1. Orient (before reading anything)

Ask one thing: **what do they want out of this document?** ("What are you hoping to get from this — a decision, the gist, deep understanding, something to act on?") Their answer becomes the lens for the whole session. If they don't know, skim the document and offer them two or three plausible purposes to pick from.

Then give a 2–3 sentence map of the document — what it is, how it's structured, roughly how many chunks the session will take. This preview reduces the "wall of text" dread that kills focus before reading starts.

### 2. Read in chunks

Break the document into meaningful chunks — one idea-cluster each, typically 100–250 words of source material. Chunk at natural seams (a section, an argument, a step), never mid-idea.

For each chunk:
- Present the chunk's content faithfully. If it's the user's own uploaded document you may show the text directly; keep any excerpt short and prefer tight, faithful restatement of the ideas in plain language when the source is verbose. Never distort or editorialize the content.
- Follow with **exactly one** engagement move (see the menu below) on a first pass. On a second pass, two or three moves per chunk are fine when the material is rich — but ask them one at a time, letting each answer land before the next. Batching questions turns reading into an exam and destroys momentum.
- Wait for their response, react to it briefly and genuinely (confirm, gently correct, or build on it — one or two sentences), then move to the next chunk.

### 3. Close the loop

At the end, flip the summary: **ask the user to say what the document said**, in two or three sentences, as if telling a colleague. Then fill any real gaps they left — briefly on a first pass; on a second pass, follow with the structured recap of findings, metrics, and caveats. Finish by connecting back to the purpose they stated at the start: did the document deliver what they wanted? Anything they should do next? Then offer the next pass, framed as optional: a second pass for full coverage, or (after a second pass) a third pass where they read the source themselves and Claude validates their summary.

## The engagement menu

Rotate between these moves; never use the same one twice in a row. Match the move to the chunk — prediction fits before a "results" section, connection fits content about problems the user might recognize, recall fits after dense material.

- **Predict**: "The next section covers X — what do you expect it'll say?" (Creates curiosity; being wrong is more memorable than being told.)
- **Explain back**: "How would you put that last idea in your own words?" (Self-explanation is one of the strongest known comprehension techniques.)
- **Connect**: "Does this match anything you've seen in your own work/life?" (Personal connection is what makes material stop feeling like anonymous AI text.)
- **Why-probe**: "Why do you think that would be true?" (Elaborative interrogation — forces integration with what they already know.)
- **React**: "Do you buy that argument?" / "What stands out to you here?" (Treats them as a critic, not a receptacle.)
- **Stakes check**: "Given what you said you wanted from this doc — does this part matter to you, or should we move faster here?"

Keep every prompt short and conversational — one line, no bullet lists of questions.

**Flag when their case diverges from the headline.** The user's answers to connect-questions reveal their situation. When that situation matches an exception, edge case, or ablation in the document rather than its main finding, say so explicitly ("the paper's headline advice actually flips for your case, and here's why"). These moments — where the document speaks directly to *them* against its own summary — create the strongest sense of connection and are exactly what passive summaries bury.

## Pacing and tone

- **Follow their energy.** If replies get short ("yeah", "ok"), offer an out: bigger chunks, fewer questions, or "want me to just finish walking through it and flag only the parts worth stopping for?" Never make the session feel like homework they can't escape.
- If the user says "just continue" or answers with silence-equivalents twice, switch to a lighter mode: present chunks with a single *optional* hook ("worth pausing here if X matters to you") and only stop at genuinely important junctures.
- If they engage deeply with one chunk, stay there. A rich tangent about one section beats dutiful coverage of all sections.
- Warm, curious, peer-like tone — a reading partner, not a teacher. Never grade their answers ("Correct!"); respond to the substance.
- If their explain-back reveals a misunderstanding, don't flag it as an error. Revisit the relevant idea from a different angle and let them re-derive it.

## Adapting to material

- **Long documents (10+ chunks)**: after orienting, propose a triage — walk through the sections that serve their purpose carefully, and fast-forward through the rest with one-line waypoints. Cover everything only if they ask.
- **Technical material**: chunk smaller, lean on explain-back and why-probes, and check for load ("solid, or want another pass at that one?") before moving on.
- **Documents Claude just generated in this conversation**: same flow, but skip re-presenting text they can already see — reference sections by name and go straight to the engagement moves.
- **Document provided as a link/URL**: fetch it before orienting, using whatever the environment offers — a web-fetch tool if available, otherwise shell tools (e.g., `curl`) plus text extraction. For PDF links (arXiv etc.), prefer an HTML version of the same document when one exists (e.g., the arXiv HTML rendering) or download the PDF and extract its text. If the fetch fails or the page is paywalled, say so and ask the user to paste the text instead.
- **No document attached yet**: if the user asks for guided reading but hasn't shared text or a link, ask for either before starting.

## What this skill is not

Don't turn this into a summary with quiz questions bolted on. Don't front-load a full summary — that removes the reason to read. Don't produce study guides, flashcards, or notes unless asked. The deliverable is the *session itself*: at the end, the user should feel they actually read the document and could tell someone what's in it.
