from django.http import HttpResponseForbidden


class PreventRegistrationMiddleware:
    """
    Middleware for preventing user registration access.

    This middleware class restricts access to
    user registration pages by checking
    the request's path. If the path starts with '/auth/register/',
    it returns an HTTP 403 Forbidden response
    with a message indicating that registration
    is not allowed.
    """

    def __init__(self, get_response):
        """Initialize the PreventRegistrationMiddleware."""
        self.get_response = get_response

    def __call__(self, request):
        """Check for registration access and handle the request."""
        if request.path.startswith('/auth/register/'):
            return HttpResponseForbidden("Registration is not allowed")
        return self.get_response(request)
