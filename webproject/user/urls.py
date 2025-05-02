from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'user'

urlpatterns = [
    path('login/',auth_views.LoginView.as_view(template_name = "login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/',views.signup, name='signup'),
    path('normalSignupForm/',views.normalSignupForm,name="normalSignupForm"),
    path('enterpriseSignupForm',views.enterpriseSignupForm, name="enterpriseSignupForm"),
    path('editInfo/', views.editInfo, name='editInfo'),
    path('editPw/', views.editPw, name='editPw'),
    path('myPage/',views.myPage, name='myPage'),
]