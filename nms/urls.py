from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('tickets/create/', views.create_ticket, name='create_ticket'),
    path('tickets/<str:ticket_box>/', views.load_ticket_box, name='load_ticket_box'),
    path('tickets/<int:ticket_id>/details/', views.view_ticket, name='view_ticket'),
    path('tickets/<int:ticket_id>/add_comment/', views.add_comment, name='add_comment'),
    path('tickets/<int:ticket_id>/update/', views.update_ticket, name='update_ticket'),


    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
