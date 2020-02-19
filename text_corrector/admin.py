import os

from django.conf import settings
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path

from .models import WaveText, CsvFile


@admin.register(WaveText)
class WaveTextAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ["name"]
    ordering = ("name",)


@admin.register(CsvFile)
class CsvFileAdmin(admin.ModelAdmin):
    change_list_template = "admin/text_corrector_admin_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("fill_database_from_file/", self.fill_database_from_file),
            path("fill_file_from_database/", self.fill_file_from_database),
        ]
        return my_urls + urls

    def fill_database_from_file(self, request):
        self.message_user(request, "Czekaj, baza jest wypełniana danymi ...")
        plik_csv = CsvFile.objects.all()[:1][0]

        csv_generator = self.csv_reader_and_database_filler(str(plik_csv))
        row_count = 0
        for row in csv_generator:
            row_count += 1
        print(f"Liczba dodanych wierszy to {row_count}")

        self.message_user(request, f"Liczba dodanych wierszy: {row_count}")
        return HttpResponseRedirect("../../")

    def fill_file_from_database(self, request):
        self.message_user(request, "Czekaj, plik jest generowany ...")
        filename = "updated_metadata_m_full.csv"
        plik_csv = os.path.join(settings.MEDIA_ROOT, filename)
        print(plik_csv)
        qs = WaveText.objects.all()[:10]
        with open(plik_csv, "a") as f:
            f.seek(0)
            f.truncate()
            for record in qs:
                new_record = (
                    record.name
                    + "|"
                    + record.before_normalization
                    + "|"
                    + record.after_normalization
                    + "\n"
                )
                f.write(new_record)
        self.message_user(request, "Plik wygenerowany :)")
        return HttpResponseRedirect("../../")

    def csv_reader_and_database_filler(self, file_name):
        for row in open(file_name, "r"):
            podzielone = row.strip().split("|")
            new_record_from_wave = WaveText(
                name=podzielone[0],
                before_normalization=podzielone[1],
                after_normalization=podzielone[2],
            )
            new_record_from_wave.save()
            yield row
