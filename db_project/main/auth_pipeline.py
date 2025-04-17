from django.core.files.base import ContentFile
import requests
from social_core.exceptions import AuthException

def save_google_profile_picture(backend, user, response, details, *args, **kwargs):
    if backend.name != 'google-oauth2':
        return

    # Get the profile picture URL from the response
    picture_url = response.get('picture')
    if not picture_url:
        return
    
    user.photo_url = picture_url
    user.save()
