from django import forms

from .models import Main


class MainForm(forms.ModelForm):
    class Meta:
        model = Main
        fields = ['title', 'descrip']

    def __init__(self, *args, **kwargs):
        super(MainForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = "form-control"

        self.fields['title'].widget.attrs['placeholder'] = 'Title'
        self.fields['descrip'].widget.attrs['placeholder'] = 'Description'
