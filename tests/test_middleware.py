import pytest


THREAD_IDENT = 'threadid'


@pytest.fixture
def middleware(monkeypatch):
    from unittest.mock import Mock
    from blame import middleware as implementation

    current_thread = Mock(ident=THREAD_IDENT)
    monkeypatch.setattr(
        implementation, 'current_thread', lambda: current_thread)

    middleware = implementation.RequestMiddleware()
    return middleware


@pytest.fixture
def http_request():
    from unittest.mock import Mock
    return Mock(session={})


def test_process_request(monkeypatch, middleware, http_request):
    """ It should be able to save the current request to thread-local storage
    """
    from blame.middleware import _requests
    middleware.process_request(http_request)
    assert _requests[THREAD_IDENT] == http_request


def test_process_resonse(monkeypatch, middleware, http_request):
    """ It should cleanup thread local storage when the request is complete """
    from unittest.mock import Mock
    from blame.middleware import _requests
    _requests[THREAD_IDENT] = http_request
    middleware.process_response(http_request, response=Mock())
    assert THREAD_IDENT not in _requests


def test_process_exception(monkeypatch, middleware, http_request):
    """ It should cleanup thread local storage when the request is complete
    due to exception.
    """
    from unittest.mock import Mock
    from blame.middleware import _requests
    _requests[THREAD_IDENT] = http_request
    try:
        middleware.process_exception(http_request, exception=Mock())
    except Exception:
        assert THREAD_IDENT not in _requests


def test_get_current_request(monkeypatch, middleware, http_request):
    """ It should cleanup thread local storage when the request is complete
    due to exception.
    """
    from blame.middleware import _requests, get_current_request

    _requests[THREAD_IDENT] = http_request

    assert get_current_request() == http_request
