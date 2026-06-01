import json

from django.contrib import admin
from django.http import JsonResponse
from django.urls import path

from .models import Song, Playlist, EmailOTP


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):

    list_display = ['title', 'artist']


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):

    list_display = ['name', 'user']

    filter_horizontal = ['songs']

    change_form_template = "admin/playlist_change_form.html"

    def get_urls(self):

        urls = super().get_urls()

        custom_urls = [

            path(
                '<int:playlist_id>/delete-selected-songs/',
                self.admin_site.admin_view(
                    self.delete_selected_songs
                ),
                name='delete_selected_songs',
            ),

        ]

        return custom_urls + urls

    def delete_selected_songs(self, request, playlist_id):

        if request.method == "POST":

            data = json.loads(request.body)

            song_ids = data.get("songs", [])

            Song.objects.filter(
                id__in=song_ids
            ).delete()

            return JsonResponse({
                "status": "success"
            })

        return JsonResponse({
            "status": "failed"
        })


admin.site.register(EmailOTP)