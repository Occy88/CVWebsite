from django import forms
from django.contrib.auth.models import User
from home.models import Group,Document

class DocumentForm(forms.ModelForm):
    docfile = forms.FileField(label='Select a file')

    class Meta:
        model=Document
        fields=[
            'docfile'
        ]
    def save(self, commit=True):
        document = super().save(commit=False)
        if commit:
            document.save()
        return document

class GroupRegistrationForm(forms.ModelForm):
    name=forms.CharField(label='name',max_length=100)
    members=forms.ModelMultipleChoiceField(label='members:',queryset=User.objects.all())
    class Meta:
        model=Group
        fields=[
            'name',
            'members'
        ]
    def save(self, commit=True):
        group = super().save(commit=False)

        if commit:
            group.save()
            self.save_m2m()
        return group
