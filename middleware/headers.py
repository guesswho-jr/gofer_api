from django.http import JsonResponse



class AuthorizationHeaderCheck:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        if 'auth' not in request.path:
            if 'admin' not in request.path:
                if 'HTTP_AUTHORIZATION' not in request.META:
                    return JsonResponse({
                        "info": [
                            "There is something wrong with authentication.",
                        ]
                    }, status=400)
        # pass
        return self.get_response(request)