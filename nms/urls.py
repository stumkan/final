from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('tickets/create/', views.create_ticket, name='create_ticket'),
    path('tickets/<str:ticket_box>/', views.load_ticket_box, name='load_ticket_box'),
    path('tickets/<int:ticket_id>/details/', views.view_ticket, name='view_ticket'),
    path('tickets/<int:ticket_id>/add_comment/', views.add_comment, name='add_comment'),
    path('tickets/<int:ticket_id>/update/', views.update_ticket, name='update_ticket'),


    path('notes/listnotes/', views.list_notes, name='notes_list'),
    path('notes/<int:note_id>/details/', views.view_note, name='view_note'),
    path('notes/create/', views.create_note, name='create_note'),
    path('notes/<int:note_id>/edit/', views.edit_note, name='edit_note'),


    path('search/', views.search_tickets, name='search_tickets'),


    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
