from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.models import User
from .models import ARTarget
from .serializers import ARTargetSerializer, ARTargetCreateSerializer

class ARTargetViewSet(viewsets.ModelViewSet):
    queryset = ARTarget.objects.all()
    serializer_class = ARTargetSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_serializer_class(self):
        if self.action == 'create':
            return ARTargetCreateSerializer
        return ARTargetSerializer

    def perform_create(self, serializer):
        # Create without user authentication for testing
        serializer.save()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        print("Sending targets data:", serializer.data)  # Debug
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def upload_to_vuforia(self, request, pk=None):
        """Simulate uploading to Vuforia"""
        target = self.get_object()
        target.is_uploaded_to_vuforia = True
        target.vuforia_target_id = f"vuforia_{target.id}"
        target.vuforia_tracking_rating = 85  # Simulated rating
        target.save()
        
        serializer = self.get_serializer(target, context={'request': request})
        return Response({
            'message': 'Successfully uploaded to Vuforia',
            'target': serializer.data
        })

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get statistics about AR targets"""
        total_targets = ARTarget.objects.count()
        uploaded_to_vuforia = ARTarget.objects.filter(is_uploaded_to_vuforia=True).count()
        
        return Response({
            'total_targets': total_targets,
            'uploaded_to_vuforia': uploaded_to_vuforia,
            'pending_upload': total_targets - uploaded_to_vuforia
        })
    
    @action(detail=False, methods=['get'], url_path='by-name/(?P<name>[^/.]+)')
    def target_by_name(self, request, name=None):
        try:
            target = ARTarget.objects.get(name=name)
            serializer = self.get_serializer(target, context={'request': request})
            return Response(serializer.data)
        except ARTarget.DoesNotExist:
            return Response({"error": "Target not found"}, status=404)