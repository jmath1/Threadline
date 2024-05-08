from django import forms
from django.contrib.gis import forms as gis_forms

from main.models import Profile


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)
    
class ProfileForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea, required=False)
    photo = forms.ImageField(required=False)
    coords = gis_forms.PointField(widget=gis_forms.OSMWidget(attrs={'map_width': 800, 'map_height': 500}))
    
    class Meta:
        model = Profile
        exclude = ["location_confirmed", "photo_url", "user_id"]