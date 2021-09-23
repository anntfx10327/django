from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("searches", views.searches, name="searches"),
    path("newpage", views.newpage, name="newpage"),
    path("editpage/<str:title>", views.editpage, name="editpage"),
    path("randompage", views.randompage, name="randompage"),
]
