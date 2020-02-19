import mimetypes
import os

from django.conf import settings
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404

from .models import WaveText
from .forms import WaveTextForm


def index(request):
    return render(request, "text_corrector/index.html")


def wave_list(request):
    wave_texts = WaveText.objects.all().order_by("name")[:50]
    paginator = Paginator(wave_texts, 3)
    page = request.GET.get("page")
    try:
        texts = paginator.page(page)
    except PageNotAnInteger:
        texts = paginator.page(1)
    except EmptyPage:
        texts = paginator.page(paginator.num_pages)
    return render(
        request,
        "text_corrector/wave_list.html",
        {"page": page, "texts": texts, "wave_texts": wave_texts},
    )


def wave_text_detail(request, pk):
    wave_text = get_object_or_404(WaveText, pk=pk)
    return render(
        request, "text_corrector/wave_text_detail.html", {"wave_text": wave_text}
    )


def wave_text_edit(request, pk):
    wave_text = get_object_or_404(WaveText, pk=pk)
    if request.method == "POST":
        form = WaveTextForm(request.POST, instance=wave_text)
        if form.is_valid():
            wave_text.modified = True
            wave_text = form.save(commit=False)
            wave_text.save()
            return redirect("text_corrector:wave_text_detail", pk=wave_text.pk)
    else:
        form = WaveTextForm(instance=wave_text)
    return render(
        request,
        "text_corrector/wave_text_edit.html",
        {"form": form, "wave_text": wave_text},
    )


def download_file(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path) + ".wav"
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
