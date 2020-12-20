from django.urls import path
from api import views
from django.conf.urls import include

urlpatterns = [
    path("register/", views.UserCreate.as_view()),
    path("login/", views.signin, name="signin"),
    path("details/<int:pk>/", views.UserDetails),
    path("new/<int:pk>/", views.FavouriteAdd),
    path("delete/<int:pk>/", views.FavouriteDelete),
]