from django.urls import path

from . import views

urlpatterns = [
        path("", views.index, name="index"),
        path("login", views.login_view, name="login"),
        path("logout", views.logout_view, name="logout"),
        path("register", views.register, name="register"),
        path("publish", views.publish, name="publish"),
        path("auction/<str:numero>", views.oferta, name="oferta"),
        path("categories", views.categories, name="categories"),
        path("category/<str:category>", views.categoryselected, name="categoryselected"),
        path("watchlist", views.watchlist, name="watchlist")]
