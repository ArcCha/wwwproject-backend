from backend.models import Image, Comment
from django.contrib.auth.models import User
from rest_framework import serializers


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Image
        fields = ('url', 'title', 'owner', 'image')
        read_only_fields = ('url', 'owner')


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = ('url', 'text', 'owner', 'image')
        read_only_fields = ('url', 'owner', 'image')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'images')
