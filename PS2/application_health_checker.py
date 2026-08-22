#!/usr/bin/env python3

import argparse
import json
import logging
import sys
import time
import urllib.error
import urllib.request
import ssl
from datetime import datetime


def check_application(url, timeout=10, insecure=False):
    start_time = time.perf_counter()

    try:
        if insecure:
            ssl_context = ssl._create_unverified_context()
        else:
            ssl_context = ssl.create_default_context()

        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Python-Application-Health-Checker/1.0"
            }
        )

        with urllib.request.urlopen(
            request,
            timeout=timeout,
            context=ssl_context
        ) as response:

            elapsed = time.perf_counter() - start_time

            return {
                "url": url,
                "status": "UP",
                "http_status": response.status,
                "response_time_ms": round(elapsed * 1000, 2),
                "timestamp": datetime.now().isoformat(timespec="seconds")
            }

    except urllib.error.HTTPError as exc:

        elapsed = time.perf_counter() - start_time

        return {
            "url": url,
            "status": "DOWN",
            "http_status": exc.code,
            "response_time_ms": round(elapsed * 1000, 2),
            "error": f"HTTP error: {exc.code}",
            "timestamp": datetime.now().isoformat(timespec="seconds")
        }

    except urllib.error.URLError as exc:

        elapsed = time.perf_counter() - start_time

        return {
            "url": url,
            "status": "DOWN",
            "http_status": None,
            "response_time_ms": round(elapsed * 1000, 2),
            "error": str(exc.reason),
            "timestamp": datetime.now().isoformat(timespec="seconds")
        }

    except Exception as exc:

        elapsed = time.perf_counter() - start_time

        return {
            "url": url,
            "status": "DOWN",
            "http_status": None,
            "response_time_ms": round(elapsed * 1000, 2),
            "error": str(exc),
            "timestamp": datetime.now().isoformat(timespec="seconds")
        }


def print_result(result):
    print("\n========================================")
    print("       APPLICATION HEALTH CHECK")
    print("========================================")
    print(f"URL            : {result['url']}")
    print(f"Timestamp      : {result['timestamp']}")
    print(f"Status         : {result['status']}")
    print(f"HTTP Status    : {result['http_status']}")
    print(f"Response Time  : {result['response_time_ms']} ms")

    if result.get("error"):
        print(f"Error          : {result['error']}")

    print("========================================\n")


def main():
    parser = argparse.ArgumentParser(
        description="Check whether an HTTP application is up or down."
    )

    parser.add_argument(
        "url",
        help="Application URL to check"
    )

    parser.add_argument(
        "--timeout",
        type=int,
        default=10,
        help="HTTP timeout in seconds (default: 10)"
    )

    parser.add_argument(
        "--insecure",
        action="store_true",
        help="Disable TLS certificate verification"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output result as JSON"
    )

    args = parser.parse_args()

    result = check_application(
        args.url,
        timeout=args.timeout,
        insecure=args.insecure
    )

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_result(result)

    return 0 if result["status"] == "UP" else 1


if __name__ == "__main__":
    sys.exit(main())

