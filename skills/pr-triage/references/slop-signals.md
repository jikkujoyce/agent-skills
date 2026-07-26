# Slop signal catalog

How to use this file: check the PR against each signal. **Hard signals** indicate fabrication — one instance, once *verified* (not merely suspected), justifies a Close verdict on its own. **Soft signals** each have innocent explanations — act only when two or three converge on the same PR, and even then the verdict is Request evidence, not Close. The **false positives** section lists patterns that superficially resemble slop and must never be flagged in isolation.

Every signal entry: what it looks like → how to check → why it matters.

## Hard signals (verify, then Close)

**H1. Contradicted claims.** The description asserts X; the diff does not-X or lacks X entirely. "Adds retry with exponential backoff" and no retry logic anywhere in the diff. → Check: search the diff for the claimed mechanism. → A description written without reading the final diff is the definitive mark of unverified generation.

**H2. Hallucinated references.** The change calls functions, imports modules, or uses config keys that exist neither in the codebase nor in the *pinned* version of a dependency. → Check: `grep -rn "<symbol>"` across the repo; check the lockfile/requirements for the actual dependency version before checking that library's docs. → Code that cannot have been run cannot have been tested; every claim in the PR is now suspect.

**H3. Phantom testing.** "All tests pass" with no CI run; pasted test output whose format doesn't match the project's actual runner; claimed test counts that don't match the suite. → Check: CI status on the PR; run the suite's real output format against the pasted one. → Fabricated verification is worse than no verification — it's aimed at the reviewer.

**H4. Invented problem.** The "bug" being fixed sits on an unreachable code path, describes behavior that's explicitly documented as intended, or is reported in an issue filed by the PR author minutes before the PR (check timestamps and author). → Check: trace reachability of the "buggy" path; read the linked issue's metadata, not just its text. → Issue-plus-fix pairs are cheap to generate and pad contribution graphs.

**H5. Benchmark theater.** Performance numbers ("38.7% faster") with no benchmark code in the diff, no linked script, no stated methodology or hardware. Suspiciously precise figures are the classic tell. → Check: search diff and description for any reproducible measurement path. → Unreproducible numbers exist to trigger a merge reflex, nothing else.

## Soft signals (two or three together → Request evidence)

**S1. Scale mismatch.** Four paragraphs, emoji section headers, and a fully-checked checklist for a six-line diff. → Compare description length/structure to diff size.

**S2. Boilerplate skeleton.** "This PR introduces a comprehensive...", "## Changes 🚀 / ## Testing ✅" structure identical across the author's other PRs; a repo PR template with every box checked and nothing edited. → Open one or two of the author's other PRs and compare skeletons.

**S3. Comment narration.** New comments that restate the line below them ("// increment the counter"); docstrings added to self-evident one-liners; comment rewording on logic the PR doesn't touch. → Scan added `+` comment lines against the code beneath them.

**S4. Convention blindness.** Introduces a second error-handling style where the codebase has one; reimplements an existing utility; uses different test idioms than the surrounding suite; adds a dependency for something the stdlib or an existing dep already does. → Compare the new code's patterns against two or three neighboring files.

**S5. Defensive padding.** Broad try/except that swallows errors, null checks on values that can't be null, backwards-compatibility shims nobody requested, config flags for hypothetical needs. → Read each guard and ask what real input triggers it.

**S6. Test theater (soft form).** Tests that assert the mock rather than the behavior; tautological assertions; tests that pass without the code change. → Read the assertions; if cheap, apply test hunks alone to base and run.

**S7. Drive-by churn.** Reformatting of untouched files, renames of unrelated variables, import reordering beyond the stated scope. Also a scope signal for Stage 3. → Diffstat files against the stated purpose.

**S8. Mechanical uniformity.** Every function receives a same-shaped docstring; every file gets a same-sized change; the diff reads like a sweep rather than a fix. → Skim the per-file diffstat for suspicious uniformity.

**S9. Author pattern.** Account under ~30 days old with many open PRs across unrelated repos sharing a description skeleton; no replies to review comments, or instant replies that restate the description without addressing the point. → `gh search prs --author <login>`; read one reply thread if any exist.

**S10. Weakened safety.** Deleted assertions, tests marked skip/xfail, error levels lowered, exception handlers broadened — green CI achieved by lowering the bar. → Search the diff for removed `assert`, added `skip`, log-level changes. (Verified instances of this one upgrade toward hard — deliberate safety removal to pass CI is fabrication-adjacent.)

## Known false positives — never flag alone

- **Template compliance.** A first-time contributor filling out the repo's own PR template completely is doing what CONTRIBUTING.md asked. Checked boxes only count as S2 when unedited boilerplate spans *multiple* PRs.
- **Non-native English.** Stiff or formulaic prose from a human doing their best is not a signal. Judge the diff.
- **Legitimately large diffs.** Codegen refreshes, dependency bumps with lockfiles, a `make fmt` run the maintainer asked for. The diffstat is huge and that's fine — Stage 1's generated-file handling covers it.
- **AI-assisted, human-verified.** The author used AI and says so, answers understanding questions crisply, and iterates on review feedback. This is a normal contribution. The catalog targets *unverified* work, not tool choice.

## Maintainer's additions

Append new patterns below with a dated, anonymized real example. Keep the format: what it looks like → how to check → why it matters.
