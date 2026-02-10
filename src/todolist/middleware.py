import time
from prometheus_client import Counter, Gauge

class PrometheusMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Лічильник запитів
        self.request_counter = Counter('http_requests_total', 'Total HTTP Requests', ['method'])
        # Метрика часу запуску (вимога ментора)
        self.creation_time = Gauge('http_requests_total_created', 'Time when the counter was created')
        self.creation_time.set(time.time())

    def __call__(self, request):
        response = self.get_response(request)
        if request.path != '/metrics':
            self.request_counter.labels(method=request.method).inc()
        return response
