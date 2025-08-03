from rest_framework import serializers
from .models import ARTarget

class ARTargetSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    model_3d_url = serializers.SerializerMethodField()
    user_username = serializers.SerializerMethodField()

    class Meta:
        model = ARTarget
        fields = [
            'id', 'name', 'description', 'image', 'image_url',
            'model_3d', 'model_3d_url', 'is_uploaded_to_vuforia',
            'vuforia_target_id', 'vuforia_tracking_rating',
            'submitted_at', 'updated_at', 'user_username'
        ]
        read_only_fields = ['id', 'submitted_at', 'updated_at', 'is_uploaded_to_vuforia', 
                           'vuforia_target_id', 'vuforia_tracking_rating']

    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

    def get_model_3d_url(self, obj):
        if obj.model_3d:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.model_3d.url)
            return obj.model_3d.url
        return None

    def get_user_username(self, obj):
        return 'Anonymous'

class ARTargetCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ARTarget
        fields = ['name', 'description', 'image', 'model_3d'] 