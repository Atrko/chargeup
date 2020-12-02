from django import forms
from .models import User

class ImageForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['profile_pic']

class UpdateImageForm(forms.ModelForm):
    # profile_pic = forms.ImageField(null=True, blank=True, upload_to='images/')

    class Meta:
        model = User
        fields = ['profile_pic']
        exclude = ['email']


