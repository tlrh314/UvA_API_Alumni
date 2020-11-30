from django.contrib.auth.tokens import default_token_generator
from django.test import Client, TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from apiweb.apps.alumni.factories import UserFactory


class PasswordResetTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.ralph = UserFactory.build(
            username="ralph", first_name="Ralph", last_name="Wijers"
        )
        cls.ralph_password = "ProfDrRalphWijers"
        cls.ralph.set_password(cls.ralph_password)
        cls.ralph.save()

    def setUp(self):
        self.client = Client()

    def test_password_reset(self):
        url = reverse("site_password_reset")
        self.assertEqual(url, "/password_reset/")

    def test_password_reset_done(self):
        url = reverse(
            "site_password_reset_done",
        )
        self.assertEqual(url, "/password_reset/done/")

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/password_reset_done.html")

    def test_password_reset_confirm(self):
        url = reverse(
            "site_password_reset_confirm",
            kwargs={"uidb64": "myuidb64", "token": "mytoken"},
        )
        self.assertEqual(url, "/reset/myuidb64/mytoken/")

        uidb64 = urlsafe_base64_encode(force_bytes(self.ralph.pk))
        token = default_token_generator.make_token(self.ralph)
        url = reverse(
            "site_password_reset_confirm",
            kwargs={"uidb64": uidb64, "token": token},
        )
        self.assertEqual(url, "/reset/{}/{}/".format(uidb64, token))

    def test_password_reset_complete(self):
        url = reverse("site_password_reset_complete")
        self.assertEqual(url, "/reset/done/")


class PasswordChangeTestCase(TestCase):
    def test_reverse_password_change(self):
        url = reverse("site_password_change")
        self.assertEqual(url, "/password_change/")
