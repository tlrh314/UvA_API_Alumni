from django.test import Client, TestCase
from django.urls import reverse

from apiweb.apps.alumni.factories import UserFactory
from apiweb.apps.research.factories import ThesisFactory


class AlumniTestMixin(object):
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


class AlumniModelTestCase(AlumniTestMixin, TestCase):
    def test_factory(self):
        self.assertEqual(str(self.ralph), "Ralph Wijers")
        # Defaults for the UserFactory
        self.assertTrue(self.ralph.is_active)
        self.assertFalse(self.ralph.is_staff)
        self.assertFalse(self.ralph.is_superuser)


class AlumniViewTestCase(AlumniTestMixin, TestCase):
    def setUp(self):
        self.client = Client()

    def test_alumnus_list_anon(self):
        url = reverse("alumni:alumnus-list")
        self.assertEqual(url, "/alumni/")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/login/?next=/alumni/")

    def test_alumnus_list_when_logged_in(self):
        login_status = self.client.login(
            username=self.ralph.username, password=self.ralph_password
        )
        self.assertTrue(login_status)

        url = reverse("alumni:alumnus-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "alumni/alumnus_list.html")

    def test_alumnus_detail_when_logged_in(self):
        login_status = self.client.login(
            username=self.ralph.username, password=self.ralph_password
        )
        self.assertTrue(login_status)

        url = reverse(
            "alumni:alumnus-detail",
            args=[self.ralph.slug],
        )
        self.assertEqual(url, "/alumni/alumnus/{}/".format(self.ralph.slug))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "alumni/alumnus_detail.html")

    def test_alumnus_detail_when_logged_in_but_title_is_unknown(self):
        # Regression test for API-ALUMNI-D
        self.thesis.title = ""
        self.thesis.save()

        login_status = self.client.login(
            username=self.ralph.username, password=self.ralph_password
        )
        self.assertTrue(login_status)

        url = reverse("alumni:alumnus-detail", args=[self.ralph.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "alumni/alumnus_detail.html")
