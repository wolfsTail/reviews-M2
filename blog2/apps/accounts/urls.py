from django.urls import path

from .views import ProfileUpdateView, ProfileDetailView, UserLogoutView,\
    UserLoginView, UserRegisterView, UserPasswordResetView, UserPasswordResetDoneView,\
    UserPasswordResetConfirmView, UserPasswordResetCompleteView




urlpatterns = [
    path('user/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
    path('user/<str:slug>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('password-reset/', UserPasswordResetView.as_view(), name='password-reset'),
    path('password-reset/done/', UserPasswordResetDoneView.as_view(), name='password-reset-done'),
    path('password-reset/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(),\
         name='password_reset_confirm'),
    path('password-reset/complete/', UserPasswordResetCompleteView.as_view(), \
         name='password_reset_complete')
]