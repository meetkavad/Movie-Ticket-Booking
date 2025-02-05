import base64
from django.core.mail import send_mail
from django.contrib.auth.hashers import check_password, make_password
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import AuthModel
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import AuthModelSerializer
import random
import os
from dotenv import load_dotenv
from django.http import JsonResponse
from .utils import extract_user

load_dotenv()

def generateCode():
    code = 0
    for _ in range(6):
        code = code * 10 + random.randint(0, 9)
    return code

@api_view(['POST'])
def signup(request):
    name = request.data['name']
    email = request.data['email']
    password = request.data['password']
    
    # checking if user alreay exists
    try:
        user = AuthModel.objects.get(email=email)
        return Response({'success': False, 'message': 'User already exists!'})
    except AuthModel.DoesNotExist:
    # Proceed with user creation or other logic
        pass
        
    # encrypt password:     
    password = make_password(password)
    auth_model = AuthModel(name=name, email=email, password=password)

    # Generate Code
    code = generateCode()
    
    # send email
    send_mail(
        'Your Verification Code',
        f'Your verification code for Movie Ticket Booking App is {code}',
        os.getenv('EMAIL_HOST_USER'),
        [email],
        fail_silently=False,
    )

    # encrypt code
    code = make_password(str(code))
    auth_model.code = code
    
    auth_model.save()

    # Generate token
    refresh = RefreshToken.for_user(auth_model)
    access_token = str(refresh.access_token)
    
    serialized = AuthModelSerializer(auth_model).data
    
    return Response({
        'success': True,
        'message': 'User created successfully!',
        'user': serialized,
        'access_token': access_token,
        'refresh_token': str(refresh)
    })

@api_view(['POST'])
def VerifyEmail(request):
    user = extract_user(request)
    
    print(user)
    return JsonResponse({'message': 'User verified successfully!'})

# @api_view(['POST'])
# def emailVerify()

@api_view(['POST'])
def login(request):
    email = request.data['email']
    password = request.data['password']
    # decode password:
    try:
        user = AuthModel.objects.get(email=email)
    except AuthModel.DoesNotExist:
        return Response({'success': False, 'message': 'User not found!'})

    # Verify the password using Django's check_password function
    if check_password(password, user.password):
        # Generate token
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        
        serialized = AuthModelSerializer(user).data
        return Response({
            'success': True,
            'message': 'Login successful!',
            'user': serialized,
            'access_token': access_token,
            'refresh_token': str(refresh)
        })
    else:
        return Response({'success': False, 'message': 'Invalid password!'})

@api_view(['PATCH'])
def updateUser(request):
    id = request.data['id']
    if 'name' not in request.data and 'password' not in request.data and 'image' not in request.data:
        return Response({'success': False, 'message': 'No data to update!'})
    
    if 'name' in request.data:
        name = request.data['name']
    if 'password' in request.data:
        password = request.data['password']
    if 'image' in request.data:
        image = request.data['image']
    image_base64 = base64.b64encode(image.read()).decode('utf-8')
    image.seek(0)

    try:
        user = AuthModel.objects.get(id = id)
    except AuthModel.DoesNotExist:
        return Response({'success': False, 'message': 'User not found!'})

    if name:
        user.name = name
    if password:
        user.password = make_password(password)
    if image:
        user.image_base64 = image_base64

    user.save()
    
    serialized = AuthModelSerializer(user).data
    
    return Response({'success': True, 'message': 'User updated successfully!', 'user': serialized})

@api_view(['DELETE'])   
def deleteUser(request):
    userId = request.data['userId']
    user = AuthModel.objects.get(id=userId)
    user.delete()
    return Response({'message': 'User deleted successfully!'})