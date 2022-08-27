from unicodedata import name
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name='create_listing'),
    path('listing_info/<int:pk>', views.listing_info, name='listing_info'),
    path('watchlist', views.watchlist, name='watchlist'),
    path('category_list', views.category_list, name='category_list'),
    path('category/<str:category>', views.category, name='category'),
    path('comments/<int:pk>', views.comments, name="comments"),
    path('delete_listing/<int:pk>', views.delete_listing, name="delete_listing"),
    path('close_listing/<int:pk>', views.close_listing, name="close_listing"),
    path('bid_listing/<int:pk>', views.bid_listing, name="bid_listing"),
    path('delete_watchlist/<int:pk>', views.delete_watchlist, name="delete_watchlist"),
]
