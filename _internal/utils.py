from datetime import datetime

def iso_to_datetime(iso_timestamp: str) -> datetime:
    """Convert an ISO8601 timestamp to a `datetime` object."""
    if iso_timestamp.endswith('Z'):
        iso_timestamp = iso_timestamp[:-1] + '+00:00'
    return datetime.fromisoformat(iso_timestamp)