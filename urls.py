from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'timetable', views.TimeTableViewSet, basename='timetable')
router.register(r'meetings', views.MeetingSlotViewSet, basename='meetings')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('check-availability/', views.MeetingSlotViewSet.check_availability, name='check-availability'),
]