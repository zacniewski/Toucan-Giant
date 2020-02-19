from django.db import models


class WaveText(models.Model):
    name = models.CharField(max_length=100)
    before_normalization = models.TextField(max_length=300)
    after_normalization = models.CharField(max_length=300)
    modified = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Teksty w plikach wave"

    def __str__(self):
        return self.name


class CsvFile(models.Model):
    file_path = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Pliki CSV"

    def __str__(self):
        return self.file_path
