# Guidance for humans and coding assistants (CS 410/510)

The **single source of truth** for course rules in this repo is **[docs/COURSE_POLICY.md](docs/COURSE_POLICY.md)** (honor code, AI use, **Sources Used**, PEP 8, what is graded). The **syllabus and instructor** override any repo text.

Everyone—whether you use AI or not, and whichever editor you use—should follow that policy when contributing.

## Same policy, different tools

These workflows are equivalent from a course-policy perspective: you still author your own graded work, document **Sources Used** when you use AI for refinement or debugging, and do not submit directly AI-generated notebook content as your own.

| How you work | Practical note |
|--------------|----------------|
| **No AI** | Follow `docs/COURSE_POLICY.md` like any other project guidelines. |
| **Browser chat** (ChatGPT, Gemini, etc.) | Same rules; name the tool in **Sources Used** on submissions. |
| **IDE assistants** (GitHub Copilot, JetBrains AI, etc.) | Same rules; name the tool(s) in **Sources Used** when applicable. |
| **Cursor** (Chat, Composer, Agent) | Same rules. Optional extra nudges for the agent live in [`.cursor/rules/cs510-course-policy.mdc`](.cursor/rules/cs510-course-policy.mdc)—they **repeat** the policy doc, not replace it. |

If your tool does not read `AGENTS.md`, point collaborators at **`docs/COURSE_POLICY.md`** directly.

## Cursor-only

[`.cursor/rules/cs510-course-policy.mdc`](.cursor/rules/cs510-course-policy.mdc) applies when using **Cursor** so the built-in agent sees the same expectations. Developers who do not use Cursor are **not** missing a separate rulebook; they rely on `docs/COURSE_POLICY.md`.
