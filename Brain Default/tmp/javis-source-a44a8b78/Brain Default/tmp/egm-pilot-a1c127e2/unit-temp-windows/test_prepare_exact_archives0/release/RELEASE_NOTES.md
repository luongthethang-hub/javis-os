# EGM 0.1.1

Declared source: `aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`
Tag: `v0.1.1`

Local source identity is caller-supplied and is not verified by this script. Publish only workflow-built candidates after exact-artifact checks.

Runtime archives: Claude and OpenAI. Verify downloads with `sha256sum -c SHA256SUMS`.

For CI-built candidates, verify each ZIP with `gh attestation verify FILE --repo google/elephant-goldfish-model --signer-workflow google/elephant-goldfish-model/.github/workflows/release.yml --source-ref refs/heads/main`. Provenance identifies the main-branch workflow run; the tagged source commit is recorded above. Local builds have no attestation.

## Changes

Maintainer: summarize changes and migration steps before publishing.

## Verification

Offline unit tests and runtime packaging are checked by CI. Live installation, workflow execution, reviewer isolation, directory approval, and cloud-host support are not established by this build. Maintainer: attach exact-bundle host evidence and limitations before publishing.
