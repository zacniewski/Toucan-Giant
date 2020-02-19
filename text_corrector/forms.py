from django import forms

from .models import WaveText


class WaveTextForm(forms.ModelForm):
    class Meta:
        model = WaveText
        fields = ("before_normalization",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['before_normalization'].widget.attrs.update(rows='4')
