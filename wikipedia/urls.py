from django.urls import path

from . import views

urlpatterns = [
    path('', views.wikipedia_search),
    path('<str:page_name>', views.get_wiki_page)
]
