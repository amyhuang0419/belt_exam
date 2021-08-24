from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('success', views.login_success),
    path('logout', views.logout),
    path('quotes', views.quotes_dashboard),
    path('quotes/create', views.create_quote),
    # path('quotes/empty', views.entry_empty),
    path('favorite/<int:quote_id>', views.favorite_quote),
    path('unfavorite/<int:quote_id>', views.unfavorite_quote),
    path('quotes/<int:quote_id>/delete', views.delete),
    path('quotes/<int:quote_id>/edit', views.edit),
    path('quotes/<int:quote_id>/update', views.update),
    path('users/<int:user_id>', views.user_details)
]