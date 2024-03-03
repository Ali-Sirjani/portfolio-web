from django.test import TestCase
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse

from ..models import Project, ProjectImage


class ProjectModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # create project objects
        cls.project1 = Project.objects.create(
            title='Test Project 1',
            description='This is a test project',
            client='Test Client',
            link='http://testlink.com',
            location='Test Location',
            start_date=timezone.now(),
            is_active=True,
        )

        cls.project2 = Project.objects.create(
            title='Test Project 2',
            description='write a description for project2',
            start_date=timezone.now(),
            is_active=True,
        )

        cls.project3 = Project.objects.create(
            title='Test Project 3',
            description='test description',
            client='Test Client 3',
            link='http://testlink.com',
            location='Test Location',
            start_date=timezone.now(),
            is_active=False,
        )

    def test_project_attributes(self):
        project1 = self.project1
        self.assertEqual(project1.title, 'Test Project 1')
        self.assertEqual(project1.description, 'This is a test project')
        self.assertEqual(project1.client, 'Test Client')
        self.assertEqual(project1.link, 'http://testlink.com')
        self.assertEqual(project1.location, 'Test Location')
        self.assertIsNotNone(project1.start_date)
        self.assertFalse(project1.slug_change)
        self.assertEqual(project1.slug, slugify(project1.title))
        self.assertTrue(project1.is_active)
        # time
        self.assertIsNotNone(project1.datetime_created)
        self.assertIsNotNone(project1.datetime_updated)

        # str
        self.assertEqual(project1.title, str(project1))

    def test_get_absolute_url(self):
        self.assertEqual(self.project2.get_absolute_url(),
                         reverse('portfolio:project_detail', args=[self.project2.slug]))

    # Test the custom manager
    def test_active_objects_manager(self):
        active_projects = Project.active_objs.all()
        # project1 and project2 are active, project3 is inactive
        self.assertEqual(active_projects.count(), 2)

    # Test main_image_url method
    def test_main_image_url(self):
        self.assertIsNone(self.project1.main_image_url())


class ProjectImageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test project for the project image
        cls.project = Project.objects.create(
            title='Test Project',
            description='This is a test project',
            client='Test Client',
            link='http://testlink.com',
            location='Test Location',
            start_date=timezone.now(),
            is_active=True,
        )

        # Create a test project image
        cls.project_image1 = ProjectImage.objects.create(
            project=cls.project,
            image='static/images/test_img/hero.png',
            is_main=True
        )
        cls.project_image2 = ProjectImage.objects.create(
            project=cls.project,
            image='static/images/test_img/shape.png',
            is_main=False
        )

    def test_project_image_fields(self):
        project_image1 = self.project_image1
        self.assertEqual(project_image1.project, self.project)
        self.assertTrue(project_image1.is_main)
        # time
        self.assertIsNotNone(project_image1.datetime_created)
        self.assertIsNotNone(project_image1.datetime_updated)
        # str
        self.assertEqual(str(self.project_image1), f'{self.project_image1.project.pk}')

    def test_main_image_url_project(self):
        self.assertEqual(self.project.main_image_url(), '/media/static/images/test_img/hero.png')
