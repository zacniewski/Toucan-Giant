from django.urls import path
from . import views

app_name = "text_corrector"

urlpatterns = [
    path("", views.index, name="index"),
    path("lista-wave-tekst", views.wave_list, name="wave_list"),
    path("wave-tekst/<int:pk>/edycja/", views.wave_text_edit, name="wave_text_edit"),
    path("wave-tekst/<int:pk>/", views.wave_text_detail, name="wave_text_detail"),
    path("download/<str:path>.wav/", views.download_file, name="download_file"),
]
