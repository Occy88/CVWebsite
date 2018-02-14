from django import forms
from django.contrib.auth.models import User
from home.models import Group,Document, GroupComment, DocumentComment

class DocumentForm(forms.ModelForm):
    name = forms.CharField(label='Choose a name',max_length=50)
    docfile = forms.FileField(label='Select a file')

    class Meta:
        model=Document
        fields=[
            'name',
            'docfile'
        ]
    def save(self, commit=True):
        document = super().save(commit=False)
        if commit:
            document.save()
        return document
class DocumentCommentForm(forms.ModelForm):
    title = forms.CharField(label='title',max_length=100)
    comment = forms.CharField(label='comment', max_length=100)
    class Meta:
        model=DocumentComment
        fields=[
            'title',
            'comment'
        ]
    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()
        return instance

class GroupCommentForm(forms.ModelForm):
    title = forms.CharField(label='title', max_length=100)
    comment = forms.CharField(label='comment', max_length=100)
    class Meta:
        model = GroupComment
        fields = [
            'title',
            'comment'
        ]

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance
class GroupRegistrationForm(forms.ModelForm):
    name=forms.CharField(label='name',max_length=100)
    members=forms.ModelMultipleChoiceField(label='members:',widget=forms.CheckboxSelectMultiple(),queryset=User.objects.all())
    isLeader = forms.ModelMultipleChoiceField(label='isLeader:',widget=forms.CheckboxSelectMultiple(), queryset=User.objects.all())
    class Meta:
        model=Group
        fields=[
            'name',
            'members',
            'isLeader'
        ]
    def save(self, commit=True):
        group = super().save(commit=False)

        if commit:
            group.save()
            self.save_m2m()
        return group
