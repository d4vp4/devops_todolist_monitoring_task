from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from django.http import HttpResponse

HTTP_REQUESTS_TOTAL = Counter(
    'http_requests_total',
    'Total number of HTTP requests',
    ['method']
)

class PrometheusMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/metrics':
            metrics_data = generate_latest()
            return HttpResponse(metrics_data, content_type=CONTENT_TYPE_LATEST)

        if request.method in ['GET', 'POST']:
            HTTP_REQUESTS_TOTAL.labels(method=request.method).inc()

        response = self.get_response(request)
        return response