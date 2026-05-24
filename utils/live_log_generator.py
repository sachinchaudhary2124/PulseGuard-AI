import random
from datetime import datetime, timedelta


endpoints = [
    "/login",
    "/payment",
    "/orders",
    "/inventory",
    "/search",
    "/profile"
]


def generate_live_logs():

    logs = []

    base_time = datetime.now()

    for i in range(20):

        endpoint = random.choice(endpoints)

        status_code = random.choices(
            [200, 500, 503, 504],
            weights=[70, 10, 10, 10]
        )[0]

        response_time = random.randint(80, 7000)

        # Simulate time progression
        timestamp = base_time + timedelta(seconds=i * 5)

        log = {
            "timestamp": timestamp.strftime("%H:%M:%S"),
            "endpoint": endpoint,
            "status_code": status_code,
            "response_time_ms": response_time
        }

        logs.append(log)

    return logs