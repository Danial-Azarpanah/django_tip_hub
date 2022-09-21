from .models import IPAddress


class SaveIpAddressMiddleware:
    """
    Middleware for IP address
    in view counting
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

        # Get IP adress of the user
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        # Try to get IP address, If doesn't exist, create one
        try:
            ip_address = IPAddress.objects.get(ip_address=ip)
        except IPAddress.DoesNotExist:
            ip_address = IPAddress(ip_address=ip)
            ip_address.save()

        request.user.ip_address = ip_address
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response