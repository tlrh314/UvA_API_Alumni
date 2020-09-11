from django.test import Client, TestCase
from django.urls import reverse

from apiweb.apps.alumni.factories import UserFactory
from apiweb.apps.research.factories import ThesisFactory


class ResearchTestMixin(object):
    @classmethod
    def setUpTestData(cls):
        cls.thesis = ThesisFactory.build()
        cls.ralph = UserFactory.build(
            username="ralph", first_name="Ralph", last_name="Wijers"
        )
        cls.ralph_password = "ProfDrRalphWijers"
        cls.ralph.set_password(cls.ralph_password)
        cls.ralph.save()
        cls.thesis.alumnus = cls.ralph
        cls.thesis.save()


class ResearchModelTestCase(ResearchTestMixin, TestCase):
    def test_factory(self):
        self.assertEqual(self.thesis.title[0:10], "TestThesis")

    def test_thesis_str(self):
        self.assertEqual(str(self.thesis), self.thesis.title)


class ResearchViewTestCase(ResearchTestMixin, TestCase):
    def setUp(self):
        self.client = Client()

    def test_thesis_list_anon(self):
        url = reverse("research:thesis-list")
        self.assertEqual(url, "/theses/")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/login/?next=/theses/")

    def test_thesis_list_when_logged_in(self):
        login_status = self.client.login(
            username=self.ralph.username, password=self.ralph_password
        )
        self.assertTrue(login_status)

        url = reverse("research:thesis-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "research/thesis_list.html")

    def test_thesis_detail_when_logged_in(self):
        login_status = self.client.login(
            username=self.ralph.username, password=self.ralph_password
        )
        self.assertTrue(login_status)

        url = reverse("research:thesis-detail", kwargs={"slug": self.thesis.slug},)
        self.assertEqual(url, "/theses/{}".format(self.thesis.slug))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "research/thesis_detail.html")
