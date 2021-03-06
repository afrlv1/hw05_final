from django.test import TestCase, Client, override_settings
from posts.models import Post, Group, Follow
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from os import path
from django.core.cache import cache
from django.core.cache.backends import locmem

User = get_user_model()

class PostsTest_Sprint5(TestCase):
    def setUp(self):
        cache.clear()
        self.client = Client()
        self.user = User.objects.create_user(
            username='test_user',
            email='test_user@test.ru',
            password='testpass1'
        )
        #создаем тестовый пост, который потом будет использоваться для тестов
        self.post = Post.objects.create(text='The test post', author=self.user)

#После регистрации пользователя создается его персональная страница (profile)
    def test_profile(self):
        # формируем GET-запрос к странице профиля тестового пользователя
        response = self.client.get('/test_user/')
        self.assertEqual(response.status_code, 200)

#Авторизованный пользователь может опубликовать пост (new)
    def test_logged_in(self):
        new_post_text = 'The new test post'
        self.client.login(username='test_user', password='testpass1')
        # отправляем запрос на создание нового тестового поста
        response_new_post_page = self.client.post('/new/', {'text': new_post_text})
        self.assertEqual(response_new_post_page.status_code, 302)
        # проверяем - появился ли текст нового поста на странице
        response_main_page = self.client.get('/')
        self.assertContains(response_main_page, text=new_post_text)

#Неавторизованный посетитель не может опубликовать пост (его редиректит на страницу входа)
    def est_not_logged_in(self):
        self.client.logout()
        response = self.client.get('/new/')
        self.assertRedirects(response, '/auth/login/?next=/new/')

# После публикации поста новая запись появляется на главной странице сайта (index),
# на персональной странице пользователя (profile), и на отдельной странице поста (post)
    def test_post(self):
        self.client.login(username='test_user', password='testpass1')
        post_text = 'The new second test post'
        #отправляем запрос на создание еще одного нового поста и проверяем успешно ли
        response_new_post_page = self.client.post(f'/new/', {'text': post_text},)
        self.assertEqual(response_new_post_page.status_code, 302)
        #Берем ID вновь созданного поста
        self.post_id = Post.objects.get(text=post_text).id
        #перебор url для проверки: на главной странице, в профиле и на странице поста
        for url in ('', '/test_user/', f'/test_user/{self.post_id}/'):
            response_post = self.client.get(url)
            self.assertContains(response_post, text=post_text)

    def test_edit_post(self):
        # Авторизованный пользователь может отредактировать свой пост и его содержимое
        # изменится на всех связанных страницах
        self.client.login(username='test_user', password='testpass1')
        # Запрашиваем ID созданного в самом начале тестового поста, который будем редактировать
        self.post_id = Post.objects.get(text='The test post').id
        edited_text = 'The edited test post'
        # отправляем запрос на редактирование тестового поста и потом проверяем его на успешность
        response_edit_post_page = self.client.post(f'/test_user/{self.post_id}/edit/', {'text': edited_text})
        self.assertEqual(response_edit_post_page.status_code, 302)
        #перебор url для проверки: на главной странице, в профиле и на странице поста
        for url in ('', '/test_user/', f'/test_user/{self.post_id}/'):
            response_post = self.client.get(url)
            self.assertContains(response_post, text=edited_text)

class UserTest_Sprint6(TestCase):
    def setUp(self):
        cache.clear()
        self.client = Client()
        self.user = User.objects.create_user(
            username='test_user',
            email='test_user@test.ru',
            password='testpass1'
        )
        self.group = Group.objects.create(title=' test', slug='test')
        PATH='./posts/small.gif'
        if path.exists(PATH) and path.isfile(PATH):
            image = PATH
        else:
            small_gif = (b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
                         b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
                         b'\x02\x4c\x01\x00\x3b')
            image = SimpleUploadedFile('small.gif', small_gif, content_type='image/gif')

        self.post = Post.objects.create(text='Test post with image', author=self.user, group=self.group, image=image)

    def test_404(self):
        # Проверка что мы не можем найти страницу
        response = self.client.get('/bad_page/')
        self.assertEquals(response.status_code, 404)

    def test_image(self):
        # Проверка наличия тега изображения на странице
        for url in ('', '/test_user/', f'/group/test/'):
            response_post = self.client.get(url)
            self.assertContains(response_post, '<img')

    def test_non_image_protection(self):
        # Проверяем что нельзя загрузить не графический файл
        with open('README.md') as nonImg:
            response = self.client.post('/new/', {'text': 'Test post with image', 'image': nonImg}, follow=True)
            self.assertNotContains(response, '<img', status_code=200, msg_prefix='', html=False)

    def test_cache(self):
        self.client.login(username='test_user', password='testpass1')
        response = self.client.post('/new/', {
            'text': 'test text'}, follow=True)
        self.assertRedirects(response, '/')
        # проверка, что OrderedDict() содержит кеш
        self.assertTrue(locmem._caches[''])
        cache.clear()
        # проверка, что OrderedDict() пустой
        self.assertFalse(locmem._caches[''])


class TestSubscription(TestCase):
    def setUp(self):
        cache.clear()
        self.client = Client()
        self.follower = User.objects.create_user(
            username='testfollower',
            email='testfollower@test.ru',
            password='testpass1'
        )
        self.following = User.objects.create_user(
            username='testfollowing',
            email='testfollowing@test.ru',
            password='testpass2'
        )

    def test_follow_unfollow(self):
        self.client.force_login(self.follower)
        self.post = Post.objects.create(text='Test subscribe', author=self.following)
        response = self.client.get(f'/{self.following}/follow/')
        self.assertRedirects(response, f'/{self.following}/', status_code=302)
        response = Follow.objects.filter(user=self.follower).exists()
        self.assertTrue(response)
        response = self.client.get(f'/{self.following}/unfollow/')
        #self.assertRedirects(response, f'/{self.following}/', status_code=302,)
        response = Follow.objects.filter(user=self.follower).exists()
        self.assertFalse(response)

    def test_post_on_follow_page(self):
        self.text = 'Test add new post to follow page'
        self.unfollower = User.objects.create_user(
            username='testunfollower',
            email='testunfollower@test.ru',
            password='testpass3'
        )
        self.client.force_login(self.follower)
        self.client.get(f'/{self.following}/follow/')
        self.post = Post.objects.create(text=self.text, author=self.following)
        response = self.client.get('/follow/')
        self.assertContains(response, self.text, status_code=200, html=False)
        self.client.logout()
        self.client.force_login(self.unfollower)
        response = self.client.get('/follow/')
        self.assertNotContains(response, self.text, html=False,)

    def test_comments(self):
        self.text = 'Test comments'
        self.post = Post.objects.create(text='Test post', author=self.following)
        response = self.client.post(f'/{self.following}/{self.post.pk}/comment/', {'text': 'Error text'},)
        self.assertRedirects(response, f'/auth/login/?next=/{self.following}/{self.post.pk}/comment/', status_code=302)
        self.client.force_login(self.follower)
        response = self.client.post(f'/{self.following}/{self.post.pk}/comment/', {'text': self.text})
        self.assertEqual(response.status_code, 302)
        response = self.client.get(f'/{self.following}/{self.post.pk}/')
        self.assertContains(response, self.text, status_code=200, html=False,)
