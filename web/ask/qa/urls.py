from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.test, name='index'),
    path('login/', views.test),
    path('signup/', views.test),
    path('question/<id>/', views.test),
    path('ask/', views.test),
    path('popular/', views.test),
    path('new/', views.test)
]
