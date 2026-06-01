from django.db import models
from django.contrib.auth.models import User


class Song(models.Model):

    title = models.CharField(max_length=100)

    artist = models.CharField(max_length=100)

    cover_image = models.ImageField(
        upload_to='covers/'
    )

    audio_file = models.FileField(
        upload_to='songs/'
    )

    def __str__(self):

        return self.title


class Playlist(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=100)

    songs = models.ManyToManyField(
        Song,
        blank=True
    )

    def __str__(self):

        return self.name


# EMAIL OTP MODEL
class EmailOTP(models.Model):

    email = models.EmailField()

    otp = models.CharField(max_length=6)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.email