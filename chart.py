"""Create a bar chart from summary.json."""

import json
import math
from pathlib import Path

import matplotlib.pyplot as plt

INPUT_JSON = Path("summary.json")
OUTPUT_IMAGE = Path("average_temperature.png")


def main():
    if not INPUT_JSON.exists():
        raise SystemExit(
            f"Cannot find {INPUT_JSON}. Run main.py first."
        )

    try:
        with INPUT_JSON.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as exc:
        raise SystemExit(
            f"{INPUT_JSON} is not valid JSON: {exc}"
        ) from exc
    except OSError as exc:
        raise SystemExit(f"Could not read JSON file: {exc}") from exc

    if not isinstance(data, list) or not data:
        raise SystemExit(
            "summary.json contains no device summaries to chart."
        )

    device_ids = []
    averages = []

    for item in data:
        if not isinstance(item, dict):
            continue

        device_id = item.get("device_id")

        try:
            average = float(item["average_temperature"])
        except (KeyError, TypeError, ValueError):
            continue

        if (
            not isinstance(device_id, str)
            or not device_id.strip()
            or not math.isfinite(average)
        ):
            continue

        device_ids.append(device_id)
        averages.append(average)

    if not device_ids:
        raise SystemExit(
            "No valid device IDs and average temperatures were found."
        )

    figure_width = max(9, len(device_ids) * 1.5)
    fig, ax = plt.subplots(figsize=(figure_width, 6))

    bars = ax.bar(device_ids, averages)

    ax.set_title("Average Temperature by Device", pad=16)
    ax.set_xlabel("Device ID", labelpad=10)
    ax.set_ylabel("Average Temperature", labelpad=10)

    ax.bar_label(bars, fmt="%.2f", padding=4)
    ax.tick_params(axis="x", labelrotation=30)

    ax.grid(axis="y", linestyle="--", alpha=0.35)
    ax.set_axisbelow(True)

    fig.tight_layout()

    try:
        fig.savefig(
            OUTPUT_IMAGE,
            dpi=150,
            bbox_inches="tight"
        )
    except OSError as exc:
        raise SystemExit(f"Could not save chart: {exc}") from exc
    finally:
        plt.close(fig)

    print(f"Chart saved to {OUTPUT_IMAGE}")


if __name__ == "__main__":
    main()