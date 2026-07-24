# Cross-repo search & registering your own repository

Adaptive Learner does not search only the official content. It can search
**across many content repositories at once**: the official one plus
community repos that coaches and teachers publish themselves. This page
explains how that federated search works and exactly how to get **your**
repository into it.

If you just want the checklist to register a repo, jump to
[Register your repository](#register-your-repository) or the focused
how-to in [REGISTER-A-REPO.md](REGISTER-A-REPO.md).

---

## The idea in one picture

Every content repository publishes a small catalogue of its sets
(`search-index.json`). A central **registry** (`recommended-repos.json`,
in the official repo) lists which repositories are part of the search and,
for each one, the exact commit that was validated. The app reads the
registry, fetches each listed repo's catalogue **at its pinned commit**,
and searches over the merged result.

```
recommended-repos.json (registry, official repo)
│
├─ self entry ── astrapi69/adaptive-learner-content ──► search-index.json  (branch main)
├─ entry ─────── coach-a/french-content   @ commit abc… ──► search-index.json @ abc…
└─ entry ─────── coach-b/python-content    @ commit def… ──► search-index.json @ def…
                                   │
                                   ▼
                    App merges every catalogue and
                    searches: language · level · domain · tags
                    ranked with trust_level as a weight
```

Two properties make this safe:

- **Federated, not centralized.** Each repo owns and publishes its own
  catalogue. Nothing is copied into the official repo except one registry
  line. Your content stays in your repo.
- **Pinned to a validated commit.** The registry points at a *specific
  commit*, not a moving branch. The search only ever serves a snapshot
  that passed validation: your repo can keep changing without affecting
  what learners see until you publish a new snapshot on purpose.

---

## The moving parts

| File | Where | Role |
|---|---|---|
| `search-index.json` | **every** content repo (root) | The repo's own catalogue of sets, the discovery feed the search reads. Auto-generated, never hand-edited. |
| `recommended-repos.json` | official repo (root) | The registry: which repos are in the search, each pinned to a validated commit. |
| `schema/search-index.schema.json` | official repo | The contract every `search-index.json` must satisfy at its pinned commit. |
| `schema/recommended-repos.schema.json` | official repo | The shape of the registry itself. |

### What's in a catalogue (`search-index.json`)

Generated from your manifests by `scripts/generate_search_index.py`. Per
set it records `id`, `name`, `description`, `source_language`,
`target_language`, `level`, `domain`, `lesson_count`, `card_count`,
`tags`, `visibility`, `ai_validated`, `trust_level`, `book`,
`updated_at`. Those are the fields the search can filter and rank on:
you do not write this file by hand, you regenerate it. `visibility` is
the consumer-display hint from the manifest set entry (engine schema
1.8): `"hidden"` asks the app not to surface the set to learners (used
for conformance/reference fixtures); absent or unknown values are
normalized to `"visible"` by the generator.

### What's in a registry entry (`recommended-repos.json`)

```jsonc
{
  "url": "https://github.com/your-name/your-content",
  "branch": "main",
  "commit": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0",  // pinned, validated
  "title": "Your set collection",
  "description": "One line about what's inside",
  "trust_level": 1,
  "languages": ["de-fr"],
  "validation": {
    "status": "validated",
    "validated_at": "2026-07-09T00:00:00Z",
    "index_schema_version": "1.0"
  }
}
```

The one **official** entry carries `"self": true` instead of a `commit`:
it is branch-tracked and validated by this repo's own CI on every push.
**Every other** entry must pin a `commit` and carry a `validation` block.

---

## Trust levels & ranking

Each entry has a `trust_level` that the search uses as a ranking weight:

| Level | Meaning |
|---|---|
| `3` | Official content. |
| `2` | Reviewed community content. |
| `1` | Community content (default for new external repos). |

Higher-trust sets rank above lower-trust ones when relevance is otherwise
comparable. New external repositories start at `1`; a maintainer can raise
the level after review.

---

## Register your repository

Getting in is a **pull request against `recommended-repos.json`** in the
official repo. CI validates your repo *at the commit you pin*; once it is
green, a maintainer merges it and your snapshot joins the search.

1. **Have a valid content repo.** It must publish a `search-index.json` at
   its root and pass `scripts/validate_content.py`. If you're starting
   fresh, see [GETTING-STARTED.md](GETTING-STARTED.md).

2. **Pick and copy the commit** you want listed:

   ```bash
   git -C your-content-repo rev-parse main
   ```

3. **Add your entry** to `recommended-repos.json` (fork the official repo,
   edit, using the entry shape shown above), then **open the PR**.

4. **CI checks the pinned snapshot** (workflow *Validate registered
   repos*): the commit exists and is on the declared branch, your
   `search-index.json` at that commit matches the contract, and its `repo`
   slug matches your URL.

5. **Green + merge = you're in.**

The full step-by-step, including the exact fields and local pre-checks,
lives in [REGISTER-A-REPO.md](REGISTER-A-REPO.md).

### Validate locally before you open the PR

```bash
pip install "jsonschema>=4,<5"
python scripts/validate_registry.py            # offline: registry shape + rules
python scripts/validate_registered_repo.py \
    https://github.com/your-name/your-content   # online: your pinned commit
```

---

## Updating a listed repo

Pinning is strict on purpose. When you publish new content, the search
does **not** pick it up automatically: that's the point, so learners
never get an unvalidated snapshot. To ship an update, open a **new PR**
that bumps your entry's `commit` (and `validated_at`) to the new SHA. CI
re-validates the new snapshot before it goes live.

---

## FAQ

**Do I have to move my content into the official repo?**
No. Your content stays in your repository. Only a single registry line
(URL + pinned commit) lives in the official repo.

**Why a commit and not just my branch?**
A branch moves; a commit does not. Pinning guarantees the search serves
exactly the snapshot that was validated, and that you control when an
update goes live.

**My repo is private. Can it be listed?**
The federated search fetches your `search-index.json` over the public web
(e.g. `raw.githubusercontent.com/<owner>/<repo>/<commit>/…`), so the
listed snapshot needs to be publicly readable. For private, invite-only
sharing use the app's invite-code flow instead (see the main
[README](../README.md#für-coaches-und-lehrer)).

**Who can raise my trust level?**
A maintainer of the official repo, after reviewing your content.

**Where does the search UI itself live?**
In the Adaptive Learner app
(<https://github.com/astrapi69/adaptive-learner>). This repository owns the
data contract (catalogue format, registry, validation gate); the app owns
the search experience that consumes it.

---

## See also

- [REGISTER-A-REPO.md](REGISTER-A-REPO.md): the focused registration how-to.
- [GETTING-STARTED.md](GETTING-STARTED.md): build a valid content repo from scratch.
- [`recommended-repos.json`](../recommended-repos.json): the live registry.
- [`schema/`](../schema/): the catalogue and registry schemas.
