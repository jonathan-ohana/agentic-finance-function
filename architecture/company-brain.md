# The company brain, and where the librarian went

*Written 15 Sep 2026, after the "company brain" framing entered circulation: the idea that
every company should maintain a governed memory layer — a library of what it knows, a
librarian that assembles the right context per task, skill files as employees, evals as
performance reviews. This page maps that vocabulary onto what this repository already runs,
and states the one place where this design deliberately departs from it. It is a position
informed by operating the system documented here; the departure has not been tested against
a retrieval-based alternative, and this page should be read with that in mind.*

---

## The map

Most of the brain vocabulary names machinery this repository already runs, and in most
cases the repository's version is enforced by a check rather than asserted as a practice.

| Brain vocabulary | What runs here | Where it is enforced |
|---|---|---|
| A skill file is an employee with a job description | An agent is a charter with an explicit prohibition list and an earned autonomy level | [The charters](../agents/), and the promotion and demotion rules in [the self-improvement loop](../correction-loop/self-improvement-loop.md) |
| Evals are performance reviews | The review ledger, and metrics computed on the agents rather than by them — acceptance rate, material correction rate, escalation recall | [The self-improvement loop](../correction-loop/self-improvement-loop.md); a missed material error demotes on one strike |
| Put deterministic work in deterministic space | Engines compute, agents judge; a workflow is born agentic and is compiled when its corrections converge | [The workflow lifecycle](lifecycle.md), including the test for what never compiles |
| Never do one-off work — turn it into a skill | A human correction becomes a versioned rule that a later run cites by ID; a stabilized workflow becomes code | [The correction loop](../correction-loop/loop-verification.md), [the lifecycle](lifecycle.md) |
| Memory hygiene: provenance and contradiction checks | Every figure traces to an artifact or a registry entry cited by ID and version; a checker recalculates every write-up against the artifact it describes and lists every metric quoted with more than one value | [The registry](../semantic-layer/definitions-instance.md), [the docverify register](../outputs/docverify-register.md) — regenerated and diffed in CI |
| Model quality is rented; you own your brain | The definitions, rulings, contracts and correction log are execution-substrate-agnostic and survive a platform change | [The lifecycle](lifecycle.md), "what this changes about the thesis" |

One clause in that vocabulary has no counterpart here, and the absence is a decision.

## The librarian, split in two

The brain framing pairs the library with a librarian: an agent that, at runtime, searches
the corpus and assembles the context each task needs. This repository has the library and
deliberately no librarian. Two reasons, one principled and one structural.

The principled one is this repository's standing test for what may stay probabilistic:
give the same corpus and the same task to two competent librarians, and ask whether they
would assemble the same context. For a bounded finance corpus they mostly would — which
documents bear on a January revenue variance is close to mechanical once the documents are
indexed and joined to the ledger. By [the lifecycle's](lifecycle.md) own logic, work that
two practitioners would do identically belongs in deterministic space. The librarian is
mostly not an agent. It is an engine: an indexer that builds the searchable surface, with
provenance attached, and refuses to rank relevance — because relevance is a verdict, and
no engine output contains a verdict field.

The structural one: runtime retrieval reintroduces, upstream of every agent, exactly the
property the whole governance layer exists to contain. Two runs that retrieve different
context produce different answers, and the difference is invisible in the output. A
free-retrieval librarian is also how a forecast comes to depend on a message nobody can
point to afterwards. The rule this repository holds is that a signal which changes a number
carries a pointer to its source the way a variance line carries a registry ID — an
intelligence layer that cannot cite its container is a copilot.

So the librarian's job is split. The searchable surface is precomputed by an engine, with
every entry carrying its source. The judgment slice — deciding that an unexpected document
matters — stays where judgment already lives, in the analyst's charter, and is escalated,
not silently acted on.

## The honest cut against this position

The strongest argument for the librarian comes from this repository's own instruments. In
the sealed evaluation run, every miss required a join between a document and the ledger
that the precomputed surface did not contain — and "what is not precomputed is not looked
at" is logged in [the friction log](../what-broke/friction-log.md) as a defect pattern,
not a virtue. Curation's failure mode is real and has been measured here.

The conclusion drawn is not to abandon curation but to widen it: the misses are treated as
gaps in the precomputed surface, and each missing context class enters the same way the
ledger did — through a contract, with a pointer, with named refusal conditions when a
signal cannot be grounded. Same destination as the librarian, different door.

For a corpus small enough to precompute in full — and a Seed-to-A company's corpus is —
that door is strictly better, because everything an agent can see is already cited. The
position weakens as the corpus grows. If this design ever serves a corpus where full
precompute stops being feasible, the answer this page commits to is retrieval as proposal:
a retriever may surface candidates with pointers, and nothing it finds touches a number
until it is mapped through the same contracts. Retrieval proposes; the precomputed,
contracted surface is what enacts.

## What remains open

Memory tiering — which context stays hot in an agent's working set and which is archived,
summarized, and fetched on demand — has no doctrine in this repository. The nearest thing,
the refresh manifest that declares which cells of a model are writable, governs artifacts
rather than context. It is recorded here as an open design question rather than papered
over, in the same spirit as the unresolved rulings in the registry: unresolved stays
marked unresolved.

## The limit

Nothing on this page is a result. The mapping in the table points at machinery that runs
and at checks that fail builds; the librarian ruling is a design position that has not been
tested against a retrieval-based alternative on the same corpus, and the sealed-run misses
cut against it exactly as described above. The claim is narrower than "curation beats
retrieval." It is that for a governed finance function at this scale, context should enter
through contracts that can cite it — and that the burden of proof sits with any component
that would let it enter another way.
