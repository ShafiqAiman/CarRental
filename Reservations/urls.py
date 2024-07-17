from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.homepage, name='homepage'),
    path('manage_cars/', views.manage_cars, name='manage_cars'),
    path('view_reservations/', views.view_reservations, name='view_reservations'),
    path('add_car/', views.add_car, name='add_car'),
    path('add_reservation/', views.add_reservation, name='add_reservation'),
    path('api/get_car_price/', views.get_car_price, name='get_car_price'),

    # Edit car URL
    path('edit-car/<int:car_id>/', views.edit_car, name='edit_car'),

    # Delete car URL
    path('delete-car/<int:car_id>/', views.delete_car, name='delete_car'),
    # path('view_feedbacks/', views.view_feedbacks, name='view_feedbacks'),
]