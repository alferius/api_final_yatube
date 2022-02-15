from rest_framework import serializers
from rest_framework.exceptions import ParseError, ValidationError

from posts.models import Comment, Follow, Group, Post, User


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')
        read_only_fields = ('post',)


class PostSerializer(serializers.ModelSerializer):
    pub_date = serializers.DateTimeField(read_only=True)
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'text', 'pub_date', 'image',
                  'group', 'author',)

    def create(self, validated_data):
        if 'comments' not in self.initial_data:
            post = Post.objects.create(**validated_data)
            return post
        else:
            raise ParseError('Нельзя создать новый пост с комментариями')


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True,
                                        slug_field='username')
    following = serializers.SlugRelatedField(slug_field='username',
                                             queryset=User.objects.all())

    class Meta:
        model = Follow
        fields = ('user', 'following', )

    def validate(self, attrs):
        following = attrs['following']
        user = self.context['request'].user
        if following == user:
            raise ValidationError('Подписка на себя запрещена!')
        check_following = (
            user.follower.filter(following=following)
        )
        if check_following.exists():
            raise ValidationError('Подписка уже существует')
        return super().validate(attrs)
