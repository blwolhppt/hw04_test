from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from ..models import Group, Post

User = get_user_model()


class PostsURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # автор поста
        cls.user = User.objects.create_user(username='test_user')
        # рандомный юзер
        cls.user_random = User.objects.create_user(username='random')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_slug',
            description='description',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

        self.random_client = Client()
        self.random_client.force_login(self.user_random)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон (для всех). """
        templates_url_names = {
            '': 'posts/index.html',
            f'/group/{self.group.slug}/': 'posts/group_list.html',
            f'/profile/{self.user}/': 'posts/profile.html',
            f'/posts/{self.post.id}/': 'posts/post_detail.html',
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_urls_uses_correct_template_auth(self):
        """Проверка create_post для авторизованного
        (и редирект для edit_post)"""
        templates_url_names = {
            '/create/': 'posts/create_post.html',
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.random_client.get(address)
                self.assertTemplateUsed(response, template)

        response = self.random_client.get(
            f'/posts/{self.post.id}/edit', follow=True)
        self.assertRedirects(response, f"/posts/{self.post.id}/")

    def test_urls_uses_correct_template_author(self):
        """Проверка edit_post для автора. """
        templates_url_names = {
            f'/posts/{self.post.id}/edit': 'posts/create_post.html'
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_redirect_guest_client(self):
        """Проверка редиректов для guest_client. """
        response = self.guest_client.get(
            f'/posts/{self.post.id}/edit', follow=True)
        self.assertRedirects(response, f"/posts/{self.post.id}/")

        response = self.guest_client.get('/create/', follow=True)
        self.assertRedirects(response, "/auth/login/?next=/create/")
