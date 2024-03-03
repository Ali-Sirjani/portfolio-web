from django.test import TestCase
from django.contrib.auth import get_user_model

from ..models import ContactMe


class ContactMeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test user
        cls.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

        # Create a test contact message
        cls.contact_message1 = ContactMe.objects.create(
            user=cls.user,
            full_name='John Doe',
            email='john@example.com',
            subject='Test Subject',
            message='This is a test message.',
            answer=False
        )
        cls.contact_message2 = ContactMe.objects.create(
            full_name='Ben Doe',
            email='Ben@example.com',
            subject='Test Subject 2',
            message='This is a test message. for Ben',
            answer=False
        )

    def test_contact_message_fields(self):
        contact_message1 = self.contact_message1
        # Check user field
        self.assertEqual(contact_message1.user, self.user)
        # Check full_name field
        self.assertEqual(contact_message1.full_name, 'John Doe')
        # Check email field
        self.assertEqual(contact_message1.email, 'john@example.com')
        # Check subject field
        self.assertEqual(contact_message1.subject, 'Test Subject')
        # Check message field
        self.assertEqual(contact_message1.message, 'This is a test message.')
        # Check answer field
        self.assertFalse(contact_message1.answer)
        # time
        self.assertIsNotNone(contact_message1.datetime_created)
        self.assertIsNotNone(contact_message1.datetime_updated)
        # str
        self.assertEqual(str(contact_message1), f'{contact_message1.full_name} - {contact_message1.subject}')

        # contact_message2 test null user
        self.assertIsNone(self.contact_message2.user)
