from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listings/<str:list_title>", views.listings, name="listings"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("category/<str:category>", views.listed_category, name="listed_category"),
    path("delete/<str:name>", views.delete, name="delete"),
    path("comment/<str:item_name>", views.comment, name="comment"),
    path("add/<str:user>", views.add, name="add"),
    path("bid", views.bid, name="bid"),
    path("close", views.close, name="close"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
