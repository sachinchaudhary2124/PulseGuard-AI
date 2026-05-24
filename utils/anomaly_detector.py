def detect_anomalies(logs):
    """
    Detect anomalies in API logs.
    """

    anomalies = []

    for log in logs:

        severity = "Low"

        # Critical server failures
        if log["status_code"] >= 500:

            if log["response_time_ms"] > 5000:
                severity = "Critical"
            else:
                severity = "High"

            anomalies.append({
                "severity": severity,
                "type": "Server Error",
                "endpoint": log["endpoint"],
                "status_code": log["status_code"],
                "response_time_ms": log["response_time_ms"],
                "message": f"Server error detected in {log['endpoint']}"
            })

        # High latency detection
        if log["response_time_ms"] > 3000:

            if log["response_time_ms"] > 5000:
                severity = "High"
            else:
                severity = "Medium"

            anomalies.append({
                "severity": severity,
                "type": "High Latency",
                "endpoint": log["endpoint"],
                "status_code": log["status_code"],
                "response_time_ms": log["response_time_ms"],
                "message": f"High latency detected in {log['endpoint']}"
            })

    return anomalies