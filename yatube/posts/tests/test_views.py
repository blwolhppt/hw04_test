from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Group, Post
from django import forms
from django.http.response import HttpResponse

User = get_user_model()

class PostsViewTests(TestCase):
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
            id=0,
            author=cls.user,
            text='Тестовый пост 0',
            group=cls.group,
        )

        cls.post_1 = Post.objects.create(
            id=1,
            author=cls.user,
            text='Тестовый пост 1',
            group=None,
        )

    def setUp(self):
        self.user = self.__class__.user
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list',
                    kwargs={'slug': self.group.slug}): 'posts/group_list.html',
            reverse('posts:profile', kwargs={
                'username': self.user.username}): 'posts/profile.html',
            reverse('posts:post_detail', kwargs={
                'post_id': self.post_0.id}): 'posts/post_detail.html',
            reverse('posts:post_edit', kwargs={
                'post_id': self.post_0.id}): 'posts/create_post.html',
            reverse('posts:post_create'): 'posts/create_post.html',
        }

        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:index'))

        posts = response.context.get('page_obj').object_list
        itog = list(Post.objects.all())
        # print(itog)
        self.assertEqual(posts, itog)

    def test_group_posts_page_show_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': self.group.slug}))

        posts = response.context.get('page_obj').object_list
        group = response.context.get('group')
        itog = list(Post.objects.filter(group_id=self.group.id))

        self.assertEqual(posts, itog)
        self.assertEqual(group, self.group)

    def test_profile_page_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:profile', kwargs={'username': self.user.username}))

        posts = response.context.get('page_obj').object_list
        author = response.context.get('author')
        itog = list(Post.objects.filter(author_id=self.user.id))

        self.assertEqual(posts, itog)
        self.assertEqual(author, self.user)

    def test_post_detail_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:post_detail', kwargs={'post_id': self.post_0.id}))

        post = response.context.get('user_post')
        self.assertEqual(post, self.post_0)

    def test_create_post_show_correct_context(self):
        """Шаблон post_create сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:post_create'))

        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_edit_post_show_correct_context(self):
        """Шаблон edit_create сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:post_edit', kwargs={'post_id': self.post_0.id}))

        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        """Создаем автора и группу."""
        super().setUpClass()
        cls.user = User.objects.create_user(username='test_user')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_slug',
            description='description',
        )
        cls.post_0 = Post.objects.create(
            author=cls.user,
            text='Тестовый пост 0',
            group=cls.group,
        )

        cls.post_1 = Post.objects.create(
            author=cls.user,
            text='Тестовый пост 1',
            group=cls.group,
        )

        cls.post_2 = Post.objects.create(
            author=cls.user,
            text='Тестовый пост 2',
            group=cls.group,
        )

        cls.post_3 = Post.objects.create(
            author=cls.user,
            text='Тестовый пост 3',
            group=cls.group,
        )

        cls.post_4 = Post.objects.create(
            author=cls.user,
            text='Тестовый пост 4',
            group=cls.group,
        )

        cls.post_5 = Post.objects.create(
            author=cls.user,
            text='Тестовый пост 5',
            group=cls.group,
        )

        cls.post_6 = Post.objects.create(
            author=cls.user,
            text='Тестовый пост 6',
            group=cls.group,
        )

        cls.post_7 = Post.objects.create(
            author=cls.user,
            text='Тестовый пост 7',
            group=cls.group,
        )
        cls.post_8 = Post.objects.create(
            author=cls.user,
            text='Тестовый пост 8',
            group=cls.group,
        )

        cls.post_9 = Post.objects.create(
            author=cls.user,
            text='Тестовый пост 9',
            group=cls.group,
        )

        cls.post_10 = Post.objects.create(
            author=cls.user,
            text='Тестовый пост 10',
            group=cls.group,
        )


    def setUp(self):
        self.user = self.__class__.user
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_index_page(self):
        """Проверка пагинации index."""
        response = self.authorized_client.get(reverse('posts:index'))
        self.assertEqual(len(response.context['page_obj']), 10)

        response = self.authorized_client.get(reverse('posts:index')+'?page=2')
        self.assertEqual(len(response.context['page_obj']), 1)

    def test_group_list_page(self):
        """Проверка пагинации group_post."""
        response = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': self.group.slug}))
        self.assertEqual(len(response.context['page_obj']), 10)

        response = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': self.group.slug})
            + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 1)

    def test_profile_page(self):
        """Проверка пагинации profile."""
        response = self.authorized_client.get(
            reverse('posts:profile', kwargs={'username': self.user.username}))
        self.assertEqual(len(response.context['page_obj']), 10)

        response = self.authorized_client.get(
            reverse('posts:profile', kwargs={'username': self.user.username})
            + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 1)
