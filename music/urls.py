from django.urls import path

from music import views


urlpatterns = [

    path('', views.home),

    path(
        'playlist/<int:playlist_id>/',
        views.home
    ),

    path('logout/', views.logout_user),

    # EMAIL OTP LOGIN
    path(
        'send-email-otp/',
        views.send_email_otp
    ),

    path(
        'verify-email-otp/',
        views.verify_email_otp
    ),

]