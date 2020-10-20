from django.test import TestCase
from django.urls import reverse
from .models import Post
from django.contrib.auth import get_user_model

# Create your tests here.
class BlogPostTest(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user",
            email="test@email.ru",
            password="test_password"
        )
        self.post = Post.objects.create(
            title="test_title",
            body="test_post_text",
            author=self.user
        )

    def test_string_representation(self):

        self.assertEqual(str(self.post), self.post.title)

    def test_get_absolute_url(self):
        self.assertEqual(self.post.get_absolute_url(), "/post/1/")

    def test_post_content(self):
        self.assertEqual(self.post.title, "test_title")
        self.assertEqual(self.post.body, "test_post_text")
        self.assertEqual(self.post.author.username, "test_user")

    def test_post_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test_post_text")
        self.assertTemplateUsed(response, "home.html")

    def test_post_detail_view(self):
        response = self.client.get('/post/1/')
        no_response = self.client.get('/post/10000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "test_post_text")
        self.assertTemplateUsed(response, "post_detail.html")

    def test_post_edit_view(self):
        response = self.client.post(reverse('post_edit', args='1'), data={
            'title': "Updated title",
            'body': "Updated body"
        })
        self.assertEqual(response.status_code, 302)

    def test_post_delete_view(self):
        response = self.client.post(reverse('post_delete', args='1'))
        self.assertEqual(response.status_code, 200)





