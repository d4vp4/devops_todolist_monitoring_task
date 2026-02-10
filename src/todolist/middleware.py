import time
from prometheus_client import Counter, Gauge  # <--- Додали Gauge

REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests', ['method', 'endpoint', 'http_status'])

start_time = Gauge('http_requests_created', 'Time when the metrics were created')
start_time.set_to_current_time()

class MetricsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.path != '/metrics':
            REQUEST_COUNT.labels(
                method=request.method,
                endpoint=request.path,
                http_status=response.status_code
            ).inc()

        return response