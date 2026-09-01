# 71 — Co-pilot addendum: free-form as the primary interface

*Ruled 20 Aug 2026 (Fable). Amends doc 21 — Jonathan's decision: the final version takes free-form questions. The doc-21 contract stands unchanged; free-form input is safe precisely because the OUTPUT is bounded (retrieve / re-aggregate / explain / compare; refusal converts to a governance event). Five additional requirements:*

1. **Vocabulary in the semantic layer.** Registry entries carry alias lists so free-form phrasing resolves to registered metrics and declared dimensions. Ambiguity gets clarify-never-guess ("By 'market' — country, or revenue segment?"): the conversational form of refuse-don't-plug.
2. **Frame discipline on follow-ups.** Multi-turn queries inherit the prior frame, and every answer restates the full applied frame ("Gross margin · Jul-26 · constant currency · excl. France · MET-003 v1.0"). The frame line is the control against out-of-context screenshots.
3. **Triage per doc 70.** One-call cheap-model triage: lookup → cheapest tier; re-slice/lineage → mid; judgment drift → decline-with-data. Test: does the answer change a decision or enter the record? When an answer will be quoted externally, offer to PIN it as a logged, citable artifact tied to its query.
4. **Eval suite.** ~50 free-form questions with expected behaviors (answer-with-provenance / clarify / refuse-and-draft-entry), scored on every prompt change — refusal behavior is the property most likely to erode. Seed from doc 21's four-question demo; grow from the query log.
5. **MVP treatment (amends doc 68).** Static artifact gains screen 6: the Co-pilot as a replayed transcript ending on the refusal beat. The live Co-pilot becomes the second live moment alongside preflight, used when room and connectivity allow.

Unchanged and non-negotiable: never writes; full query logging; refusal-rate and repeat-query clusters feed the reporting backlog — with free-form primary, the query log is the requirements document for standard reporting.
