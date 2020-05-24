from django.urls import path
from . import views

urlpatterns = [
    path('', views.questions_paginator, {'paginator_type': 'default'}),
    path('login/', views.test),
    path('signup/', views.test),
    path('question/<int:question_id>/', views.question_page),
    path('ask/', views.add_question),
    path('popular/', views.questions_paginator, {'paginator_type': 'popular'}),
    path('new/', views.test)
]
