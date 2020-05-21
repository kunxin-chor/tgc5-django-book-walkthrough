from django import forms
from accounts.models import Profile
from django.contrib.auth.models import Group


class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    address = forms.CharField(max_length=255)

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        profile = Profile()
        profile.address = self.cleaned_data['address']
        user.save()

        # save the profile
        profile.user = user
        profile.save()

        # add the user to group
        customer_group = Group.objects.get(name="customer")
        customer_group.user_set.add(user)
