from datetime import datetime, timezone, timedelta


def iso_to_datetime(iso_timestamp: str, /) -> datetime:
    """Converts an ISO8601 timestamp to a `datetime` object."""
    return datetime.fromisoformat(iso_timestamp)


def snowflake_to_datetime(int_snowflake: int, /) -> datetime:
    """Converts a Discord Snowflake to a `datetime` object."""
    discord_epoch = datetime(2015, 1, 1, tzinfo=timezone.utc)
    timestamp_ms = (int_snowflake >> 22)
    return discord_epoch + timedelta(milliseconds=timestamp_ms)
