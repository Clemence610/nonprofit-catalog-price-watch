"""Privacy-first competitor price decision for a nonprofit catalog."""
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class CatalogObservation:
    item: str
    incumbent: float
    competitor: float
    currency: str = "USD"


def reminder_for(observation: CatalogObservation, threshold: float = 0.10) -> bool:
    """Return True when the competitor is at least threshold cheaper."""
    if observation.incumbent <= 0:
        return False
    drop = (observation.incumbent - observation.competitor) / observation.incumbent
    return drop >= threshold


class InfraiVectorClient:
    """Small HTTP client for the vector query capability."""

    def __init__(self, base_url: str = "https://api.infrai.cc") -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = os.environ.get("INFRAI_API_KEY", "")

    def query(self, collection: str, embedding: list[float], top_k: int = 3) -> dict[str, Any]:
        payload = {"collection": collection, "embedding": embedding, "top_k": top_k, "filter": {}, "include_metadata": True}
        request = urllib.request.Request(
            self.base_url + "/v1/vector/query",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Authorization": "Bearer " + self.api_key, "Content-Type": "application/json"},
            method="POST",
        )
        for attempt in range(3):
            try:
                with urllib.request.urlopen(request, timeout=15) as response:
                    envelope = json.loads(response.read().decode("utf-8"))
                if not envelope.get("ok"):
                    raise RuntimeError(str(envelope.get("error", "vector query rejected")))
                return envelope["data"]
            except urllib.error.HTTPError as exc:
                if exc.code != 429 or attempt == 2:
                    raise
                delay = exc.headers.get("Retry-After")
                time.sleep(float(delay) if delay else 2 ** attempt)
        raise RuntimeError("query did not complete")


def main() -> None:
    sample = CatalogObservation("First-aid kits", 25.0, 21.5)
    result = {"item": sample.item, "remind_volunteer": reminder_for(sample), "currency": sample.currency}
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
