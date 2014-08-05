__author__ = 'dali'
from core.models import Video
from .models import  Comment,Portfolio
from rest_framework import serializers


class VideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Video
        fields = ('id', 'name', 'youtube_id',)


class PortfolioSerializer(serializers.ModelSerializer):
    video = VideoSerializer(required=False)
    thumbnail_url = serializers.Field(source='get_thumbnail_url')
    tags = serializers.Field(source='tags')

    class Meta:
        model = Portfolio
        fields = ("id", "user", "name", "description", "timestamp", "video", "description", "thumbnail_url", "tags", "status",)


class PortfolioThumbSerializer(serializers.ModelSerializer):

    class Meta:
        model = Portfolio
        fields = ("id", "thumbnail",)


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'user', 'text', 'portfolio', 'created_on',)


