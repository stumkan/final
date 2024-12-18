from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('tickets/create/', views.create_ticket, name='create_ticket'),
    path('tickets/active/', views.active_and_outstanding_tickets, name='active_outstanding_tickets'),

    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
