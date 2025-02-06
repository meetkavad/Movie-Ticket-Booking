from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from datetime import timedelta
from rest_framework_simplejwt.tokens import AccessToken

class PermanentAccessToken(AccessToken):
    lifetime = timedelta(days=31)

class TemporaryAccessToken(AccessToken):
    lifetime = timedelta(minutes=5)

def generate_token(user, type):
    if type == 'permanent':
        token = PermanentAccessToken.for_user(user)
        return str(token)
    elif type == 'temporary':
        token = TemporaryAccessToken.for_user(user)
        return str(token)
    else:
        return None

def extract_user(request):
    # getting auth from header
    token = request.headers['Authorization']
    if token is None:
        return None
    
    token = AccessToken(token)
    return token.payload

