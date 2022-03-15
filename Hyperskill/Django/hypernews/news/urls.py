from django.urls import path, re_path
from news.views import MainView, PostView, CreateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', MainView.as_view()),
    path('create/', CreateView.as_view()),
    re_path(r'(?P<link>[^/]+)', PostView.as_view()),
]

urlpatterns += static(settings.STATIC_URL)
