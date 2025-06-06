import random
import time

from flask import Flask

from prometheus_client import (
    Counter,
    generate_latest,
    Histogram,
    REGISTRY,
)

# [END monitoring_sli_metrics_prometheus_setup]

app = Flask(__name__)
# [START monitoring_sli_metrics_prometheus_create_metrics]
PYTHON_REQUESTS_COUNTER = Counter("python_requests", "total requests")
PYTHON_FAILED_REQUESTS_COUNTER = Counter("python_failed_requests", "failed requests")
PYTHON_LATENCIES_HISTOGRAM = Histogram(
    "python_request_latency", "request latency by path"
)
# [END monitoring_sli_metrics_prometheus_create_metrics]


@app.route("/")
# [START monitoring_sli_metrics_prometheus_latency]
@PYTHON_LATENCIES_HISTOGRAM.time()
# [END monitoring_sli_metrics_prometheus_latency]
def homePage():
    # count request
    PYTHON_REQUESTS_COUNTER.inc()
    # fail 10% of the time
    if random.randint(0, 100) > 90:
        PYTHON_FAILED_REQUESTS_COUNTER.inc()
        # [END monitoring_sli_metrics_prometheus_counts]
        return ("error!", 500)
    else:
        random_delay = random.randint(0, 5000) / 1000
        # delay for a bit to vary latency measurement
        time.sleep(random_delay)
        return "home page"

# [START monitoring_sli_metrics_prometheus_metrics_endpoint]
@app.route("/metrics", methods=["GET"])
def stats():
    return generate_latest(REGISTRY), 200

# [END monitoring_sli_metrics_prometheus_metrics_endpoint]

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)