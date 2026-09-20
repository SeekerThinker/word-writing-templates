# Continuous Web Access Policy

## Publication intent

The PPF publication target is continuously rebuildable HTML. Continuous Web publication is not the same as a formal edition release.

## Visibility

- Source repository: public
- Published site: public
- Current deployment state: staged; not claimed as live until a deployed URL and authenticated browser readback are recorded.

## Private-site rule

For private repositories, the unified reading password must be created and rotated by the owner in Cloudflare Access or an equivalent provider control plane. It must never appear in Git, YAML, GitHub Actions logs, chat, or this repository.

## Acceptance evidence

A deployment is complete only after all of the following are recorded outside this file:

1. Cloudflare project and production URL.
2. Successful build/deploy result.
3. Authenticated browser readback.
4. Unauthenticated access behavior.
5. Rollback or disable procedure.

## Non-goals

This file does not authorize publication, domain changes, source disclosure, or password creation.
