from rest_framework import serializers

from ads.models import Ad


class CommentSerializer(serializers.ModelSerializer):
    # TODO сериалайзер для модели
    pass


class AdListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ["pk", "image", "title", "price", "description"]


class AdDetailSerializer(serializers.ModelSerializer):
    author_id = serializers.ReadOnlyField(source='author.pk')

    class Meta:
        model = Ad
        fields = [
            "pk", "image", "title", "price", "phone", "description",
            "author_first_name", "author_last_name", "author_id"
        ]
