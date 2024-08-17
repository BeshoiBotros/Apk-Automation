from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.HomeView.as_view(), name='home'),
    path('home/app/delete/<int:pk>/', views.delete_app, name='home-delete-app'),
    path('home/app/update/<int:pk>/', views.update_app, name='update_app'),
    path('home/app/run/<int:pk>/', views.run_app, name="run_app")
]