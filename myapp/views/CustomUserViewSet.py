from django.contrib import messages
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response
from myapp.models.CustomUser import CustomUser
from myapp.serializers.CustomUserSerializer import CustomUserSerializer
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.contrib.auth import logout
from django.contrib.auth import logout as django_logout



class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    @csrf_exempt
    @action(detail=False, methods=['get', 'post'], url_path='register')
    def register_user(self, request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            email = request.POST.get('email')
            contact_number = request.POST.get('contact_number')
            role = request.POST.get('role')

            if not username or not password or not email:
                return render(request, 'register.html', {
                    'error': "Username, password, and email are required."
                })

            if password != confirm_password:
                return render(request, 'register.html', {
                    'error': "Password and Confirm Password do not match."
                })

            if CustomUser.objects.filter(username=username).exists():
                return render(request, 'register.html', {
                    'error': f"Username '{username}' is already taken."
                })

            hashed_password = make_password(password)

            CustomUser.objects.create(
                username=username,
                password=hashed_password,
                email=email,
                contact_number=contact_number,
                role=role
            )
            return render(request, 'register.html', {
                'success': f"User '{username}' registered successfully!"
            })

        return render(request, 'register.html')
    
    @csrf_exempt
    @action(detail=False, methods=['get', 'post'], url_path='login')
    def login(self, request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            try:
                user = CustomUser.objects.get(username=username)
                if check_password(password, user.password):
                    request.session['user_id'] = user.id   #<==Here Im saving the logged-in user's id for future validation(admin or user)
                    messages.success(request, f"Welcome, {user.username}")
                    return redirect('/api/users/dashboard/') 
                else:
                    messages.error(request, "Invalid password")
                    return render(request, 'login.html')
            except CustomUser.DoesNotExist:
                messages.error(request, "User not found")
                return render(request, 'login.html')
        
        return render(request, 'login.html')
    
    @csrf_exempt
    @action(detail=False, methods=['post'], url_path='logout')
    def logout(self, request):
        django_logout(request)  # properly clears session
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
    
    
    @csrf_exempt
    @action(detail=False, methods=['get'], url_path='get_logged_in_user_id')
    def get_logged_in_user_id(self, request):
        user_id = request.session.get('user_id')
        if user_id:
            return JsonResponse({'user_id': user_id})
        else:
            return JsonResponse({'error': 'User not logged in'}, status=401)
        
    @csrf_exempt
    @action(detail=False, methods=['get'], url_path='profile_page')    
    def profile_page(self,request):
        return render(request, 'profile.html')
    
    @csrf_exempt
    @action(detail=False, methods=['get'], url_path='dashboard')    
    def dashboard(self,request):
        return render(request, 'dashboard.html')
    

