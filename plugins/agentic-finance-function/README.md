# Agentic Finance Function plugin

An installable, skill-first version of the repository's governance model for Codex and Claude Code.

It helps a finance leader review source exports, gate data readiness, resolve contested metric definitions, analyze variances, surface owned exceptions, and prepare a decision-ready brief. It does not include the unpublished finance engine and does not post journals, approve payments, or modify source systems.

## Try it

Give the agent a completed month's exports and ask:

> Review these finance files. Start with a data-readiness verdict, identify any definition decisions, and produce a traceable executive brief with owned exceptions.

The plugin will classify the request as ready, degraded, or blocked before producing analysis. Material claims are labeled as observed, derived, or inferred.

## Codex

From the repository root:

```bash
codex plugin marketplace add .
codex plugin add agentic-finance-function@agentic-finance
```

Start a new Codex session, then ask for a close review, variance analysis, management pack review, reforecast review, or finance-function assessment.

## Claude Code

The bundled skill uses Claude Code's standard `skills/<name>/SKILL.md` layout. The plugin also includes a `.claude-plugin/plugin.json` manifest, so it can be validated and distributed through a Claude Code plugin marketplace.

For a project-local trial, copy `skills/governed-finance-review/` to `.claude/skills/governed-finance-review/` in the target project.

## Product boundary

This version proves the judgment and review workflow. The next product step is a read-only MCP service over a governed company instance, with authentication, company-level data isolation, and review logging. Native GL, billing, CRM, and contract integrations should follow evidence from real design partners.
