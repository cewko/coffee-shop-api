from django.contrib.auth import get_user_model
from django.utils.timezone import now


User = get_user_model()


class SetLastUserLogin:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            request.user.__class__.objects.filter(
                id=request.user.id
            ).update(last_login=now())
        
        response = self.get_response(request)
        return response