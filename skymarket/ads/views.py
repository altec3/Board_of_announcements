from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import pagination, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from ads.models import Ad, Comment
from ads.permissions import IsOwnerOrStaff
from ads.serializers import AdListSerializer, AdDetailSerializer, CommentSerializer


class AdPagination(pagination.PageNumberPagination):
    page_size = 4
    page_query_param = 'page'


@extend_schema_view(
    list=extend_schema(summary="Список всех объявлений"),
    create=extend_schema(summary="Создать объявление"),
    retrieve=extend_schema(summary="Подробно об объявлении"),
    partial_update=extend_schema(summary="Изменить объявление"),
    destroy=extend_schema(summary="Удалить объявление"),
)
class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    pagination_class = AdPagination
    http_method_names = ["get", "post", "patch", "delete"]

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


@extend_schema_view(
    list=extend_schema(summary="Список отзывов к объявлению"),
    create=extend_schema(summary="Оставить отзыв"),
    retrieve=extend_schema(summary="Получить отзыв по ID"),
    partial_update=extend_schema(summary="Изменить отзыв"),
    destroy=extend_schema(summary="Удалить отзыв"),
)
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    pagination_class = AdPagination
    permission_classes = [IsAuthenticated, IsOwnerOrStaff]
    serializer_class = CommentSerializer
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        return self.queryset.filter(ad=self.kwargs['ad_pk'])

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, ad_id=self.kwargs['ad_pk'])


@extend_schema(summary="Мои объявления")
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
