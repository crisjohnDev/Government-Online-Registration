from django.urls import path
from . import views

urlpatterns = [
    path('add-barangay/', views.add_brgy, name="add_brgy"),
    path('brgy-list/', views.brgy_list, name="brgy_list"),
    path('delete-brgy/<int:pk>/', views.delete_brgy, name="delete-brgy")
]