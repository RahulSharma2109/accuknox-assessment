import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from application_health_checker import check_application


def test_application_is_up():
    result = check_application(
        "https://wisecow.local",
        timeout=10,
        insecure=True
    )

    assert result["status"] == "UP"
    assert result["http_status"] == 200


def test_application_is_down():
    result = check_application(
        "https://localhost:9999",
        timeout=3,
        insecure=True
    )

    assert result["status"] == "DOWN"
    assert result["http_status"] is None
