from django.db import models
from django.contrib.auth.models import User

class AppManagement(models.Model):
    name = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    apk_file_path = models.FileField(upload_to='apk/app/')
    first_screen_screenshot_path = models.ImageField(upload_to='apk/images/first_screen_screenshot_path/', null=True, blank=True, max_length=500)
    second_screen_screenshot_path = models.ImageField(upload_to='apk/images/second_screen_screenshot_path', null=True, blank=True, max_length=500)
    video_recording_path = models.FileField(upload_to='apk/video/', null=True, blank=True)
    ui_hierarchy = models.TextField(null=True, blank=True)
    screen_changed = models.BooleanField(default=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


