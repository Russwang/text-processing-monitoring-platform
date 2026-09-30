# HTTP API

All examples use the frontend origin `http://localhost:8080`. Endpoints accept and return JSON unless otherwise noted.

| Method | Frontend path | Description |
|---|---|---|
| GET | `/api/count/{service}?text=...` | Count text with `wordcount`, `charcount`, `vowelcount`, `commacount`, `andcount`, or `palindromecount`; result contains integer `answer` |
| GET | `/api/count/check-services` | HTTP availability: `Online`, `Error`, `Offline` for each configured service |
| POST | `/api/count/reload-config` | Re-read gateway config; reject invalid config while preserving the previous mapping |
| POST | `/api/text/saveText` | Save `{"id":"demo","text":"Hello world"}`; return 201, or 409 for an existing ID |
| GET | `/api/text/getText?id=demo` | Return `{"text":"Hello world"}`; return 404 if absent |
| GET | `/api/monitor/service-status` | Latest health sample per service: `SUCCESS`, `FAILURE`, or `SLOW` |
| GET | `/api/monitor/recent-performance` | Twelve most recent log records, newest first |

```bash
curl 'http://localhost:8080/api/count/vowelcount?text=Hello'
curl -X POST 'http://localhost:8080/api/text/saveText' \
  -H 'Content-Type: application/json' -d '{"id":"demo","text":"Hello world"}'
curl 'http://localhost:8080/api/text/getText?id=demo'
```

Counting requests preserve the upstream JSON HTTP status. Gateway errors use JSON and status 404 (unknown service), 502 (unavailable or malformed upstream response), or 504 (timeout). Storage rejects malformed/non-object JSON and empty or non-string IDs/text with 400. Health checks have a two-second timeout per service, and routed/monitored requests have a five-second timeout.

The monitor is sequential; a scheduled minute is not a measured maximum detection delay. It performs an initial pass at startup and may record failures while dependent containers are still starting. These are replaced by subsequent successful samples. Latest state is selected by monotonically increasing SQLite row ID, so logs sharing a timestamp cannot make state selection ambiguous.

English word and palindrome tokenisation, UTF-16 character length and ASCII counting conventions are preserved from the course implementation. The six counters do not all use the same Unicode tokenisation policy.
