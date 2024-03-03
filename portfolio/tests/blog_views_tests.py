from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.http import Http404
from unittest.mock import patch

from jalali_date.templatetags.jalali_tags import to_jalali

from ..models import Category, Post, PostImage, PostComment
from core.templatetags.trans_fa import num_fa


class PostListAndSearchViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

        # Create test categories
        cls.category1 = Category.objects.create(
            name='Category 1',
            slug='category-1'
        )

        cls.category2 = Category.objects.create(
            name='Category 2',
            slug='category-2'
        )

        # Create test posts
        # active
        cls.post1 = Post.objects.create(
            title='Post 1',
            description='Description for post 1',
            can_published=True,
            category=cls.category1
        )

        cls.post2 = Post.objects.create(
            title='Post 2',
            description='Description for post 2',
            can_published=True,
            category=cls.category2
        )

        # inactive
        cls.post3 = Post.objects.create(
            title='Post 3',
            description='Description for post 3',
            can_published=False,
        )

        # Create a test post image
        cls.post2_image1 = PostImage.objects.create(
            post=cls.post2,
            image='static/images/test_img/hero.png',
            is_main=True
        )
        cls.post2_image2 = PostImage.objects.create(
            post=cls.post2,
            image='static/images/test_img/shape.png',
            is_main=False
        )

    def test_post_list_url_and_template(self):
        response = self.client.get(reverse('portfolio:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfolio/blog/post_list.html')

    def test_posts_in_post_list(self):
        response = self.client.get(reverse('portfolio:post_list'))
        # post1 active
        self.assertContains(response, self.post1.title)
        self.assertContains(response, self.post1.category)
        self.assertContains(response, num_fa(to_jalali(self.post1.datetime_updated, "%Y/%m/%d")))
        # post2 active
        self.assertContains(response, self.post2.title)
        # post2_image1 is main
        self.assertContains(response, self.post2_image1.image.url)
        self.assertNotContains(response, self.post2_image2.image.url)

        # post3 inactive
        self.assertNotContains(response, self.post3.title)

    def test_posts_in_post_list_category(self):
        response = self.client.get(reverse('portfolio:post_category_list', args=[self.category1.slug]))
        # post1 active, category1
        self.assertContains(response, self.post1.title)
        self.assertContains(response, self.post1.category)
        self.assertContains(response, num_fa(to_jalali(self.post1.datetime_updated, "%Y/%m/%d")))
        # post2 active, category2
        # post2 show as recent posts
        self.assertContains(response, self.post2.title)
        # post2_image1 is main
        self.assertContains(response, self.post2_image1.image.url)
        self.assertNotContains(response, self.post2_image2.image.url)

        self.assertTrue('posts' in response.context)
        posts = response.context['posts']
        self.assertEqual(posts.count(), 1)
        self.assertTrue(self.post1 in posts)
        self.assertFalse(self.post2 in posts)

        # post3 inactive
        self.assertNotContains(response, self.post3.title)

    def test_post_search_url_and_template(self):
        response = self.client.get(reverse('portfolio:post_search'))
        # q didn't pass
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfolio/blog/search_q_none.html')
        # q did pass
        response = self.client.get(reverse('portfolio:post_search'), {'q': 'test'})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfolio/blog/search_page.html')

    def test_posts_in_post_search_view(self):
        # all posts
        response = self.client.get(reverse('portfolio:post_search'), {'q': 'post'})
        # post2 active
        self.assertContains(response, self.post2.title)
        # post2_image1 is main
        self.assertContains(response, self.post2_image1.image.url)
        self.assertNotContains(response, self.post2_image2.image.url)
        # post1 active
        self.assertContains(response, self.post1.title)
        self.assertContains(response, self.post1.category)
        self.assertContains(response, num_fa(to_jalali(self.post1.datetime_updated, "%Y/%m/%d")))

        self.assertTrue('posts' in response.context)
        posts = response.context['posts']
        self.assertEqual(posts.count(), 2)
        self.assertTrue(self.post1 in posts)
        self.assertTrue(self.post2 in posts)

        # post3 inactive
        self.assertNotContains(response, self.post3.title)

        # just post2
        response = self.client.get(reverse('portfolio:post_search'), {'q': 'post 2'})

        self.assertTrue('posts' in response.context)
        posts = response.context['posts']
        self.assertEqual(posts.count(), 1)
        self.assertFalse(self.post1 in posts)
        self.assertTrue(self.post2 in posts)

        # search based on category name
        response = self.client.get(reverse('portfolio:post_search'), {'q': 'categoRY 2'})

        self.assertTrue('posts' in response.context)
        posts = response.context['posts']
        self.assertEqual(posts.count(), 1)
        self.assertFalse(self.post1 in posts)
        self.assertTrue(self.post2 in posts)

        # search no result
        response = self.client.get(reverse('portfolio:post_search'), {'q': 'empty'})

        self.assertTrue('posts' in response.context)
        posts = response.context['posts']
        self.assertEqual(posts.count(), 0)


class PostDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

        # Create test category
        cls.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )

        # Create test post
        cls.post = Post.objects.create(
            title='Test Post',
            description='Description for test post',
            can_published=True,
            category=cls.category
        )

    def test_post_detail_url_and_template(self):
        response = self.client.get(reverse('portfolio:post_detail', args=[self.post.slug]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfolio/blog/post_detail.html')

    def test_post_detail_inactive_post(self):
        # Create an inactive post
        inactive_post = Post.objects.create(
            title='Inactive Post',
            description='Description for inactive post',
            can_published=False,
            category=self.category
        )

        response = self.client.get(reverse('portfolio:post_detail', args=[inactive_post.slug]))

        self.assertEqual(response.status_code, 404)

    def test_post_detail_post_info(self):
        response = self.client.get(reverse('portfolio:post_detail', args=[self.post.slug]))

        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.description)

    def test_post_detail_login_required(self):
        response = self.client.post(reverse('portfolio:post_detail', args=[self.post.slug]))

        # Check if the response redirects to the login page
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    @patch('django.contrib.messages.success')
    def test_post_detail_create_comment(self, mock_success_message):
        self.client.force_login(self.user)
        form_data = {
            'text': 'This is a test comment'
        }

        response = self.client.post(reverse('portfolio:post_detail', args=[self.post.slug]), data=form_data)

        # Check if the comment is created successfully
        self.assertEqual(response.status_code, 302)
        self.assertTrue(PostComment.objects.filter(author=self.user).exists())

        # Check if success message is displayed
        mock_success_message.assert_called_once()

    def test_post_detail_show_confirmed_comments(self):
        # Create confirmed and unconfirmed comments
        confirmed_comment = PostComment.objects.create(post=self.post, author=self.user, text='Confirmed comment', confirmation=True)
        unconfirmed_comment = PostComment.objects.create(post=self.post, author=self.user, text='Unconfirmed comment', confirmation=False)

        response = self.client.get(reverse('portfolio:post_detail', args=[self.post.slug]))

        # Check if confirmed comment is displayed
        self.assertContains(response, 'Confirmed comment')

        # Check if unconfirmed comment is not displayed
        self.assertNotContains(response, 'Unconfirmed comment')
