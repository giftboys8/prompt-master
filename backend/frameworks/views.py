from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination
from .models import Framework, FrameworkModule
from .serializers import FrameworkSerializer, FrameworkCreateSerializer, FrameworkModuleSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class FrameworkViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Framework.objects.all()
    pagination_class = StandardResultsSetPagination
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return FrameworkCreateSerializer
        return FrameworkSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        with_modules = self.request.query_params.get('with_modules', '').lower() == 'true'
        
        if with_modules:
            queryset = queryset.prefetch_related('modules')
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        """
        重写list方法，处理with_modules参数
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def modules(self, request, pk=None):
        framework = self.get_object()
        modules = framework.modules.all()
        serializer = FrameworkModuleSerializer(modules, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_module(self, request, pk=None):
        framework = self.get_object()
        serializer = FrameworkModuleSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(framework=framework)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FrameworkModuleViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = FrameworkModule.objects.all()
    serializer_class = FrameworkModuleSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        framework_id = self.request.query_params.get('framework_id', None)
        
        if framework_id:
            queryset = queryset.filter(framework_id=framework_id)
        
        return queryset