from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from ..models import Project, ProjectImage


class ProjectListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

        # Create test projects
        # active
        cls.project1 = Project.objects.create(
            title='Project 1',
            description='Description for project 1',
            client='Test Client',
            link='http://testlink.com',
            location='Test Location',
            start_date=timezone.now(),
            is_active=True
        )

        # inactive
        cls.project2 = Project.objects.create(
            title='Project 2',
            description='Description for project 2',
            location='Test Location project 2',
            start_date=timezone.now(),
            is_active=False
        )

        # Create test project image
        cls.project1_image1 = ProjectImage.objects.create(
            project=cls.project1,
            image='static/images/test_img/hero.png',
            is_main=True
        )
        cls.project1_image2 = ProjectImage.objects.create(
            project=cls.project1,
            image='static/images/test_img/shape.png',
            is_main=False
        )

    def test_project_list_url_and_template(self):
        response = self.client.get(reverse('portfolio:project_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfolio/project/project_list.html')

    def test_projects_in_project_list(self):
        response = self.client.get(reverse('portfolio:project_list'))
        self.assertContains(response, self.project1.title)
        # main image
        self.assertContains(response, self.project1_image1.image.url)
        # not main image
        self.assertNotContains(response, self.project1_image2.image.url)

        # inactive project
        self.assertNotContains(response, self.project2.title)


class ProjectDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

        # Create test projects
        # active
        cls.project1 = Project.objects.create(
            title='Project 1',
            description='Description for project 1',
            start_date=timezone.now(),
            is_active=True
        )
        # not active
        cls.project2 = Project.objects.create(
            title='Project 2',
            description='Description for project 2',
            start_date=timezone.now(),
            is_active=False
        )

        # Create test project image
        cls.project1_image1 = ProjectImage.objects.create(
            project=cls.project1,
            image='static/images/test_img/hero.png',
            is_main=True
        )
        cls.project1_image2 = ProjectImage.objects.create(
            project=cls.project1,
            image='static/images/test_img/shape.png',
            is_main=False
        )

    def test_project_detail_url_and_template(self):
        # active
        response = self.client.get(reverse('portfolio:project_detail', args=[self.project1.slug]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfolio/project/project_detail.html')
        # not active
        response = self.client.get(reverse('portfolio:project_detail', args=[self.project2.slug]))

        self.assertEqual(response.status_code, 404)

    def test_project_detail_context_data(self):
        response = self.client.get(reverse('portfolio:project_detail', args=[self.project1.slug]))

        self.assertTrue('project' in response.context)

        project = response.context['project']
        self.assertEqual(project, self.project1)
        self.assertContains(response, project.title)
        self.assertContains(response, project.description)
        self.assertContains(response, project.client)
        self.assertContains(response, project.link)
        self.assertContains(response, project.location)
        # image
        self.assertContains(response, self.project1_image1.image.url)
        self.assertContains(response, self.project1_image2.image.url)
        # Test the presence of next and previous project slugs
        project_slug_list = list(Project.active_objs.values_list('slug', flat=True).order_by('-datetime_updated'))
        index_obj = project_slug_list.index(project.slug)

        try:
            self.assertEqual(response.context['previous_project_slug'], project_slug_list[index_obj + 1])
            self.assertContains(response, project_slug_list[index_obj + 1])
        except IndexError:
            self.assertIsNone(response.context['previous_project_slug'])

        try:
            if index_obj != 0:
                self.assertEqual(response.context['next_project_slug'], project_slug_list[index_obj - 1])
                self.assertContains(response, project_slug_list[index_obj - 1])
            else:
                self.assertIsNone(response.context['next_project_slug'])
        except IndexError:
            self.assertIsNone(response.context['next_project_slug'])
