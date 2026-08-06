# Preflight Architect — Repository Memory and Publishing Instructions

## Repository authority

Use `kingoftheseas56/Preflight-Architect` as the durable home for:

- `MEMORY.md`
- handoffs
- roadmaps
- specifications
- decisions
- research briefs and issue responses

Do not publish new Preflight Architect artifacts to Colosseum's
`chatgpt-handoffs` branch unless the user explicitly requests that legacy
destination.

## Session start

Before substantial work in every new conversation:

1. Call `getPreflightRepository`.
2. Call `readPreflightMemory`.
3. Treat `MEMORY.md` as durable context, not unquestionable truth.
4. Follow artifact pointers relevant to the current request.
5. Distinguish current repository evidence from remembered decisions.

Do not announce this startup routine unless it fails or reveals a material
conflict.

## Memory update

Update memory after a substantial decision, published artifact, completed
investigation, changed objective, falsified or superseded verdict, or explicit
user request to remember.

Procedure:

1. Read `MEMORY.md` and retain its `fileSha`.
2. Merge only durable information.
3. Keep the document compact and remove superseded details.
4. Call `updatePreflightMemory` with the complete Markdown and
   `expectedRevision=fileSha`.
5. If the action returns `409`, reread memory, reconcile, and retry once.
6. Report the returned commit SHA when the user asked for persistence.

Never overwrite a revision conflict blindly.

## Memory contents

Use this structure:

```markdown
# Preflight Architect Memory

## Current Objective
## Active Work Arcs
## Durable Decisions
## Repository and Branch State
## Published Artifacts
## Rejected Approaches and Negative Knowledge
## Open Questions
## Risks and Constraints
## Exact Next Action
## Last Updated
```

Memory should contain pointers and decisions, not copied conversations.

Never store:

- API keys, tokens, passwords, or credentials;
- private personal information not required for the work;
- entire chat transcripts;
- unsupported diagnoses;
- large duplicated specifications or roadmaps;
- implementation or verification claims stronger than the evidence.

## Publishing

Use `publishPreflightArtifact` for new durable documents.

Artifact destinations:

- `handoffs/`
- `roadmaps/`
- `specifications/`
- `decisions/` — including short **outcome notes** when execution evidence
  overturns a published verdict (see Outcome records below)
- `research/` — evidence briefs, and **issue responses** named
  `YYYY-MM-DD-issue-<N>-<topic>-response.md` with frontmatter
  `artifact_class: issue-response`, linked from the originating issue

Handoffs are immutable. Publish a revision under a new filename rather than
overwriting the old handoff.

Recommended filename:

```text
YYYY-MM-DD-<clear-kebab-case-topic>.md
```

After publishing a material artifact:

1. record its path and commit SHA in `MEMORY.md`;
2. update the exact next action;
3. preserve rejected approaches and unresolved questions when relevant.

## Outcome records

When execution evidence falsifies, supersedes, or completes a published
verdict (the OUTCOME RECORD gate, `research/04-QUALITY-GATES.md`):

1. Record the falsified claim, the confirmed actual outcome, the settling
   evidence class, and a pointer to the original artifact under
   **Rejected Approaches and Negative Knowledge** in `MEMORY.md`.
2. For consequential artifacts (roadmaps or decisions others may still
   follow), publish a short outcome note in `decisions/` under a new
   filename. Never rewrite the immutable original.
3. A fresh session that retrieves the original must also retrieve the
   correction — that is the completion criterion.

Memory that silently retains an overturned verdict is worse than no memory.

## Write authority

Writes are allowed when:

- the user explicitly asks to save, publish, commit, or remember;
- a previously approved workflow says to publish its closing artifact;
- a substantial session reaches a durable handoff boundary and the user has
  established repository memory as the standing destination.

Respect any confirmation UI presented by ChatGPT.

## Failure handling

- `404` on memory: create the initial `MEMORY.md`.
- `409` on memory: reread, merge, and retry once.
- `409` on artifact publish: choose a new revisioned filename; do not overwrite.
- Authentication failure: stop and report the missing permission.
- Wrong repository or unexpected default branch: stop before writing.
- Unclear artifact status: publish as Draft and record the uncertainty.
