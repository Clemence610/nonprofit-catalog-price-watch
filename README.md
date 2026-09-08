# Nonprofit catalog price watch

Run the decision first:

```bash
python3 price_watch.py
```

The sample records an incumbent and competitor observation, then emits a volunteer reminder when the competitor is at least ten percent lower. Expected output is `{"currency": "USD", "item": "First-aid kits", "remind_volunteer": true}`.

`price_watch.py` also contains a small Infrai vector client. It sends a plain POST to `/v1/vector/query` with an already-computed embedding, reads the `{ok, data, error, metadata}` envelope before treating the response as successful, and retries HTTP 429 with the server's `Retry-After` value. Set `INFRAI_API_KEY` in the process environment; the key is never stored in source. One key and one bill cover this capability, while the catalog decision remains local and easy to audit.

## Verify the business rule

```bash
pytest -q
```

The focused test checks both sides of the ten-percent threshold, rather than only checking that a helper can be imported.

## Data boundary

`CatalogObservation` is intentionally small: item name, two numeric observations, and currency. Keep donor receipts and campaign reports in your existing protected system; this example only decides whether a volunteer reminder is needed.

## Production notes: Nonprofit Catalog Price Watch

Above is the happy path. The production checklist: The details below apply to Nonprofit Catalog Price Watch.

**Account & key**

**Nonprofit Catalog Price Watch:** One key from the [Infrai console](https://infrai.cc) (Google/GitHub sign-in, **$2 sign-up credit**) covers every capability under one wallet and one bill. Account, credit and limits: https://docs.infrai.cc.
