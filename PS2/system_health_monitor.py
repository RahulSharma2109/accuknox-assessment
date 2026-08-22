#!/usr/bin/env python3

import json
import logging
import os
import sys
import psutil
from datetime import datetime


CONFIG_FILE = "config.json"


def load_config():
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"ERROR: Configuration file '{CONFIG_FILE}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as exc:
        print(f"ERROR: Invalid JSON configuration: {exc}")
        sys.exit(1)


def setup_logging(log_file):
    log_directory = os.path.dirname(log_file)

    if log_directory:
        os.makedirs(log_directory, exist_ok=True)

    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s"
    )


def get_system_metrics():
    cpu_usage = psutil.cpu_percent(interval=1)

    memory = psutil.virtual_memory()
    memory_usage = memory.percent

    disk = psutil.disk_usage("/")
    disk_usage = disk.percent

    process_count = len(psutil.pids())

    return {
        "cpu": cpu_usage,
        "memory": memory_usage,
        "disk": disk_usage,
        "processes": process_count
    }


def check_thresholds(metrics, config):
    alerts = []

    if metrics["cpu"] > config["cpu_threshold"]:
        alerts.append(
            f"CPU usage is high: {metrics['cpu']:.1f}% "
            f"(threshold: {config['cpu_threshold']}%)"
        )

    if metrics["memory"] > config["memory_threshold"]:
        alerts.append(
            f"Memory usage is high: {metrics['memory']:.1f}% "
            f"(threshold: {config['memory_threshold']}%)"
        )

    if metrics["disk"] > config["disk_threshold"]:
        alerts.append(
            f"Disk usage is high: {metrics['disk']:.1f}% "
            f"(threshold: {config['disk_threshold']}%)"
        )

    if metrics["processes"] > config["process_threshold"]:
        alerts.append(
            f"Process count is high: {metrics['processes']} "
            f"(threshold: {config['process_threshold']})"
        )

    return alerts


def display_report(metrics, alerts):
    print("\n========================================")
    print("       SYSTEM HEALTH MONITOR")
    print("========================================")
    print(f"Timestamp        : {datetime.now().isoformat(timespec='seconds')}")
    print(f"CPU Usage        : {metrics['cpu']:.1f}%")
    print(f"Memory Usage     : {metrics['memory']:.1f}%")
    print(f"Disk Usage       : {metrics['disk']:.1f}%")
    print(f"Running Processes: {metrics['processes']}")

    if alerts:
        print("\nSTATUS: ALERT")

        for alert in alerts:
            print(f"[ALERT] {alert}")
    else:
        print("\nSTATUS: HEALTHY")
        print("All monitored metrics are within configured thresholds.")

    print("========================================\n")


def main():
    config = load_config()
    setup_logging(config["log_file"])

    metrics = get_system_metrics()
    alerts = check_thresholds(metrics, config)

    display_report(metrics, alerts)

    if alerts:
        logging.warning("System health alerts detected.")

        for alert in alerts:
            logging.warning(alert)
    else:
        logging.info("System health check completed successfully.")

    return 1 if alerts else 0


if __name__ == "__main__":
    sys.exit(main())
