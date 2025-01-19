from django.shortcuts import render
import base64
from django.core.files.base import ContentFile
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import AuthModel

@api_view(['POST'])
def upload_image(request):
    name = request.data['name']
    email = request.data['email']
    password = request.data['password']
    image = request.data['image']
    image_base64 = base64.b64encode(image.read()).decode('utf-8')
    print(image_base64)
    image.seek(0)
    auth_model = AuthModel(name=name, email=email, password=password, image_base64=image_base64)
    auth_model.save()
    return Response({'message': 'Image uploaded successfully!'})
# Compare this snippet from ticket_booking_backend/auth/serializers.py: 

