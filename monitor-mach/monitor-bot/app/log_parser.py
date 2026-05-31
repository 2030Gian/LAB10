import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional


LOG_PATTERN = re.compile(
    r"^(?P<timestamp>\S+)\s+"
    r"(?P<module>\S+)\s+"
    r"(?P<api>\S+)\s+"
    r"(?P<function>\S+)\s+"
    r"(?P<message>.*)$"
)

STATUS_PATTERN = re.compile(r"status=(?P<status>\d+)")
LATENCY_PATTERN = re.compile(r"latency_ms=(?P<latency>[\d.]+)")


@dataclass
class LogEntry:
    timestamp: datetime
    module: str
    api: str
    function: str
    message: str
    status: Optional[int]
    latency_ms: Optional[float]


def parse_log_line(line: str) -> Optional[LogEntry]:
    match = LOG_PATTERN.match(line.strip())

    if not match:
        return None

    data = match.groupdict()

    try:
        timestamp = datetime.fromisoformat(data["timestamp"])
    except ValueError:
        return None

    status_match = STATUS_PATTERN.search(data["message"])
    latency_match = LATENCY_PATTERN.search(data["message"])

    status = int(status_match.group("status")) if status_match else None
    latency_ms = float(latency_match.group("latency")) if latency_match else None

    return LogEntry(
        timestamp=timestamp,
        module=data["module"],
        api=data["api"],
        function=data["function"],
        message=data["message"],
        status=status,
        latency_ms=latency_ms,
    )


def read_logs(log_paths: list[str]) -> list[LogEntry]:
    entries: list[LogEntry] = []

    for path_str in log_paths:
        path = Path(path_str)

        if path.is_dir():
            files = list(path.rglob("*.log"))
        else:
            files = [path]

        for file in files:
            if not file.exists():
                continue

            with open(file, "r", encoding="utf-8") as f:
                for line in f:
                    entry = parse_log_line(line)
                    if entry:
                        entries.append(entry)

    return entries