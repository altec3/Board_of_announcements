from rest_framework import pagination, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from ads.models import Ad
from ads.permissions import IsOwnerOrStaff
from ads.serializers import AdListSerializer, AdDetailSerializer


class AdPagination(pagination.PageNumberPagination):
    page_size = 4
    page_query_param = 'page'


class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    pagination_class = AdPagination

    serializers = {
        "list": AdListSerializer,
    }
    default_serializer = AdDetailSerializer

    permissions = {
        "create": [IsAuthenticated()],
        "retrieve": [IsAuthenticated()],
        "update": [IsAuthenticated(), IsOwnerOrStaff()],
        "partial_update": [IsAuthenticated(), IsOwnerOrStaff()],
        "destroy": [IsAuthenticated(), IsOwnerOrStaff()],
    }
    default_permissions = [AllowAny()]

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.default_serializer)

    def get_permissions(self):
        return self.permissions.get(self.action, self.default_permissions)

    # Переопределяем метод для добавления в serializer поля с автором.
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    pass


class AdsByUserListView(ListAPIView):
    """
    Get listing of ads from the current user
    """
    queryset = Ad.objects.all()
    pagination_class = AdPagination
    serializer_class = AdListSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrStaff]

    def get_queryset(self):
        queryset = self.queryset
        return queryset.filter(author_id=self.request.user.pk)
