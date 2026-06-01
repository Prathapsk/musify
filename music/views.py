
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import Song, Playlist, EmailOTP
import random
import resend
import os


# RESEND API KEY
resend.api_key = os.getenv("RESEND_API_KEY")


# HOME
@login_required(login_url='/send-email-otp/')
def home(request, playlist_id=None):

    playlists = Playlist.objects.all()

    playlist_name = "All Songs"

    if playlist_id:

        selected_playlist = Playlist.objects.get(
            id=playlist_id
        )

        songs = selected_playlist.songs.all()

        playlist_name = selected_playlist.name

    else:

        songs = Song.objects.all()

    return render(request, 'home.html', {

        'songs': songs,

        'playlists': playlists,

        'playlist_name': playlist_name
    })


# SEND EMAIL OTP
def send_email_otp(request):

    if request.method == "POST":

        name = request.POST.get("name")

        email = request.POST.get("email")

        # DELETE OLD OTP
        EmailOTP.objects.filter(
            email=email
        ).delete()

        # NEW OTP
        otp = str(random.randint(100000, 999999))

        # SAVE OTP
        EmailOTP.objects.create(
            email=email,
            otp=otp
        )

        # SEND EMAIL USING RESEND
        resend.Emails.send({

            "from": "onboarding@resend.dev",

            "to": email,

            "subject": "Your Login OTP",

            "html": f"""

            <h2>Musify Login OTP</h2>

            <h1>{otp}</h1>

            <p>Your OTP is valid for 1 minute.</p>

            """
        })

        return render(request, 'verify_email_otp.html', {

            'email': email,

            'name': name
        })

    return render(request, 'email_otp.html')


# VERIFY EMAIL OTP
def verify_email_otp(request):

    if request.method == "POST":

        name = request.POST.get("name")

        email = request.POST.get("email")

        otp = request.POST.get("otp")

        check = EmailOTP.objects.filter(

            email=email,
            otp=otp

        ).last()

        if check:

            # OTP EXPIRY TIME
            expiry_time = (
                check.created_at
                + timedelta(minutes=1)
            )

            # CHECK EXPIRY
            if timezone.now() > expiry_time:

                messages.error(
                    request,
                    "OTP Expired"
                )

                return redirect(
                    '/send-email-otp/'
                )

            # CREATE USER
            user, created = User.objects.get_or_create(

                username=email,

                defaults={

                    'email': email,

                    'first_name': name
                }
            )

            user.first_name = name

            user.save()

            # LOGIN
            login(request, user)

            return redirect('/')

        else:

            messages.error(
                request,
                "Wrong OTP"
            )

            return redirect('/send-email-otp/')


# LOGOUT
def logout_user(request):

    logout(request)

    return redirect('/send-email-otp/')

