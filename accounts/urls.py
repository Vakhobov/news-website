from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView, LogoutView, \
     PasswordChangeView, PasswordChangeDoneView, PasswordResetView, \
        PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    # path('login/', LoginView.as_view(), name='login'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    path('password-change/', PasswordChangeView.as_view(), name='password_change'),
    path('password-change-done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('passwprd-reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('profile/', dashboard_view, name='user_profile'),
    path('signup/', user_register, name='user_register'),
    # path('signup/', SignUpView.as_view(), name='user_register'),
    path('profile/edit/', edit_user, name='edit_user_information'),
    # path('profile/edit/', EditUserView.as_view(), name='edit_user_information'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
