from django.urls import path
from . import views
from users.views import login_injection_view
from users.views import query_injection_view


urlpatterns = [
    path('', views.home_view, name='home'), 
    path('login/', views.login_view, name='login'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('logout/', views.logout_view, name='logout'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('login-injection/', login_injection_view, name='login_injection'),
    path('query-injection/', query_injection_view, name='query_injection'),

]
print("🔗 Available URLs:")
print("http://127.0.0.1:8000/")
print("http://127.0.0.1:8000/login/")
print("http://127.0.0.1:8000/login-injection/")
print("http://127.0.0.1:8000/query-injection/")


