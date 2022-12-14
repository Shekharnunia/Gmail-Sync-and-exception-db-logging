import traceback
import sys
from django.conf import settings
from django.http import HttpResponse
from .models import ErrorLog


class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.error_log = None
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)
        print(response.__dict__)
        if response.status_code in settings.ERROR_CODES:
            if self.error_log:
                self.error_log.status_code = response.status_code
                self.error_log.save()
            response.status_code = 200
            response._container = [b'Error']
            
        # Code to be executed for each request/response after
        # the view is called.
        return response
    
    def process_exception(self, request, exception):
        """
        Processes exceptions during handling of a http request.
        Logs them with *ERROR* level.
        """
        a, b, stacktrace = sys.exc_info()
        self.error_log = ErrorLog(error_stack=traceback.format_tb(stacktrace))
        return None