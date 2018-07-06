""" Middleware for saving the current request in thread-local storage

See: https://stackoverflow.com/a/36328564
"""

from threading import current_thread

from django.utils.deprecation import MiddlewareMixin


# Thread-local storage of requests
_requests = {}


def _current_thread():
    """ (Private) get current thread id """
    return current_thread().ident


def _set_request(request):
    """ (Private) clears the current thread-local request """
    _requests[_current_thread()] = request


def _clear_request():
    """ (Private) clears the current thread-local request """
    _requests.pop(_current_thread(), None)


def get_current_request():
    """ Returns the current thread-local request """
    return _requests.get(_current_thread(), None)


class RequestMiddleware(MiddlewareMixin):
    """ Middleware for storing request in thread-locals.

    This middleware should be used sparingly as storing values in thread-locals
    is generally frowned upon in the django community unless there is a good
    reason(https://stackoverflow.com/a/36328564). Our good reason is to access
    the current user at model save() so that we can auto-populate the
    blame columns.
    """

    def process_request(self, request):
        """ Handle incoming request """
        _set_request(request)

    def process_response(self, request, response):
        """ Handle outbound response """
        _clear_request()  # flush request when when completed
        return response

    def process_exception(self, request, exception):
        """ Handle outbound exception (i.e response) """
        _clear_request()  # exception is also a response, flush request
        raise exception
