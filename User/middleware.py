# User/middleware.py

from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

class DisableCSRFOnAPI(MiddlewareMixin):
    def process_request(self, request):
        if request.path.startswith('/User/'):  # सिर्फ User APIs पर CSRF हटे
            setattr(request, '_dont_enforce_csrf_checks', True)
