from django.urls import path
from . import views

app_name = "google_cloud_speech"

urlpatterns = [
    path("podaj-tekst", views.podaj_tekst, name="podaj_tekst"),
    path("text-to-speech/", views.text_to_speech, name="text_to_speech"),
    path("voice-files/", views.voice_files, name="voice_files"),
    path("load-voice-file/<str:path>/", views.load_voice_file, name="load_voice_file"),
    path("examine-voice-file/<str:text>", views.output_file, name="output_file"),
    path("speech-to-text/<str:local_file_path>/", views.speech_to_text, name="speech_to_text"),
]
