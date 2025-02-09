from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from .models import User
from .models import Movie
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .serializers import MovieSerializer

def normalize_phone(phone):
    """ Convert phone number to a consistent format (e.g., +639123456789) """
    phone = phone.replace(" ", "").replace("-", "") 
    if phone.startswith("+63"):  
        return phone  
    elif phone.startswith("09"):  
        return "+63" + phone[1:]  
    elif phone.startswith("9") and len(phone) == 10:  
        return "+63" + phone  
    return phone  

@csrf_exempt
@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        fullName = request.data.get('fullName', None)
        email = request.data.get('email', None)
        phoneNumber = request.data.get('phoneNumber', None)
        password = request.data.get('password', None)

        if not fullName or not password or (not email and not phoneNumber):
            return JsonResponse({'error': 'Full name, password, and either email or phone number are required'}, status=400)
        
        if phoneNumber:
            phoneNumber = normalize_phone(phoneNumber)  # Normalize before saving
        
        user = User.objects.create_user(
            fullName=fullName,
            email=email,
            phoneNumber=phoneNumber,
            password=password 
        )
        return JsonResponse({'message': 'User registered successfully'}, status=201)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
@api_view(['POST'])
def login_view(request):
    
    print("Raw request body:", request.body)  # Debugging
    print("Parsed request data:", request.data)  # Debugging

    if request.method == 'POST':
        identifier = request.data.get('identifier', None)
        password = request.data.get('password', None)

        print("Received identifier:", identifier)
        print("Received password:", password)

        if not identifier or not password:
            return JsonResponse({'error': 'Identifier (email or phone) and password are required'}, status=400)

        user = User.objects.filter(email=identifier).first()

        if not user:
            normalized_phone = normalize_phone(identifier)
            user = User.objects.filter(phoneNumber=normalized_phone).first()

        if user and user.check_password(password):
            token, created = Token.objects.get_or_create(user=user)
            return JsonResponse({'message': 'Login successful', 'token': token.key}, status=200)

        return JsonResponse({'error': 'Invalid credentials'}, status=401)
        
    return JsonResponse({'error': 'Invalid request method'}, status=405)


@api_view(['GET'])
def movie_list(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_movie(request):
    if request.user.role != 'admin': 
        return Response({'error': 'You do not have permission to add movies'}, status=403)

    serializer = MovieSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)