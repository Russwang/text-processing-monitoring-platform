# Repair and validation report

Maintenance date: 2026-09-30. Original coursework directories and Word documents remain untouched in the parent workspace. This repository contains the cleaned portfolio version.

## Confirmed issues and repairs

| Area | Original issue | Repair |
|---|---|---|
| Frontend requests | AbortController signal never reached fetch; late responses could replace newer results | Pass signal, ignore cancellation errors, and check latest controller before displaying results; response-ordering regression |
| Frontend health | All nonempty status strings were treated as Online | Render actual Online/Error/Offline state |
| Frontend configuration | Actions could run before configuration loaded | Await configuration readiness before API calls |
| Frontend storage | Every failure was shown as duplicate or missing ID | Display actual backend errors |
| Gateway | No timeout; upstream errors could become 200 | Five-second timeout, preserve upstream JSON HTTP status, 502/504 for failures |
| Config reload | Invalid content could replace active routes | Validate replacement; retain previous config on failure |
| Java query | Encoded text was counted without decoding | Parse raw query, split once on equals, decode UTF-8; HTTP regression includes spaces, ampersand and plus |
| Java tests | Nonstandard source layout and no explicit JUnit 5 runner | Standard Maven layout, pinned Surefire, fail if zero tests are found |
| PHP health | Missing text parameter generated a warning | Empty default and string validation |
| Node input | Array/object input could reach string counter | Reject non-string text with 400 |
| SQLite storage | Inconsistent read/write paths, check-then-insert race, connection leak on duplicates | Shared path, parent directory creation, managed transactions and atomic primary-key rejection with 409 |
| Monitor database | Missing parent directory prevented initialization | Create directory and table idempotently |
| Monitor correctness | Only HTTP/JSON parsing was checked | Validate integer answer against six configured expectations |
| Monitor latency | Timing sent a second request; its failure could be labelled as performance success | Time the same request with perf_counter; persist SUCCESS/FAILURE/SLOW |
| Monitor state | Tied timestamps and alert/performance records made latest state ambiguous | Select greatest row ID for health samples only |
| Monitor alerts | No timeout; exception text could contain webhook secret | Five-second timeout, environment-only webhook, secret-free delivery errors |
| Deployment | Manual commands and host.docker.internal URLs | Ten-service Compose application, container DNS, Nginx same-origin routes, two data volumes |
| Packaging | Old runtime images, no unified GitHub CI, local artifacts mixed with source | Updated images, Node lockfile, pinned Python direct dependencies, language and container tests, ignores and attribution |

## Local verification

| Suite | Passed cases |
|---|---:|
| Python backend regressions | 15 |
| Original Python vowel-count suite (five input assertions) | 1 |
| Frontend asynchronous/status/storage regressions | 3 |
| Node character counter | 1 |
| Go counting and HTTP handler | 2 |
| Ruby Rack/Sinatra | 4 |
| Java JUnit, including loopback HTTP | 3 |
| **Total** | **29** |

Java tests were compiled with javac 17 and executed with JUnit Platform Console 1.10.0; Maven execution is verified separately in CI. Python compilation, JavaScript syntax and Compose configuration validation passed.

The local Docker build was attempted, but Docker Hub's authentication endpoint timed out. Complete container HTTP validation runs in the GitHub Actions integration job, separately from unit-test results. The local npm audit request could not complete because the reachable mirror does not implement its audit endpoint; no claim is made that dependencies are vulnerability-free.

## Publication contents

Only cleaned source, deployment configuration, tests and documentation are included. Original assignment/submission documents, resumes, databases, editor metadata, prior Git histories and the original webhook value are excluded. Webhook alerts are disabled by default. No external alert was sent during validation.

The original coursework copies were not modified, and existing resume PDFs were not overwritten. Updated bilingual project bullets are in [RESUME_NOTES.md](RESUME_NOTES.md).

See [GitHub Actions](https://github.com/Russwang/text-processing-monitoring-platform/actions) for actual current language and integration results.
