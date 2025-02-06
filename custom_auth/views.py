import base64
from django.core.mail import send_mail
from django.contrib.auth.hashers import check_password, make_password
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import AuthModel
from .serializer import AuthModelSerializer
import random
import os
from dotenv import load_dotenv
from django.http import JsonResponse
from .utils import generate_token, extract_user

load_dotenv()

def generateCode():
    code = ''
    for _ in range(6):
        code += str(random.randint(0, 9))
    return code

@api_view(['POST'])
def signup(request):
    name = request.data['name']
    email = request.data['email']
    password = request.data['password']
    
    try:
        user = AuthModel.objects.get(email=email)
        return Response({'success': False, 'message': 'User already exists!'})
    except AuthModel.DoesNotExist:
        pass
        
    # encrypt password:     
    password = make_password(password)
    auth_model = AuthModel(name=name, email=email, password=password)

    # Generate Code
    code = generateCode()
    
    # send email
    send_mail(
        'Your Verification Code',
        f'Your verification code for Movie Ticket Booking App is {code} \n Please enter this code to verify your email within 5 minutes.',
        os.getenv('EMAIL_HOST_USER'),
        [email],
        fail_silently=False,
    )

    # encrypt code
    code = make_password(code)
    auth_model.code = code
    auth_model.save()
    token = generate_token(auth_model, 'temporary')

    
    serialized = AuthModelSerializer(auth_model).data
    
    return Response({
        'success': True,
        'message': 'User created successfully!',
        'user': serialized,
        'access_token': token,
    })

@api_view(['POST'])
def VerifyEmail(request):
    code = request.data['code']
    
    # check whether the token is expired or not
    user = extract_user(request)
    print(user)

    # check whether the code is valid or not
    user_id = user['user_id']
    try: 
        user = AuthModel.objects.get(id=user_id)
        if not check_password(code, user.code):
            return Response({'success': False, 'message': 'Invalid code!'})
        
    except AuthModel.DoesNotExist:
        # delete user since token is expired:
        user.delete()
        return Response({'success': False, 'message': 'User not found!'})

    # generate token:   
    token = generate_token(user, 'permanent')
    user.code = None
    user.save()

    return Response({'success': True, 'access_token': token, 'message': 'User verified successfully!'})

@api_view(['POST'])
def forgotPassword(request):
    email = request.data['email']

    try:
        user = AuthModel.objects.get(email=email)
        if user.code:
            return Response({'success': False, 'message': 'User not verified!'})
    except AuthModel.DoesNotExist:
        return Response({'success': False, 'message': 'User not found!'})

    # Generate Token:
    token = generate_token(user, 'temporary')

    # send email
    send_mail(
        'Reset Password',
        f'Click the link below to reset your password \n http://localhost:3000/reset-password/{token}',
        os.getenv('EMAIL_HOST_USER'),
        [email],
        fail_silently=False,
    )

    return Response({'success': True, 'token': token, 'message': 'Email sent successfully!'})

# to check token and update the forgot password: 
@api_view(['POST'])
def resetPassword(request):

    password = request.data['password']

    # check whether the token is expired or not
    user = extract_user(request)
    if not user:
        return Response({'success': False, 'message': 'Token expired!'})

    user = AuthModel.objects.get(id=user['user_id'])

    # create new password
    user.password = make_password(password)
    user.save()

    return Response({'success': True, 'message': 'Password reset successfully!'})
    

@api_view(['POST'])
def login(request):

    email = request.data['email']
    password = request.data['password']
    # decode password:
    try:
        user = AuthModel.objects.get(email=email)
    except AuthModel.DoesNotExist:
        return Response({'success': False, 'message': 'User not found!'})

    # check whether the user is verified or not:
    if user.code:
        return Response({'success': False, 'message': 'User not verified!'})

    # Verify the password using Django's check_password function
    if check_password(password, user.password):
        # Generate token
        token = generate_token(user, 'permanent')
        
        serialized = AuthModelSerializer(user).data
        return Response({
            'success': True,
            'message': 'Login successful!',
            'user': serialized,
            'access_token': token,
        })
    else:
        return Response({'success': False, 'message': 'Invalid password!'})

@api_view(['PATCH'])
def updateUser(request):
    user = extract_user(request)

    try:
        user = AuthModel.objects.get(id = user['user_id'])
    except AuthModel.DoesNotExist:
        return Response({'success': False, 'message': 'User not found!'})
    
    if 'name' not in request.data and 'password' not in request.data and 'image' not in request.data:
        return Response({'success': False, 'message': 'No data to update!'})
    
    name, password, image = None, None, None
    if 'name' in request.data:
        name = request.data['name']
    if 'password' in request.data:
        password = request.data['password']
    if 'image' in request.data:
        image = request.data['image']
        image_base64 = base64.b64encode(image.read()).decode('utf-8')
        image.seek(0)
   
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
    user = extract_user(request)

    try:
        user = AuthModel.objects.get(id = user['user_id'])
    except AuthModel.DoesNotExist:
        return Response({'success': False, 'message': 'User not found!'})
    
    user.delete()
    return Response({'message': 'User deleted successfully!'})