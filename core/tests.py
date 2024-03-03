from django.test import TestCase
from django.db import IntegrityError
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Profile


class ProfileModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test user
        cls.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

    def setUp(self) -> None:
        self.profile = Profile.objects.get(user=self.user)

    def test_profile_attributes(self):
        profile = self.profile

        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.first_name, '')
        self.assertEqual(profile.last_name, '')
        self.assertEqual(profile.picture, '../static/images/logo-icon.png')
        # time
        self.assertIsNotNone(profile.datetime_created)
        self.assertIsNotNone(profile.datetime_updated)
        # str
        self.assertEqual(str(profile), 'testuser')

    def test_one_to_one_user(self):
        with self.assertRaises(IntegrityError):
            Profile.objects.create(user=self.user)


class ProfileViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test user
        cls.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

    def setUp(self) -> None:
        self.profile = Profile.objects.get(user=self.user)

    def test_profile_view_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('core:profile_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/profile.html')

    def test_profile_view_unauthenticated(self):
        response = self.client.get(reverse('core:profile_page'))
        self.assertRedirects(response, '/accounts/login/?next=/profile/')

    def test_profile_view_update_valid_form(self):
        self.client.force_login(self.user)
        data = {
            'first_name': 'Jane',
            'last_name': 'Doe',
        }
        response = self.client.post(reverse('core:profile_page'), data)
        self.assertEqual(response.status_code, 200)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.first_name, 'Jane')
        self.assertEqual(self.profile.last_name, 'Doe')


class SetUsernameViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test user
        cls.user1 = get_user_model().objects.create_user(username='testuser', password='testpassword')
        cls.user2 = get_user_model().objects.create_user(username='TestUserExists', password='testpassword',
                                                         email='test@gmail.com')

    def test_set_username_view_authenticated(self):
        self.client.force_login(self.user1)
        response = self.client.post(reverse('core:set_username'))
        self.assertEqual(response.status_code, 400)  # Because form is empty
        self.assertIsInstance(response, JsonResponse)

    def test_set_username_view_invalid_username(self):
        self.client.force_login(self.user1)
        response = self.client.post(reverse('core:set_username'), {'username': ''})
        self.assertEqual(response.status_code, 400)
        self.assertIsInstance(response, JsonResponse)

    def test_set_username_view_valid_username(self):
        new_username = 'new_test_user'
        self.client.force_login(self.user1)
        response = self.client.post(reverse('core:set_username'), {'username': new_username})

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)

        # Check if the username was changed successfully
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.username, new_username)

    def test_set_username_view_already_used_username(self):
        self.client.force_login(self.user1)
        response = self.client.post(reverse('core:set_username'),
                                    {'username': self.user1.username})  # Already username of user1

        self.assertEqual(response.status_code, 400)

        self.client.force_login(self.user1)
        response = self.client.post(reverse('core:set_username'),
                                    {'username': self.user2.username})  # Already existing username

        self.assertEqual(response.status_code, 400)

    def test_set_username_view_anonymous_user(self):
        response = self.client.post(reverse('core:set_username'), {'username': 'testuser'})
        self.assertEqual(response.status_code, 302)  # Redirects to login page
