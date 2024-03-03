from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model

from ..models import Project, ContactMe


class HomePageViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create test projects
        for i in range(10):
            Project.objects.create(
                title=f'Test Project {i+1}',
                description=f'Description for Test Project {i+1}',
                start_date=timezone.now(),
                is_active=True
            )

    def test_home_page_view_url_and_template(self):
        response = self.client.get(reverse('portfolio:home_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfolio/general/home_page.html')

    def test_home_page_view_queryset(self):
        response = self.client.get(reverse('portfolio:home_page'))
        self.assertEqual(response.status_code, 200)

        # Check if there are at most 6 projects in the context
        self.assertEqual(len(response.context['projects']), 6)
        self.assertIsNotNone(response.context['recent_posts'])

    def test_home_page_view_project_and_recent_post_info(self):
        response = self.client.get(reverse('portfolio:home_page'))
        self.assertEqual(response.status_code, 200)

        # Check if project information is present in the page
        for project in response.context['projects']:
            self.assertContains(response, project.title)

        # Check if recent post information is present in the page
        for recent_post in response.context['recent_posts']:
            self.assertContains(response, recent_post.title)
            self.assertContains(response, recent_post.category)


class ContactMeViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test user
        cls.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

    def test_contact_me_view_post_success_authenticated(self):
        url = reverse('portfolio:create_contact_message')
        data = {
            'full_name': 'Test User',
            'email': 'test@example.com',
            'subject': 'Test Subject',
            'message': 'Test Message',
        }
        self.client.force_login(self.user)
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 200)
        message_created = ContactMe.objects.get(full_name='Test User')
        self.assertEqual(message_created.user, self.user)
        self.assertEqual(message_created.email, 'test@example.com')
        self.assertEqual(message_created.subject, 'Test Subject')
        self.assertEqual(message_created.message, 'Test Message')

    def test_contact_me_view_post_success_unauthenticated(self):
        url = reverse('portfolio:create_contact_message')
        data = {
            'full_name': 'Test User without login',
            'email': 'test@gmail.com',
            'subject': 'Test Subject',
            'message': 'Test Message'
        }
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 200)
        message_created = ContactMe.objects.get(full_name='Test User without login')
        self.assertEqual(message_created.email, 'test@gmail.com')
        self.assertEqual(message_created.subject, 'Test Subject')
        self.assertEqual(message_created.message, 'Test Message')

    def test_contact_me_view_post_invalid_form(self):
        url = reverse('portfolio:create_contact_message')
        # Send invalid form data (missing required fields)
        data = {
            'full_name': '',
            'email': '',
            'subject': '',
            'message': ''
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 400)
        self.assertFalse(ContactMe.objects.filter(full_name='Test User').exists())
