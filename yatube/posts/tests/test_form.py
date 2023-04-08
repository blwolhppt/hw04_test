from django.test import Client, TestCase
from django.urls import reverse

from ..models import Post, Group, User


class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание'
        )
        cls.post_0 = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
            group=cls.group
        )

    def setUp(self):
        self.guest_client = Client()
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

    def test_edit_post_invalid(self):
        """Проверка на невалидные данные."""
        form_data = {
            'text': ' ',
        }
        self.authorized_client.post(
            reverse('posts:post_edit', args=f'{self.post_0.id}'),
            data=form_data,
            follow=True)
        self.assertFalse(Post.objects.filter(text='').exists())

    def test_guest_cannot_edit_post(self):
        """Проверка edit_post для guest_client."""
        form_data = {
            "text": "Тестовый пост(guest)",
            "group": self.group.id
        }
        response = self.guest_client.post(
            reverse("posts:post_edit", kwargs=({"post_id": self.post_0.id})),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(
            response, f"/posts/{self.post_0.id}/"
        )

    def test_guest_cannot_create(self):
        """Проверка create_post для guest_client."""
        form_data = {
            "text": "Тестовый пост (guest)",
            "group": self.group.id
        }
        response = self.guest_client.post(
            reverse("posts:post_create"),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(
            response, "/auth/login/?next=/create/"
        )

