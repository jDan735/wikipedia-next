from django.urls import path

from . import views

urlpatterns = [
    path('wikipedia/search/<str:q>/', views.wikipedia_search),
]
