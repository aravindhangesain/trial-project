from django.contrib import messages
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response
from myapp.models.UserApps import UserApps
from myapp.models.App import App
from myapp.models.CustomUser import CustomUser
from myapp.serializers.AppSerializer import AppSerializer
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

class AppViewSet(viewsets.ModelViewSet):

    queryset=App.objects.all()
    serializer_class=AppSerializer

    @csrf_exempt
    @action(detail=False, methods=['get', 'post'], url_path='add_app')
    def add_app(self, request):
        if request.method == 'POST':
            name = request.data.get('name')
            publisher = request.data.get('publisher')
            app_logo = request.data.get('app_logo')
            points = request.data.get('points')

            
            user_id = request.session.get('user_id')
            if not user_id:
                return Response({'detail': 'User not logged in'}, status=status.HTTP_401_UNAUTHORIZED)

            try:
                #I'm only allowing admin users to add a new apps and
                # since I can use permission_classes only if I have inbuilt django user admin I'm Validating manually here.
                valid_user = CustomUser.objects.get(id=user_id,role='Admin')      
            except CustomUser.DoesNotExist:
                return Response({'detail': 'Invalid user in session'}, status=status.HTTP_400_BAD_REQUEST)

            
            app = App.objects.create(
                name=name,
                publisher=publisher,
                app_logo=app_logo,
                points=points,
                user=valid_user 
            )

            # serializer = AppSerializer(app)
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
            return render(request, 'dashboard.html')

        return Response({'detail': 'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    @csrf_exempt
    @action(detail=False, methods=['get', 'post'], url_path='add_app_form')
    def add_app_form(self, request):

        return render(request,'add_app.html')
    
    @csrf_exempt
    @action(detail=False, methods=['get', 'post'], url_path='verify_installation')
    def verify_installation(self, request):
        if request.method=='POST':
            user_id=request.data.get('user_id')
            app_id=request.data.get('app_id')
            screenshots=request.data.get('screenshots')

            installed_app_data=App.objects.get(id=app_id)

            if installed_app_data is not None:
                # Validating for null values
                if screenshots is not None:                                 
                    UserApps.objects.create(user_id=user_id,app_id=app_id,screenshots=screenshots)  # Adding User and installed apps in a separate table

                    user=CustomUser.objects.get(id=user_id)
                    current_points=user.points                        #Getting existing points
                    if current_points is None:
                        current_points=0
                        current_points+=installed_app_data.points         #Adding intalled app's points to existing 
                        user.points=current_points
                        user.save()                                       #Saving the new balence
                        return Response({'detail':'Installation Verified, Please visit your profile for checking out the received rewards'},status=status.HTTP_201_CREATED)
                    else:
                        current_points+=installed_app_data.points         #Adding intalled app's points to existing points
                        user.points=current_points
                        user.save()                                       #Saving the new balence
                        return Response({'detail':'Installation Verified, Please visit your profile for checking out the received rewards'},status=status.HTTP_201_CREATED)

                else:
                    return Response({'detail': 'Please Upload Screenshot'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'detail': 'Invalid App'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    @csrf_exempt
    @action(detail=False, methods=['get', 'post'], url_path='verify_installation_form')
    def verify_installation_form(self, request):
        return render(request, 'verify_installation.html')
    
    @csrf_exempt
    @action(detail=False, methods=['get'], url_path='app_profile_page')
    def app_profile_page(self,request):
        return render(request, 'app_profile.html')
    
    @csrf_exempt
    @action(detail=False, methods=['post', 'get'], url_path='verified_apps')
    def verified_apps(self, request):
        
        user_id = request.data.get('user_id') if request.method == 'POST' else request.query_params.get('user_id')

        if not user_id:
            return Response({'error': 'User ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        
        app_ids = UserApps.objects.filter(user_id=user_id).values_list('app_id', flat=True)

        
        

        
        user_app_data = App.objects.filter(id__in=app_ids)

        
        serializer = AppSerializer(user_app_data, many=True)
        return Response(serializer.data)
    
    @csrf_exempt
    @action(detail=False, methods=['post', 'get'], url_path='my_apps_page')
    def my_apps_page(self, request):
        return render(request, 'my_apps.html')




                
                


    



    