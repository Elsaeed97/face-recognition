from django.urls import path
from . import views 
from django.contrib.auth import views as auth_views

urlpatterns = [
	path('', views.index,name='index'),
	path('register/',views.register,name='register'),
	path('login/',views.login_user,name='login'),
	# path('login/', auth_views.LoginView.as_view(), name='login'),
	# path('login/face-match/' ,views.face ,name='face'),
	path('profile/',views.profile ,name='profile'),
	path('logout/', auth_views.LogoutView.as_view(), name='logout'),
] 

