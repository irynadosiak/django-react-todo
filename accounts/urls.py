from django.urls import path
from knox import views as knox_views
from accounts.views import RegisterView
from accounts.views import LoginView
from accounts.views import UserView

urlpatterns = [
    path('api/auth/register', RegisterView.as_view()),
    path('api/auth/login', LoginView.as_view()),
    path('api/auth/user', UserView.as_view()),
    path('api/auth/logout', knox_views.LogoutView.as_view(), name='knox_logout'),
]
