from datetime import datetime, timedelta

from app.log_parser import read_logs
from app.metrics import (
    calculate_daily_availability,
    calculate_daily_latency,
    calculate_general_stats,
    detect_bottleneck,
    filter_entries,
    get_last_days_range,
    retry_recommendation,
    scaling_recommendation,
)
from app.renderer import render_ascii_graph, render_table


DEFAULT_LOG_PATHS = [
    "../search-api/logs",
    "../poke-stats-service/logs",
    "../poke-images-service/logs",
]


def parse_date(value: str) -> datetime:
    return datetime.strptime(value, "%Y-%m-%d")


def check_latency(module: str, start_date: str, end_date: str, log_paths=None):
    log_paths = log_paths or DEFAULT_LOG_PATHS
    entries = read_logs(log_paths)

    start = parse_date(start_date)
    end = parse_date(end_date) + timedelta(days=1)

    filtered = filter_entries(entries, module, start, end)
    daily_latency = calculate_daily_latency(filtered)

    print(f"Latency for module: {module}")
    render_table(daily_latency, suffix="ms")


def check_availability(module: str, last_days: int, log_paths=None):
    log_paths = log_paths or DEFAULT_LOG_PATHS
    entries = read_logs(log_paths)

    start, end = get_last_days_range(last_days)

    filtered = filter_entries(entries, module, start, end)
    availability = calculate_daily_availability(filtered)

    print(f"Availability for module: {module}")
    render_table(availability, suffix="%")


def render_graph(metric: str, module: str, last_days: int, log_paths=None):
    log_paths = log_paths or DEFAULT_LOG_PATHS
    entries = read_logs(log_paths)

    start, end = get_last_days_range(last_days)
    filtered = filter_entries(entries, module, start, end)

    metric_lower = metric.lower()

    if metric_lower == "latency":
        data = calculate_daily_latency(filtered)
        render_ascii_graph(data, f"Latency graph for {module}")
    elif metric_lower == "availability":
        data = calculate_daily_availability(filtered)
        render_ascii_graph(data, f"Availability graph for {module}")
    else:
        print("Metric inválida. Usa Latency o Availability.")


def stats(module: str, last_days: int, log_paths=None):
    log_paths = log_paths or DEFAULT_LOG_PATHS
    entries = read_logs(log_paths)

    start, end = get_last_days_range(last_days)
    filtered = filter_entries(entries, module, start, end)

    general_stats = calculate_general_stats(filtered)

    print(f"Stats for module: {module}")
    print(f"P95 latency: {general_stats['p95_latency_ms']} ms")
    print(f"Requests per minute: {general_stats['requests_per_minute']}")
    print(f"Error ratio: {general_stats['error_ratio']}%")
    print(f"Throughput: {general_stats['throughput']} successful req/min")
    print(f"Top failing endpoint: {general_stats['top_failing_endpoint']}")
    print(f"Total requests: {general_stats['total_requests']}")
    print(f"Success count: {general_stats['success_count']}")
    print(f"Error count: {general_stats['error_count']}")
    print(f"Average latency: {general_stats['avg_latency_ms']} ms")

    print()
    print("Analysis")
    print(detect_bottleneck(filtered))
    print(retry_recommendation(general_stats))
    print(scaling_recommendation(general_stats))