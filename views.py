from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from .models import FacultyProfile, TimeTable, MeetingSlot
from .serializers import (
    FacultyProfileSerializer,
    TimeTableSerializer,
    MeetingSlotSerializer
)
from django.http import HttpResponse

@csrf_exempt
@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    
    if user is not None:
        login(request, user)
        try:
            profile = FacultyProfile.objects.get(user=user)
            serializer = FacultyProfileSerializer(profile)
            return Response(serializer.data)
        except FacultyProfile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=404)
    return Response({'error': 'Invalid credentials'}, status=401)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request)
    return Response({'message': 'Logged out successfully'})

class TimeTableViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TimeTableSerializer
    
    def get_queryset(self):
        return TimeTable.objects.filter(faculty__user=self.request.user)

class MeetingSlotViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = MeetingSlotSerializer
    
    def get_queryset(self):
        return MeetingSlot.objects.filter(faculty__user=self.request.user)
    
    @api_view(['GET'])
    def check_availability(request):
        date = request.query_params.get('date')
        time = request.query_params.get('time')
        
        available_faculty = []
        faculty_profiles = FacultyProfile.objects.all()
        
        for profile in faculty_profiles:
            # Check if faculty has any timetable entry at this time
            has_class = TimeTable.objects.filter(
                faculty=profile,
                day=date.strftime('%A'),
                start_time__lte=time,
                end_time__gte=time
            ).exists()
            
            # Check if faculty has any meeting at this time
            has_meeting = MeetingSlot.objects.filter(
                faculty=profile,
                date=date,
                start_time__lte=time,
                end_time__gte=time,
                is_available=False
            ).exists()
            
            if not has_class and not has_meeting:
                available_faculty.append({
                    'username': profile.user.username,
                    'available': True
                })
            else:
                available_faculty.append({
                    'username': profile.user.username,
                    'available': False
                })
        
        return Response(available_faculty)
    
def index(request):
    return HttpResponse("Hello from Faculty Calendar API!")