# Inquiry Publishing Stack — Project State

Updated: 2026-09-20

This file records stack-level continuity only. It does not replace template/release stability rules, compatibility evidence, or project history.

## Project and work units

- Primary project: Word structured-thinking and writing toolkit.
- Desktop artifact set: 12 Word `.dotx` templates across numbering profiles and Windows/macOS.
- Web subproject: local-browser structured editor and public documentation/site.
- Release/maintenance subproject: compatibility tests, release bundles, stability rules, changelog and maintainership documentation.
- Authoritative project state: `README.md`, `STABILITY.md`, `MAINTAINERS.md`, `CHANGELOG.md`, `RELEASE_NOTES.md`, `release/`, current tests and workflows.

## Current goal

Preserve the stable template matrix and local-first Web editor while continuing compatibility/release verification without overstating automated checks as real Microsoft Word validation.

## Confirmed boundaries

- Existing templates, browser-local draft behavior, public website, license, release history, and stable download expectations are preserved.
- Automated OOXML/PDF checks do not become a claim of complete real-Word validation.
- No template/content rewrite or publishing cutover is part of this stack maintenance.

## Stack adoption

- Starter: active, `full-research-publication`, control-plane revision `4889739d448a9bf68bedb42ce3182315eda0caeb`.
- AHICP: active, `research-full`; template/adopted revision remains `3e6c126741b557967ffb848b35b3538ba36e4bb1`.
- PPF: active, project-native continuous Web; template/adopted revision remains `dd332c1a5afe133e063dd063c811ed82127c5ee1`.
- Vault Interface: active; template/adopted revision remains `0e3c646687f675223a4b0829e5b97159685c2ca5`.
- New upstream HEADs are not silently promoted to adopted framework state.

## Privacy, publication, and provider state

- Source repository: public (pre-existing state).
- Existing website: authorized/public through the existing GitHub Pages publication.
- Browser drafts: local by current design; this upgrade does not introduce cloud storage.
- Provider/canonical identity migration: none.

## Unresolved / evidence-needed items

- Real Microsoft Word platform/version validation remains distinct from automated structural checks.
- Any future change to the protected template matrix, filenames, download contracts, or publication provider must follow existing stability/release rules.

## Next step

Run the repository's compatibility, release, Stack, and PPF checks for this branch; merge only after the maintenance PR is clean, then resume project work from existing release/stability sources.
