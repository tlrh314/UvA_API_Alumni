import factory
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from faker import Factory

User = get_user_model()
FAKER = Factory.create("nl_NL")


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User  # alumni.models.Alumnus
        django_get_or_create = ("username",)

    email = factory.LazyAttribute(lambda _: FAKER.email())
    first_name = factory.LazyAttribute(lambda _: "TestUser: " + FAKER.first_name())
    last_name = factory.LazyAttribute(lambda _: FAKER.last_name())
    username = factory.LazyAttribute(
        lambda _: slugify(
            str(factory.SelfAttribute("first_name"))
            + str(factory.SelfAttribute("last_name"))
        )
    )

    is_active = True
    is_staff = False
    is_superuser = False


class AdminFactory(UserFactory):
    is_staff = True
    is_superuser = True
