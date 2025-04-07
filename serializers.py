from rest_framework import serializers
from django.contrib.auth.models import User
from .models import FacultyProfile, TimeTable, MeetingSlot

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class FacultyProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = FacultyProfile
        fields = '__all__'

class TimeTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeTable
        fields = '__all__'

class MeetingSlotSerializer(serializers.ModelSerializer):
    faculty_name = serializers.CharField(source='faculty.user.username', read_only=True)
    
    class Meta:
        model = MeetingSlot
        fields = '__all__'