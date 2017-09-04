from django.utils.timezone import now
from django.contrib.auth.models import User


class SetLastVisitMiddleware(object):
    """
    Записывает дату последнего визта пользователя
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_template_response(self, request, response):
        if request.user.is_authenticated():
            # Update last visit time after request finished processing.
            profile = request.user.profile
            profile.last_visit = now()
            profile.save()
        return response