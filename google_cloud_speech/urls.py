from django.urls import path
from . import views

app_name = "google_cloud_speech"

urlpatterns = [
    path("podaj-tekst", views.podaj_tekst, name="podaj_tekst"),
    path("tekst-to-speech/", views.text_to_speech, name="text_to_speech"),
    path("download-voice-file/", views.output_file, name="output_file"),
]
