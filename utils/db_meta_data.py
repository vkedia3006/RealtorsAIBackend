from datetime import datetime, UTC

def with_meta(doc: dict, is_update=False) -> dict:
    now = datetime.now(UTC)
    if is_update:
        doc.setdefault("meta", {})["modified_at"] = now
    else:
        doc["meta"] = {
            "created_at": now,
            "modified_at": now
        }
    return doc