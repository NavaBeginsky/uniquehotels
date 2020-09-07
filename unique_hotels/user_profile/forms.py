from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django import forms
from .models import UserProfilePic

class UpdateUserForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = None

class UpdatePictureForm(forms.ModelForm):
    profile_pic = forms.ImageField(error_messages = {'invalid':("Image files only")}, widget=forms.FileInput)

    class Meta:
        model = UserProfilePic
        fields = ['profile_pic']


class ChangePassword(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["new_password1"].help_text = None