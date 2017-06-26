from backend.models import Image, Comment
from backend.serializers import ImageSerializer, UserSerializer, CommentSerializer
from backend.permissions import IsOwnerOrReadOnly
from django.contrib.auth.models import User
from rest_framework import generics, permissions, viewsets, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.shortcuts import get_object_or_404


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ImageViewSet(viewsets.ModelViewSet):
    serializer_class = ImageSerializer
    queryset = Image.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentViewSet(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
    mixins.DestroyModelMixin, mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)


class NestedCommentViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)

    def get_image(self, request, image_pk=None):
        """
        Look for the referenced image
        """
        # Check if the referenced image exists
        image = get_object_or_404(Image.objects.all(), pk=image_pk)

        # Check permissions
        self.check_object_permissions(self.request, image)

        return image

    def create(self, request, *args, **kwargs):
        self.get_image(request, image_pk=kwargs['image_pk'])

        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(
            owner=self.request.user,
            image_id=self.kwargs['image_pk']
        )

    def get_queryset(self):
        return Comment.objects.filter(image=self.kwargs['image_pk'])

    def list(self, request, *args, **kwargs):
        self.get_image(request, image_pk=kwargs['image_pk'])

        return super().list(request, *args, **kwargs)
