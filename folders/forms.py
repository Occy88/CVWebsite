from django import forms

class DocumentForm(forms.Form):

    docfile = forms.FileField(
        label='Select a file',
    )
    class Meta:
        fields=[
            'docfile'

        ]
    docfile = forms.FileField(
        label='Select a file',
    )