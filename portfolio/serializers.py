__author__ = 'dali'
from core.models import Video
from .models import PortfolioQuestion, PortfolioAnswer, Comment, Document
from rest_framework import serializers


class VideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Video
        fields = ('id', 'name', 'youtube_id',)


class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document
        fields = ('id', 'name', 'document_id',)


class JSONSerializerField(serializers.WritableField):
    pass


class PortfolioQuestionSerializer(serializers.ModelSerializer):
    video = VideoSerializer(required=False)
    document = DocumentSerializer(required=False)
    thumbnail = serializers.Field(source='thumbnail')

    class Meta:
        model = PortfolioQuestion
        fields = ('id', 'course', 'title', 'video', 'thumbnail', 'document', 'description', 'timestamp')


class PortfolioAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = PortfolioAnswer



class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
