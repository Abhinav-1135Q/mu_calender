from django.db import models
from django.contrib.auth.models import User

class FacultyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.URLField(blank=True)
    department = models.CharField(max_length=100)
    
    def __str__(self):
        return self.user.username

class TimeTable(models.Model):
    faculty = models.ForeignKey(FacultyProfile, on_delete=models.CASCADE)
    day = models.CharField(max_length=10)
    start_time = models.TimeField()
    end_time = models.TimeField()
    subject = models.CharField(max_length=100)
    
    class Meta:
        unique_together = ('faculty', 'day', 'start_time')

class MeetingSlot(models.Model):
    faculty = models.ForeignKey(FacultyProfile, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('faculty', 'date', 'start_time')