from django.urls import path
from Main import views
app_name = 'search365'
urlpatterns = [
    path('', views.entrys.as_view(), name='main'),
    path('search/', views.entrys.as_view(), name='search_results'),
    path('new_entry/', views.new_entry, name='new_entry'),
    path('edit_entry/<int:pk>/', views.edit_entry, name='edit_entry'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('upload_csv/', views.upload_csv, name='upload_csv'),
]
