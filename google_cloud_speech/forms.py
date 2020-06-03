from django import forms


class TextForm(forms.Form):
    text = forms.CharField(label="Tekst do zamiany na mowę", max_length=250)
