import inspect
from datetime import datetime

from webmap.database.base import Database


class StatusDB(Database):
    def __init__(self) -> None:
        super().__init__()

    def log_status(self, message: str) -> bool:
        """Log a status message with timestamp and caller file."""
        # Get caller information
        frame = inspect.currentframe().f_back
        filename = frame.f_code.co_filename.split('/')[-1]  # Get just the filename
        
        # Get current timestamp
        timestamp = datetime.now().isoformat()
        
        with self._driver.session() as session:
            result = session.run(
                "CREATE (s:StatusMessage {message: $message, timestamp: $timestamp, filename: $filename}) RETURN s",
                message=message,
                timestamp=timestamp,
                filename=filename
            )
            return result.single() is not None
