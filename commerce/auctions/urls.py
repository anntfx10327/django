from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # path("action/<int:pk>", views.ActionList.as_view(), name="actionlist"),
    path("wish", views.WiskList.as_view(), name="wisklist"),
    path("action/<int:pk>", views.DetailsView.as_view(), name="actionlist"),
    # path("bid/create", views.BidCreate.as_view(), name="bidcreate"),
    path("action/create", views.ActionCreate.as_view(), name="actioncreate"),
    path("category", views.CategoryList.as_view(), name="categorylist"),
    path("category/<str:category>", views.CategoryTemp.as_view(), name="categorytemp"),
    # path("category/create", views.CategoryCreate.as_view(), name="categorycreate"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
