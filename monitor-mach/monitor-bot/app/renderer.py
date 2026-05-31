def render_table(data: dict[str, float], suffix: str = ""):
    if not data:
        print("No hay datos para mostrar.")
        return

    for day, value in data.items():
        print(f"{day} {value}{suffix}")


def render_ascii_graph(data: dict[str, float], title: str):
    if not data:
        print("No hay datos para graficar.")
        return

    print()
    print(title)
    print("=" * len(title))

    max_value = max(data.values())

    for day, value in data.items():
        if max_value == 0:
            bar_length = 0
        else:
            bar_length = int((value / max_value) * 40)

        bar = "█" * bar_length
        print(f"{day} | {bar} {value}")

    print()