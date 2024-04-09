from src.db.engine import DatabaseEngine
from src.settings import (
    DatabaseSettings,
    get_settings,
)

db_engine = DatabaseEngine(
    db_url=str(get_settings(DatabaseSettings).url),
    debug=False
)
