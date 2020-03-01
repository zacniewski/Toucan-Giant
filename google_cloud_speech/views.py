import mimetypes
import os

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

from google.cloud import texttospeech

from .forms import TextForm

"""Synthesizes speech from the input string of text or ssml.

Note: ssml must be well-formed according to:
    https://www.w3.org/TR/speech-synthesis/
"""


def text_to_speech(request):

    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    text = request.GET.get('results', 'To wartość domyślna!')
    print(text)

    synthesis_input = texttospeech.types.SynthesisInput(text=text)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.types.VoiceSelectionParams(
        language_code='pl-PL',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)

    # Select the type of audio file you want returned
    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.LINEAR16)

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(synthesis_input, voice, audio_config)

    # The response's audio_content is binary.
    file_path = settings.MEDIA_ROOT + '/output.wav'

    with open(file_path, 'wb') as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print('Audio content written to file "output.wav"')
    return render(request, "google_cloud_speech/text-to-speech.html", {'text': text})


def podaj_tekst(request):
    return render(request, 'google_cloud_speech/podaj_tekst.html')


def output_file(request):
    file_path = os.path.join(settings.MEDIA_ROOT) + "/output.wav"
    if os.path.exists(file_path):
        with open(file_path, "rb") as fh:
            mime_type, _ = mimetypes.guess_type(file_path)
            response = HttpResponse(fh.read(), content_type=mime_type)
            response["Content-Disposition"] = "inline; filename=" + os.path.basename(
                file_path
            )
            return response
        raise Http404("Nie ma takiego pliku!")
    else:
        return render(request, "text_corrector/404.html")
