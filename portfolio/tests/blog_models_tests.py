from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.utils.text import slugify

from ..models import Category, TopCategory, Post, PostImage, PostComment


class CategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create four test categories
        cls.category1 = Category.objects.create(
            name='Category 1',
        )

        cls.category2 = Category.objects.create(
            name='Category 2',
            parent=cls.category1
        )

        cls.category3 = Category.objects.create(
            name='Category 3',
            parent=cls.category1
        )

        cls.category4 = Category.objects.create(
            name='Category 4',
            parent=cls.category2
        )

    def test_category_attributes(self):
        category1 = self.category1

        self.assertEqual(category1.name, 'Category 1')
        self.assertFalse(category1.slug_change)
        self.assertEqual(category1.slug, slugify(category1.name))
        # time
        self.assertIsNotNone(category1.datetime_created)
        self.assertIsNotNone(category1.datetime_updated)
        # str
        self.assertEqual(self.category1.name, str(self.category1))

    def test_category_absolute_url(self):
        self.assertEqual(self.category1.get_absolute_url(),
                         reverse('portfolio:post_category_list', args=[self.category1.slug]))

    def test_category_hierarchy(self):
        # Test hierarchical relationships
        self.assertEqual(self.category1.get_descendants().count(), 3)
        self.assertEqual(self.category1.get_ancestors().count(), 0)

        self.assertEqual(self.category2.get_descendants().count(), 1)
        self.assertEqual(self.category2.get_ancestors().count(), 1)

        self.assertEqual(self.category3.get_descendants().count(), 0)
        self.assertEqual(self.category3.get_ancestors().count(), 1)

        self.assertEqual(self.category4.get_descendants().count(), 0)
        self.assertEqual(self.category4.get_ancestors().count(), 2)


class TopCategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test category
        cls.category = Category.objects.create(
            name='Test Category',
            slug_change=False,
            slug='test-category'
        )

        # Create a test top category
        cls.top_category = TopCategory.objects.create(
            category=cls.category,
            level='1',
            is_top_level=True
        )

    def test_top_category_attributes(self):
        top_category = self.top_category

        # Check category attribute
        self.assertEqual(top_category.category, self.category)
        # Check level attribute
        self.assertEqual(top_category.level, '1')
        # Check is_top_level attribute
        self.assertTrue(top_category.is_top_level)
        # time
        self.assertIsNotNone(top_category.datetime_created)
        self.assertIsNotNone(top_category.datetime_updated)
        # Check str method
        self.assertEqual(str(top_category), 'Test Category')

    def test_one_to_one_category(self):
        with self.assertRaises(IntegrityError):
            TopCategory.objects.create(
                category=self.category,
                level='2',
                is_top_level=False
            )


class PostModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test category
        cls.category = Category.objects.create(
            name='Test Category',
            slug_change=False,
            slug='test-category'
        )

        # Create a test post
        cls.post1 = Post.objects.create(
            category=cls.category,
            title='Test Post 1',
            description='This is a test post description.',
            can_published=True,
        )

        cls.post2 = Post.objects.create(
            title='Test Post 2',
            description='This is a test post description. (post 2)',
            can_published=True,
        )

        cls.post2 = Post.objects.create(
            title='Test Post 3',
            description='This is a test description. (post 3)',
            can_published=False,
        )

    def test_post_attributes(self):
        post1 = self.post1

        # Check category attribute
        self.assertEqual(post1.category, self.category)
        # Check title attribute
        self.assertEqual(post1.title, 'Test Post 1')
        # Check description attribute
        self.assertEqual(post1.description, 'This is a test post description.')
        # Check can_published attribute
        self.assertTrue(post1.can_published)
        # Check slug_change attribute
        self.assertFalse(post1.slug_change)
        # Check slug attribute
        self.assertEqual(post1.slug, slugify(post1.title))
        # time
        self.assertIsNotNone(post1.datetime_created)
        self.assertIsNotNone(post1.datetime_updated)
        # Check __str__ method
        self.assertEqual(str(post1), post1.title)

    def test_post_absolute_url(self):
        self.assertEqual(self.post2.get_absolute_url(), reverse('portfolio:post_detail', args=[self.post2.slug]))

    def test_main_image_url(self):
        self.assertIsNone(self.post2.main_image_url())

    def test_custom_active_manager(self):
        # all objects
        self.assertEqual(Post.objects.all().count(), 3)

        # post1 and post2 are active, post3 is inactive
        self.assertEqual(Post.active_objs.all().count(), 2)


class PostImageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test post for the post image
        cls.post = Post.objects.create(
            title='Test Post',
            description='This is a test post description.',
            can_published=True,
        )

        # Create a test post image
        cls.post_image1 = PostImage.objects.create(
            post=cls.post,
            image='static/images/test_img/hero.png',
            is_main=True
        )
        cls.post_image2 = PostImage.objects.create(
            post=cls.post,
            image='static/images/test_img/shape.png',
            is_main=False
        )

    def test_post_image_fields(self):
        post_image1 = self.post_image1
        self.assertEqual(post_image1.post, self.post)
        self.assertTrue(post_image1.is_main)
        # time
        self.assertIsNotNone(post_image1.datetime_created)
        self.assertIsNotNone(post_image1.datetime_updated)

        # Check the __str__ method
        self.assertEqual(str(self.post_image1), f'{self.post_image1.post.pk}')

    def test_main_image_url_post(self):
        # Assuming you have a method like main_image_url in your Post model
        self.assertEqual(self.post.main_image_url(), '/media/static/images/test_img/hero.png')


class PostCommentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test user
        cls.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

        # Create a test post
        cls.post = Post.objects.create(
            title='Test Post',
            description='This is a test post description.',
            can_published=True,
            slug_change=False,
            slug='test-post'
        )

        # Create a test post comment hierarchy
        cls.comment1 = PostComment.objects.create(
            post=cls.post,
            author=cls.user,
            text='Comment 1',
            confirmation=False
        )

        cls.comment2 = PostComment.objects.create(
            post=cls.post,
            author=cls.user,
            text='Comment 2',
            confirmation=True,
            parent=cls.comment1
        )

        cls.comment3 = PostComment.objects.create(
            post=cls.post,
            author=cls.user,
            text='Comment 3',
            confirmation=True,
            parent=cls.comment1
        )

        cls.comment4 = PostComment.objects.create(
            post=cls.post,
            author=cls.user,
            text='Comment 4',
            confirmation=False,
            parent=cls.comment2
        )

    def test_post_comment_fields(self):
        post_comment1 = self.comment1

        # Check parent field
        self.assertIsNone(post_comment1.parent)
        # Check post field
        self.assertEqual(post_comment1.post, self.post)
        # Check author field
        self.assertEqual(post_comment1.author, self.user)
        # Check text field
        self.assertEqual(post_comment1.text, 'Comment 1')
        # Check confirmation field
        self.assertFalse(post_comment1.confirmation)
        # time
        self.assertIsNotNone(post_comment1.datetime_created)
        self.assertIsNotNone(post_comment1.datetime_updated)
        # str
        self.assertEqual(f'author: {post_comment1.author}, post pk: {post_comment1.post.pk}', str(post_comment1))

    def test_comment_hierarchy(self):
        # Test hierarchical relationships
        self.assertIsNone(self.comment1.parent)
        self.assertEqual(list(self.comment1.get_children()), [self.comment2, self.comment3])

        self.assertEqual(self.comment2.parent, self.comment1)
        self.assertEqual(list(self.comment2.get_children()), [self.comment4])

        self.assertEqual(self.comment3.parent, self.comment1)
        self.assertEqual(list(self.comment3.get_children()), [])

        self.assertEqual(self.comment4.parent, self.comment2)
        self.assertEqual(list(self.comment4.get_children()), [])

