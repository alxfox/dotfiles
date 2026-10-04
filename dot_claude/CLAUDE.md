# Personal working conventions

Author: Alexander Fuchs (alx.fuchs@tum.de). These are user-level conventions that apply to
every project. A project-level instruction file (`CLAUDE.md` or `AGENTS.md`) may add
detail or override a rule, but never relaxes the writing rules in "Documentation" or the
commit rules in "Git".

## Communication

- Ground every answer in the actual checkout. Read the file, log, or config being
  discussed before answering from general knowledge.
- Give the real cause, not only a workaround. If the root cause stays unproven, say so
  explicitly and name the exact files and tooling involved.
- Do not pad answers with alternatives I will not take. Recommend one option.

## Documentation

- Technical documentation only. No prose, no marketing voice, no narrative filler.
- NEVER use em-dashes or similar decorative punctuation. Use commas, colons, or
  parentheses.
- NO emojis. Not in docs, not in code, not in commit messages, not in terminal output.
- Match the tone and structure of the existing pages in the repo. Read one reference
  page before writing a new one.
- Admonitions: GitHub-style only (`> [!NOTE]`, `> [!TIP]`, `> [!IMPORTANT]`,
  `> [!WARNING]`, `> [!CAUTION]`). A few high-value callouts, not a wall of them.
- Use mermaid diagrams and other visual aids wherever they carry information. External
  graphics I have to produce myself are allowed as placeholders, but must be clearly
  marked as placeholders.
- Never invent behavior. If something is unclear, undecided, or unverified, state that
  visibly in the document (a NOTE admonition marking it as an open decision).
- Strict page ownership. When content overlaps two pages, move it to the page that owns
  it and cross-link. Do not duplicate procedures.
- Migrating or importing content means reorganizing and tightening it, not copying it
  verbatim.
- Landing pages get a short intro, a "Start Here" style section map, and one or two
  callouts. Not a rewrite, not an empty page.
- Structural changes must update the navigation config too (`mkdocs.yml`, `.nav.yml`,
  sidebar files, index pages).
- If docstrings feed generated API docs, the docstring is the documentation. Write it
  properly and never hand-edit the generated page.

## Code

- Match the surrounding code: naming, structure, comment density, existing idioms.
- Keep modules with a single responsibility and replaceable seams. Prefer a thin entry
  point over a monolith.
- Do not refactor code outside the scope of the task, and never code owned by someone
  else on the team.
- No defensive scaffolding I did not ask for (no speculative try/except, no unused
  config flags, no compatibility shims for cases that do not exist).
- Do not leave commented-out code or "legacy" duplicates behind.

## Verification and honesty

- Check that a tool exists before relying on it. Do not assume `mkdocs`, `uv`, `pytest`,
  ROS tooling, or any other runner is on the host.
- Never claim something works, passes, or is fixed without having run it. If
  verification is blocked (missing tooling, no GPU, container-only code), say "not
  verified" and say why.
- Distinguish clearly between "structurally correct by inspection" and "executed
  successfully".
- Re-read the current file contents before applying multi-file or multi-step patches.
  Files drift between turns.
- Report failures with the actual output. Report skipped steps as skipped.

## Git

- Never mention LLMs, AI, Claude, Codex, Copilot, or any assistant in commit messages,
  PR descriptions, code comments, or documentation.
- No `Co-Authored-By` assistant trailers. No "Generated with ..." footers.
- No emojis and no conventional-commit gitmoji decorations in commit messages.
- Commit subject: imperative mood, lower case after the type prefix if the repo uses
  prefixes, no trailing period, wrapped at roughly 72 characters.
- Commit body: what changed and why, only if it is not obvious from the subject.
- Commit on any non-default branches. Push only when I ask. Never commit on a default branch without saying so.
- One commit per repository. A change spanning several repos is several commits, never
  assume one covers the others.

## Environment and tooling

- Use the project's own entry points for setup and running: `make setup`, `make dev`,
  `uv sync`, the documented script under `scripts/`. Do not hand-roll `python -m venv`,
  `pip install`, or `npm install` when a Makefile or task runner exists.
- If a generated environment is broken, delete it and rerun the project's setup target
  instead of patching it by hand.
- Containerized stacks are container-first. If the stack is documented as running in
  Docker, do not produce host-install instructions or run its code on the host.
- Do not build heavy container images locally when the project has CI that builds them.

## Scope and open questions

- When work hits an undefined interface or an architectural hole, ASK before
  implementing against an assumption.
- If the answer is "not decided yet", record it as an explicit future decision in the
  documentation and design around it.
- Deliver the full requested scope. If part of it is blocked, finish everything else and
  state plainly what was left out and why. Do not silently narrow the task.
- Cross-cutting changes get done on both sides in the same session (source plus its
  docs, producer plus consumer), and the summary says explicitly which files in which
  repos were touched.
