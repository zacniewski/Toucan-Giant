import glob
import io
import mimetypes
import os

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

from google.cloud import texttospeech
from google.cloud import speech_v1
from google.cloud.speech_v1 import enums
from slugify import slugify

from .forms import TextForm

"""Synthesizes speech from the input string of text or ssml.

Note: ssml must be well-formed according to:
    https://www.w3.org/TR/speech-synthesis/
"""


def text_to_speech(request):

    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    text = request.GET.get("results", "To wartość domyślna!")
    print(text)

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code="pl-PL", ssml_gender=texttospeech.SsmlVoiceGender.MALE
    )
    voices = client.list_voices(request={"language_code": "pl"})

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    # response = client.synthesize_speech(synthesis_input, voice, audio_config)
    response = client.synthesize_speech(
        request={
            "input": synthesis_input,
            "voice": voice,
            "audio_config": audio_config
        }
    )

    # The response's audio_content is binary.
    slug_text = slugify(text)
    if len(slug_text) < 20:
        slug_text = slug_text + (20 - len(slug_text)) * "_"
    else:
        slug_text = slug_text[:20]
    file_path = settings.MEDIA_ROOT + "/" + slug_text + ".wav"

    with open(file_path, "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print(f'Audio content written to file {slug_text}.wav"')
    return render(
        request,
        "google_cloud_speech/text-to-speech.html",
        {"text": text, "slug_text": slug_text},
    )


def podaj_tekst(request):
    return render(request, "google_cloud_speech/podaj_tekst.html")


def output_file(request, text):
    file_path = os.path.join(settings.MEDIA_ROOT) + "/" + text + ".wav"
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


def voice_files(request):
    voice_files_list = []
    dir_path = settings.MEDIA_ROOT
    for full_path in glob.iglob(dir_path + '/' + '*.wav'):
        voice_files_list.append([os.path.basename(full_path), os.path.basename(full_path)[:-4]])
    return render(request, "google_cloud_speech/voice-files.html", {'voice_files_list': voice_files_list})


def load_voice_file(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
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


def speech_to_text(request, local_file_path):
    """
    Transcribe a short audio file using synchronous speech recognition

    Args:
      local_file_path Path to local audio file, e.g. /path/audio.wav
    """

    client = speech_v1.SpeechClient()

    # local_file_path = 'resources/brooklyn_bridge.raw'

    # The language of the supplied audio
    language_code = "pl-PL"

    # Sample rate in Hertz of the audio data sent
    sample_rate_hertz = 24000  # było 16000

    # Encoding of audio data sent. This sample sets this explicitly.
    # This field is optional for FLAC and WAV audio formats.
    encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16
    config = {
        "language_code": language_code,
        # "sample_rate_hertz": sample_rate_hertz,
        "encoding": encoding,
    }
    local_full_path = settings.MEDIA_ROOT + '/' + local_file_path
    local_file_name = local_file_path[:-4]
    with io.open(local_full_path, "rb") as f:
        content = f.read()
    audio = {"content": content}

    response = client.recognize(config, audio)
    for result in response.results:
        # First alternative is the most probable result
        alternative = result.alternatives[0]
        print(u"Transcript: {}".format(alternative.transcript))
        print(u"Confidence: {}".format(alternative.confidence))

    return render(
        request,
        "google_cloud_speech/speech-to-text.html",
        {"text": alternative.transcript,
         'confidence': alternative.confidence,
         'local_file_name': local_file_name},
    )
