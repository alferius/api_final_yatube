from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField('Заголовок',
                             max_length=200,
                             help_text='Название группы')
    slug = models.SlugField('Адрес URLа', unique=True, help_text='URL группы')
    description = models.TextField('Описание', help_text='Описание группы')

    def __str__(self) -> str:
        return self.title


class Post(models.Model):
    text = models.TextField('Текст поста', help_text='Введите текст поста')
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор'
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='groups4all',
        verbose_name='Группа',
        help_text='Выберите группу'
    )
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True,
        help_text='Выберите картинку'
    )
    # изменяет вывод зщстов и не проходят тесты с пагинацией
    # class Meta:
    #     ordering = ('-pub_date',)

    def __str__(self) -> str:
        return self.text[:15]


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )
    text = models.TextField('Текст комментария',
                            help_text='Введите текст комментария')
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    def __str__(self) -> str:
        return self.text[:15]


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Пользователь',
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('user', 'following'),
                                    name='one_following'),
            models.CheckConstraint(check=~models.Q(user=models.F('following')),
                                   name='user_not_author')
        ]

    def __str__(self) -> str:
        return self.user.username
