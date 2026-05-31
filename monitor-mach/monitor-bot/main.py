import argparse

from app.commands import (
    check_availability,
    check_latency,
    render_graph,
    stats,
)


def main():
    parser = argparse.ArgumentParser(
        description="MonitorMach Bot CLI"
    )

    subparsers = parser.add_subparsers(dest="command")

    latency_parser = subparsers.add_parser("CheckLatency")
    latency_parser.add_argument("module")
    latency_parser.add_argument("--start-date", required=True)
    latency_parser.add_argument("--end-date", required=True)

    availability_parser = subparsers.add_parser("CheckAvailability")
    availability_parser.add_argument("module")
    availability_parser.add_argument("--last-days", type=int, required=True)

    graph_parser = subparsers.add_parser("RenderGraph")
    graph_parser.add_argument("--metric", required=True, choices=["Latency", "Availability"])
    graph_parser.add_argument("--module", required=True)
    graph_parser.add_argument("--last-days", type=int, required=True)

    stats_parser = subparsers.add_parser("Stats")
    stats_parser.add_argument("module")
    stats_parser.add_argument("--last-days", type=int, required=True)

    args = parser.parse_args()

    if args.command == "CheckLatency":
        check_latency(args.module, args.start_date, args.end_date)

    elif args.command == "CheckAvailability":
        check_availability(args.module, args.last_days)

    elif args.command == "RenderGraph":
        render_graph(args.metric, args.module, args.last_days)

    elif args.command == "Stats":
        stats(args.module, args.last_days)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()