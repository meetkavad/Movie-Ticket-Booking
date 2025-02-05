from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

def extract_user(request):
    # getting auth from header
    token = request.headers['Authorization']
    if token is None:
        print("i ama here if,",token)
        return None
    try:
        print("i ama here in try ,",token)
        token = AccessToken(token)
        return token.payload
    except:
        print("i ama here in catch ,",token)
        return None
