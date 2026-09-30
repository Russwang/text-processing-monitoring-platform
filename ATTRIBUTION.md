# Attribution and project history

Built from cloud computing coursework and maintained as a text-processing and monitoring portfolio.

## Course starter components

The course supplied the original `editor-frontend`, `editor-wordcount` (PHP), and `editor-charcount` (Node.js) implementations. The original character counter's package metadata credits **David Cutting**; this credit is retained. These components are adapted here and are not claimed as implementations written entirely by me.

## Coursework contribution — Xinghao Wang

- Four additional counting services: Python vowel count, Go comma count, Ruby standalone `and` count, and Java palindrome count.
- A Flask gateway, text save/retrieve service backed by SQLite, monitoring and optional Discord alerts.
- Frontend extensions and language-specific test/CI configurations.

## Portfolio maintenance — 2026

The subsequent maintenance fixes frontend cancellation and status reporting, HTTP error handling, Java query decoding and test discovery, SQLite paths and duplicate writes, monitoring correctness/latency, and deployment configuration. It adds Docker Compose, GitHub Actions, regression tests, documentation, and environment-based webhook configuration.

OpenAI Codex assisted with code review, repairs, tests and portfolio packaging. The original submission also records ChatGPT assistance with selected CI configuration and debugging. This maintenance should not be interpreted as the original coursework submission.

No blanket open-source licence is granted for third-party course starter code; its original ownership and terms remain applicable. No course assignment or private submission document is distributed here.
