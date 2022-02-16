from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .mixins import CreateListViewSet
from .permissions import IsAuthorOrReadOnlyPermission
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)
from posts.models import Comment, Follow, Group, Post


class PostViewSet(ModelViewSet):
    """
    Работа с публикациями: вывод, создание, обновление, удаление
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthorOrReadOnlyPermission,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(ReadOnlyModelViewSet):
    """
    Работа с группами: только отображение
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.AllowAny,)


class CommentViewSet(ModelViewSet):
    """
    Работа с комментариями: вывод, создание, обновление, удаление
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnlyPermission,)

    def list(self, serializer, **kwargs):
        post_id = int(kwargs['post_id'])
        post = get_object_or_404(Post, id=int(post_id))
        comments4post = post.comments.filter(post=post_id)
        page = self.paginate_queryset(comments4post)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(comments4post, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=int(self.kwargs['post_id']))
        serializer.save(author=self.request.user, post=post)

    def perform_update(self, serializer):
        post = get_object_or_404(Post, id=int(self.kwargs['post_id']))
        serializer.save(author=self.request.user, post=post)


class FollowViewSet(CreateListViewSet):
    """Подписочки на авторчиков :-)"""
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter, )
    search_fields = ('=following__username',)

    def perform_create(self, serializer):
        following = serializer.validated_data['following']
        serializer.save(user=self.request.user, following=following)

    def get_queryset(self):
        return self.request.user.follower.all()
