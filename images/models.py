from django.db import models
from django.contrib.auth.models import User

def target_upload_path(instance, filename):
    return f'targets/{filename}'

def model3d_upload_path(instance, filename):
    return f'models_3d/{filename}'

class ARTarget(models.Model):
    # user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='ar_targets')
    
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    image = models.ImageField(upload_to=target_upload_path)
    model_3d = models.FileField(upload_to=model3d_upload_path, blank=True, null=True)

    is_uploaded_to_vuforia = models.BooleanField(default=False)
    vuforia_target_id = models.CharField(max_length=100, blank=True, null=True)
    vuforia_tracking_rating = models.IntegerField(blank=True, null=True)

    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - Anonymous"

    class Meta:
        ordering = ['-submitted_at']
