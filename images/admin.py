from django.contrib import admin
from .models import ARTarget

@admin.register(ARTarget)
class ARTargetAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_uploaded_to_vuforia', 'vuforia_target_id', 'submitted_at']
    list_filter = ['is_uploaded_to_vuforia', 'submitted_at']
    search_fields = ['name', 'description']
    readonly_fields = ['submitted_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description')
        }),
        ('Files', {
            'fields': ('image', 'model_3d')
        }),
        ('Vuforia Integration', {
            'fields': ('is_uploaded_to_vuforia', 'vuforia_target_id', 'vuforia_tracking_rating')
        }),
        ('Timestamps', {
            'fields': ('submitted_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
