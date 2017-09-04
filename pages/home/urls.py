from django.conf.urls import url

from pages.home.views import HomeView, get_animal_results, get_people_results


urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^animal_results/$', get_animal_results, name='animal_results'),
    url(r'^people_results/$', get_people_results, name='people_results'),
]