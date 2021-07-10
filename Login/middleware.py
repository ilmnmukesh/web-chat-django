import datetime
from django.core.cache import cache
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

class AUserMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        current_user = request.user
        print(request.user)
        if request.user.is_authenticated:
            now = datetime.datetime.now()
            print(now)
            cache.set('seen_%s' %(current_user.username), now, 
                           settings.USER_LASTSEEN_TIMEOUT)
        return response

