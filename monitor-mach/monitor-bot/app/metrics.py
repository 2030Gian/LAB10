from collections import Counter, defaultdict
from datetime import datetime, timedelta
from statistics import mean
from typing import Optional

from app.log_parser import LogEntry


def filter_entries(
    entries: list[LogEntry],
    module: str,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> list[LogEntry]:
    result = []

    for entry in entries:
        if entry.module.lower() != module.lower():
            continue

        if start_date and entry.timestamp < start_date:
            continue

        if end_date and entry.timestamp > end_date:
            continue

        result.append(entry)

    return result


def get_last_days_range(days: int) -> tuple[datetime, datetime]:
    end = datetime.now()
    start = end - timedelta(days=days)
    return start, end


def calculate_daily_latency(entries: list[LogEntry]) -> dict[str, float]:
    grouped = defaultdict(list)

    for entry in entries:
        if entry.latency_ms is not None:
            day = entry.timestamp.strftime("%d/%m")
            grouped[day].append(entry.latency_ms)

    return {
        day: round(mean(values), 2)
        for day, values in sorted(grouped.items())
        if values
    }


def calculate_daily_availability(entries: list[LogEntry]) -> dict[str, float]:
    grouped = defaultdict(lambda: {"success": 0, "error": 0})

    for entry in entries:
        if entry.status is None:
            continue

        day = entry.timestamp.strftime("%d/%m")

        if entry.status == 200:
            grouped[day]["success"] += 1
        elif entry.status >= 500:
            grouped[day]["error"] += 1

    result = {}

    for day, values in sorted(grouped.items()):
        success = values["success"]
        error = values["error"]
        total = success + error

        if total == 0:
            result[day] = 0
        else:
            result[day] = round((success / total) * 100, 2)

    return result


def percentile(values: list[float], p: float) -> float:
    if not values:
        return 0

    values = sorted(values)
    index = int(round((p / 100) * (len(values) - 1)))
    return values[index]


def calculate_general_stats(entries: list[LogEntry]) -> dict:
    latencies = [
        entry.latency_ms
        for entry in entries
        if entry.latency_ms is not None
    ]

    statuses = [
        entry.status
        for entry in entries
        if entry.status is not None
    ]

    total_requests = len(statuses)
    success_count = sum(1 for status in statuses if status == 200)
    error_count = sum(1 for status in statuses if status >= 500)

    if entries:
        min_time = min(entry.timestamp for entry in entries)
        max_time = max(entry.timestamp for entry in entries)
        duration_minutes = max((max_time - min_time).total_seconds() / 60, 1)
    else:
        duration_minutes = 1

    failing_endpoints = Counter(
        entry.api
        for entry in entries
        if entry.status is not None and entry.status >= 500
    )

    top_failing_endpoint = failing_endpoints.most_common(1)

    return {
        "p95_latency_ms": round(percentile(latencies, 95), 2),
        "requests_per_minute": round(total_requests / duration_minutes, 2),
        "error_ratio": round((error_count / total_requests) * 100, 2) if total_requests else 0,
        "throughput": round(success_count / duration_minutes, 2),
        "top_failing_endpoint": top_failing_endpoint[0][0] if top_failing_endpoint else "N/A",
        "total_requests": total_requests,
        "success_count": success_count,
        "error_count": error_count,
        "avg_latency_ms": round(mean(latencies), 2) if latencies else 0,
    }


def detect_bottleneck(entries: list[LogEntry]) -> str:
    module_latencies = defaultdict(list)

    for entry in entries:
        if entry.latency_ms is not None:
            module_latencies[entry.module].append(entry.latency_ms)

    if not module_latencies:
        return "No hay datos suficientes para detectar bottleneck."

    avg_by_module = {
        module: mean(values)
        for module, values in module_latencies.items()
        if values
    }

    bottleneck = max(avg_by_module, key=avg_by_module.get)

    return f"El bottleneck parece estar en {bottleneck}, con latencia promedio de {round(avg_by_module[bottleneck], 2)} ms."


def retry_recommendation(stats: dict) -> str:
    if stats["error_count"] == 0:
        return "No se observan errores 500. No parece necesario agregar retry por ahora."

    if stats["error_ratio"] >= 5:
        return "Sí conviene agregar retry en llamadas a endpoints con errores 500 frecuentes."

    return "Podría agregarse retry con backoff solo para errores 500 o timeouts."


def scaling_recommendation(stats: dict) -> str:
    if stats["p95_latency_ms"] > 2000 or stats["error_ratio"] > 10:
        return "Sí debería evaluarse escalar, porque hay alta latencia P95 o alto ratio de error."

    return "No parece necesario escalar todavía; el servicio se mantiene estable."