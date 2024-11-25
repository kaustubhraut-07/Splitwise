# core/middleware.py

from django.http import JsonResponse

def api_authentication_middleware(get_response):
    def middleware(request):
     
        excluded_paths = ['/user_registeration/', '/user_login/']

        
        if any(request.path.startswith(path) for path in excluded_paths):
            return get_response(request)

        
        # if request.path.startswith('/'):
        #     if not request.user.is_authenticated:
        #         return JsonResponse({'detail': 'Authentication credentials were not provided.'}, status=401)

        response = get_response(request)
        return response

    return middleware
