import datetime
import sqlite3


def adapt_date_iso(val: datetime.date) -> str:
    """Adapt datetime.date to ISO 8601 date."""
    return val.isoformat()


def convert_date(val):
    """Convert ISO 8601 date to datetime.date object."""
    return datetime.date.fromisoformat(val.decode())


sqlite3.register_adapter(datetime.date, adapt_date_iso)
sqlite3.register_converter("date", convert_date)
