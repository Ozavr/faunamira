from django.contrib.auth.models import User
from django.db.models import Q

def get_similar_people(user, people):
    """
    Поиск похожих людей
    """
    query = User.objects.filter(is_active=True).exclude(username=people.username).exclude(username=user.username)
    if query:
        try:
            pfind = people.about.find
            ppurp = people.about.purpose
        except:
            results = None
        else:
            results = query.filter(profile__gender=pfind, about__purpose=ppurp)
            if not results:
                results = query.filter(Q(profile__gender=pfind) | Q(about__purpose=ppurp))
                if not results:
                    results = query
    else:
        results = None
    return results