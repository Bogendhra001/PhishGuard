from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    # path('classify/<str:dynamic_string>/', views.classify, name='classify'),
    re_path(r'^classify/(?P<dynamic_string>.+)/$',
            views.classify, name='classify'),
    # Other URL patterns...
]
