from django import forms
from django.contrib.auth.models import User
from home.models import Group, Membership
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

class GroupRegistrationForm(forms.ModelForm):
    leader=forms.EmailField(max_length=100,required=True)

    members=forms.ModelMultipleChoiceField(queryset=User.objects.all())
    def __init__(self,*args,**kwargs):
        if kwargs.get('instance'):
            # We get the 'initial' keyword argument or initialize it
            # as a dict if it didn't exist.
            initial = kwargs.setdefault('initial', {})
            # The widget for a ModelMultipleChoiceField expects
            # a list of primary key for the selected data.
            initial['members'] = [m.pk for m in kwargs['instance'].member_set.all()]

        forms.ModelForm.__init__(self, *args, **kwargs)

    def save(self, commit=True):
        # Get the unsave Pizza instance
        instance = forms.ModelForm.save(self, False)

        # Prepare a 'save_m2m' method for the form,
        old_save_m2m = self.save_m2m

        def save_m2m():
            old_save_m2m()
            # This is where we actually link the pizza with toppings
            instance.members_set.clear()
            for member in self.cleaned_data['members']:
                instance.member_set.add(member)

        self.save_m2m = save_m2m

        # Do we need to save all changes now?
        if commit:
            instance.save()
            self.save_m2m()

        return instance