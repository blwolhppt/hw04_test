from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Group, Post
from django import forms
from django.http.response import HttpResponse

User = get_user_model()


class PostsFormsTests(TestCase):
    def __init__(self, methodName: str = ...):
        super().__init__(methodName)
        self.author = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='test_user')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_slug',
            description='description',
        )
        cls.post_0 = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
            group=cls.group,
        )

    def setUp(self):
        self.user = self.__class__.user
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post(self):
        """Валидная форма создает запись в create_post."""

        form_data = {
            'text': 'Новый Тестовый пост',
            'group': self.group.id
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response,
                             reverse('posts:profile',
                                     kwargs={'username': self.user.username}))

        self.assertTrue(Post.objects.filter(text='Тестовый пост',
                                            author=self.user,
                                            group=self.group).exists())


    def test_edit_post(self):
        """Валидная форма изменяет запись в edit_post."""

        form_data = {
            'text': 'Новый Тестовый пост',
            'group': self.group.id
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={
                'post_id': self.post_0.id}),
            data=form_data,
            follow=True)
        modified_post = Post.objects.get(id=self.post_0.id)
        self.assertRedirects(response, reverse('posts:post_detail', args=(1,)))

        self.assertNotEqual(modified_post.text, self.post_0.text)




