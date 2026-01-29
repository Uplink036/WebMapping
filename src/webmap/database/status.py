import inspect
from datetime import datetime
from types import FrameType
from typing import cast

from webmap.database.base import Database


class StatusDB(Database):
    def __init__(self) -> None:
        super().__init__()

    def _get_caller_information(
        self, frame: FrameType
    ) -> tuple[str, int, str, list[str] | None, int | None]:
        """Return information regarding the previous frame to the frame"""
        previous_frame = frame.f_back
        if previous_frame is None:
            raise ValueError("Database error: Could not get FrameType")
        (
            absolute_file_path,
            line_number,
            function_name,
            lines,
            index,
        ) = inspect.getframeinfo(previous_frame)

        return (absolute_file_path, line_number, function_name, lines, index)

    def log_status(self, message: str) -> bool:
        """Log a status message with extra information on caller"""

        current_frame = inspect.currentframe()
        if current_frame is None:
            raise ValueError("Database error: Could not get FrameType")
        caller_info = self._get_caller_information(current_frame)
        caller_file = caller_info[0]
        filename: str = caller_file.split("/")[-1]
        timestamp = datetime.now().isoformat()

        with self._driver.session() as session:
            result = session.run(
                "CREATE (s:StatusMessage {message: $message, timestamp: $timestamp, filename: $filename}) RETURN s",
                message=message,
                timestamp=timestamp,
                filename=filename,
            )
            return result.single() is not None
